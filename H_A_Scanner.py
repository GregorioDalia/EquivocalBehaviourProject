import os
import subprocess
import pandas as pd
import time


Dataset = "dataset.csv"
df = pd.read_csv(Dataset)

Sha_not_in_HA = "Sha_not_in_HA.txt"
Sha_Present_in_HA = "Sha_Present_in_HA.txt"
Folder_Report_from_DB = "Report_from_DB"


with open(Sha_not_in_HA, 'r') as sha_non_sottomessi_file:
    sha_to_submit_set = set(sha_non_sottomessi_file.read().splitlines())

with open(Sha_Present_in_HA, 'r') as sha_sottomessi_file:
    sha_done_set = set(sha_sottomessi_file.read().splitlines())

db_len  = len(df['sha'])
i = 0
count = 0



for sha_value in df['sha']:
    print(str(i) + "/" +str(db_len))
    print("COUNT = "+str(count))
    i = i+1

    if sha_value in sha_done_set or sha_value in sha_to_submit_set:
        print(f"{sha_value} alredy checked")
        if sha_value in sha_done_set:
            count = count+1
        continue

    search_SHA_command = f'cd VxAPI-master && python vxapi.py search_hash {sha_value}'
    start_time = time.time()

    try:
        result = subprocess.run(search_SHA_command, shell=True, capture_output=True, text=True, errors='ignore')
    except UnicodeDecodeError:
        print("UTF-8")
        result = subprocess.run(search_SHA_command, shell=True, capture_output=True, text=True, encoding="utf-8")
    except Exception as e:
        print(f"Unexpected Error: {e}")
        exit()

    if result.returncode == 0:
        output_search_SHA = result.stdout.replace('\033[0m', '')
    else:
        print(f"Error. Return Code: {result.returncode}")
        print(result)
        if "HTTPSConnectionPool" in str(result.stderr):
            print("No Internet")
            exit()
        else:
            print(result.stderr)
            exit()
    if "Quota limit has been exceeded" in output_search_SHA:
        print("Apy key limit")
        exit()

    if "[]" in output_search_SHA.split('\n')[0]:
        print(sha_value + " is not present in H.A. Database")
        with open(Sha_not_in_HA, 'a') as sha_non_sottomessi_file:
            sha_non_sottomessi_file.write(sha_value + "\n")

    else:
        print(sha_value + " MATCH!!!")
        count = count + 1
        # print(output_search_SHA)
        with open(Sha_Present_in_HA, 'a') as sha_sottomessi_file:
            sha_sottomessi_file.write(sha_value + "\n")

        try:
            with open(os.path.join(Folder_Report_from_DB, sha_value
                                                            + "_report.txt"), 'w') as newreport:
                newreport.write(output_search_SHA)
        except UnicodeDecodeError:
            print("utf-8 output")
            with open(os.path.join(Folder_Report_from_DB, sha_value
                                                            + "_report.txt"), 'w', encoding="utf-8") as newreport:
                newreport.write(output_search_SHA)
        except Exception as e:
            print("Unexpected Error")
            print(str(e))

    time_end = time.time()
    delta_time = time_end - start_time
    if delta_time < 1.8:
        time.sleep(1.8 - delta_time)