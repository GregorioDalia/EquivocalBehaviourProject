import os
import json

# Definire il percorso del file JSON
Equivocal_Behaviours_File= "EquivocalBehaviours.txt"

Folder_Equivocal_Behaviours = "Equivocal_Behaviours"
Folder_Equivocal_Tecnics = "Equivocal_Tecnics"

with open(Equivocal_Behaviours_File, "r") as file:
    Equivocal_Behaviours = json.load(file)

# Elaborare ogni file nella cartella di input
for report_tec in os.listdir(Folder_Equivocal_Tecnics):

    unique_behaviours_results = set()

    output_filename = report_tec.replace("EQUIVOCAL_Tecnics", "Equivocal_Behaviours")
    output_filepath = os.path.join(Folder_Equivocal_Behaviours, output_filename)

    # Creare il file di output e scriverci dentro
    with open(output_filepath, "w") as output_file:
        output_file.write(f"Analysis for {report_tec}\n")

        # Aprire il file di input e leggere ogni linea
        input_filepath = os.path.join(Folder_Equivocal_Tecnics, report_tec)
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

                    for comportamento in Equivocal_Behaviours.keys():
                        if analysis_result in Equivocal_Behaviours.get(comportamento):
                            trovato=True
                            if comportamento not in unique_behaviours_results:
                                output_file.write(f"{comportamento}\n")
                                unique_behaviours_results.add(comportamento)

                    if not trovato:
                        output_file.write("ERRORE CODICE\n")