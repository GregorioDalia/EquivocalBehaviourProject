import os
import json

Folder_Reports = r"Reports"
Folder_Mitre_Signatures= r"Mitre_Signatures"
# Ottieni la lista dei file nella cartella
repor_list = os.listdir(Folder_Reports)

for report in repor_list:

    with open(os.path.join(Folder_Reports, report), 'r',errors='ignore') as Nfile_report:
        report_json = json.loads(Nfile_report.read())

    Name_File_Mitre = report.replace("Report", "Mitre")

    with open(os.path.join(Folder_Mitre_Signatures, Name_File_Mitre), 'w') as nfileMitre:
        print("Number  of occurence of  mitre_attcks:", len(report_json.get("mitre_attcks", [])), file=nfileMitre,
              flush=True)

        for entry in report_json.get("mitre_attcks", []):
            attck_id = entry.get("attck_id", "N/A")
            print("attck_id:", attck_id, file=nfileMitre, flush=True)