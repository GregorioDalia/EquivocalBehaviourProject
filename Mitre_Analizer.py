import os
import json

with open('EquivocalTecnics.txt', 'r') as file:
    content = file.readlines()

Equivocal_tecnics = set()

for line in content:
    clean_line = line.strip()

    Equivocal_tecnics.add(clean_line)

Folder_Equivocal_Tecnics = "Equivocal_Tecnics"

Folder_Mitre_Signatures = "Mitre_Signatures"

file_mitre_list = [file for file in os.listdir(Folder_Mitre_Signatures) if file.startswith("Mitre") and file.endswith(".txt")]

for file_name in file_mitre_list:
    input_file_path = os.path.join(Folder_Mitre_Signatures, file_name)

    output_file_path = os.path.join(Folder_Equivocal_Tecnics, f"EQUIVOCAL_Tecnics_{file_name.replace('Mitre_', '')}")

    with open(output_file_path, 'w') as output_file:
        with open(input_file_path, 'r') as file:

            for line in file:
                attck_id = line.split(":")[1].strip().split(".")[0]

                if attck_id in Equivocal_tecnics:
                    output_file.write(line)
