import subprocess
import json
import os

Folder_Executables = r"Executables"

Folder_Scans = r"Scans"

file_names = os.listdir(Folder_Executables)

for name in file_names:

        print(f"Scan {name}")

        Executables_toScan = os.path.join(Folder_Executables, name)

        OS_codes = [140, 160]
        Dictonary_OS = {
            140: "Windows_11_64",
            160: "Windows_10_64",
            400: "Mac_Catalina_64_bit_(x86)",
            310: "Linux_(Ubuntu_20.04_64_bit)"
        }

        for Code in OS_codes:

            name_analisisys = name + "_" + Dictonary_OS[Code]

            print(f"Scan {name} on {Dictonary_OS[Code]}")

            try:
                comando_submit_file = f'cd VxAPI-master && python vxapi.py submit_file ../{Executables_toScan} {Code}'
                output_submit_file = subprocess.check_output(comando_submit_file, shell=True, text=True)

                File_output_submition = output_submit_file.replace('\033[0m', '')

                String_Name = name.split('.')[0]
                Name_file_scan = f'Scan_{String_Name}_{Dictonary_OS[Code]}.txt'

                result_submit_file = json.loads(File_output_submition)

                if (result_submit_file.get("message")
                    == "Quota limit has been exceeded, you have submitted too many files."):
                    print("Quota limit has been exceeded, you have submitted too many files.")
                    exit()

                if "job_id" not in result_submit_file:
                    print(f"Error for {name},no jobID\n")


                with open(os.path.join(Folder_Scans, Name_file_scan), 'w') as file:
                    file.write(File_output_submition)


            except Exception as e:
                print(f"Error for {name} : {str(e)}")

                continue