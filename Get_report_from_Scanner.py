import os
import json


Folder_Report_from_DB = r"Report_from_DB"
Folder_Reports = r"Reports"
list_reportsDB =os.listdir(Folder_Report_from_DB)


for composed_report in list_reportsDB:

    print("_______________")
    with open(os.path.join(Folder_Report_from_DB, composed_report), 'r') as File_report:
        reports = json.loads(File_report.read())

    for single_report in reports:

        try:
            enviroment = single_report['environment_description']
        except Exception as e:
            print("Exception "+str(e))
            continue

        if single_report['environment_description'] == "Static Analysis":
            print("Found a static analysis: useless")

        else:

            try:
                single_enviroment = single_report['environment_description'].replace(' ', '_')
            except Exception as e:
                single_enviroment= "NULL"



            print("Enviroment = " + single_enviroment)

            Name_report= "Report_" + composed_report.split('_')[0] + "_" + single_enviroment + ".txt"

            print("file report = " + Name_report)

            nfilereport_SINGOLO_path = os.path.join(Folder_Reports, Name_report)

            with open(nfilereport_SINGOLO_path, 'w') as nfilereport_SINGOLO:
                json.dump(single_report, nfilereport_SINGOLO, indent=4)


