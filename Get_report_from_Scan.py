import subprocess
import json
import os

Folder_Scans= r"Scans"
Folder_Reports = r"Reports"

scans_list = os.listdir(Folder_Scans)

for File_Name in scans_list:
    with open(os.path.join(Folder_Scans, File_Name), 'r') as Nfile:
        scan = json.loads(Nfile.read())

    job_id = scan.get("job_id")

    print(f"Check {job_id} for {File_Name} \n")

    task_report = f'cd VxAPI-master && python vxapi.py report_get_summary {job_id}'

    try:
        output_report = subprocess.check_output(task_report, shell=True, text=True)
    except Exception as e:
        print("utf-8")
        output_report = subprocess.check_output(task_report, shell=True, encoding="utf-8")

    Final_report = output_report.replace('\033[0m', '')
    Report_json = json.loads(Final_report)

    if Report_json.get("state") != "SUCCESS":

        print("error id " + job_id +" state= " + Report_json.get("state") + "\n")
        print(f"File is {File_Name} \n")

        continue
    else:
        print("Report is ready")
        Name_Report = File_Name.replace("Scan", "Report")
        try:
            with open(os.path.join(Folder_Reports, Name_Report), 'w') as nfilereport:
                nfilereport.write(Final_report)
        except Exception as e:
            print("utf-8 output")
            with open(os.path.join(Folder_Reports, Name_Report), 'w', encoding="utf-8") as nfilereport:
                nfilereport.write(Final_report)
