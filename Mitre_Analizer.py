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

'''
# Definire il percorso del file JSON
Comportamenti_Equivoci_File = "Comportamenti_Equivoci.txt"
Comportamenti_Equivoci_folder ="Equivocal_Behaviours_Report_Summary"
# Leggere il JSON dal file
with open(Comportamenti_Equivoci_File, "r") as file:
    comportamenti_equivoci = json.load(file)

# Elaborare ogni file nella cartella di input
for report_tecniche in os.listdir(Equivocal_Tecnics_folder):

    unique_behaviours_results = set()
    # Creare il nome del file di output con estensione "_Report.txt"
    output_filename = os.path.splitext(report_tecniche)[0] + "_Report.txt"
    output_filepath = os.path.join(Comportamenti_Equivoci_folder, output_filename)

    # Creare il file di output e scriverci dentro
    with open(output_filepath, "w") as output_file:
        output_file.write(f"Analysis for {report_tecniche}\n")

        # Aprire il file di input e leggere ogni linea
        input_filepath = os.path.join(Equivocal_Tecnics_folder, report_tecniche)
        with open(input_filepath, "r") as input_file:
            for line in input_file:
                # Analizzare ogni linea e prendere ciò che sta dopo i due punti
                line_parts = line.split(":")
                if len(line_parts) >= 2:
                    analysis_result = line_parts[1]
                    if "." in analysis_result:
                        analysis_result=analysis_result.split(".")[0]+"\n"
                    analysis_result = analysis_result.strip()

                    trovato = False

                    for comportamento in comportamenti_equivoci.keys():
                        if analysis_result in comportamenti_equivoci.get(comportamento):
                            trovato=True
                            if comportamento not in unique_behaviours_results:
                                output_file.write(f"{comportamento}\n")
                                unique_behaviours_results.add(comportamento)

                    if not trovato:
                        output_file.write("ERRORE CODICE\n")

'''
