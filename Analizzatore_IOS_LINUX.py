import os
import json


def extract_mitre_techniques(report_folder, output_folder):
    """Estrae le tecniche MITRE dai report JSON e le salva in file di testo."""
    os.makedirs(output_folder, exist_ok=True)
    reports = os.listdir(report_folder)

    for report in reports:
        with open(os.path.join(report_folder, report), 'r', errors='ignore') as file:
            data = json.load(file)

        output_file = os.path.join(output_folder, report.replace("Report", "Mitre").replace(".json", ".txt"))
        with open(output_file, 'w') as out:
            print(f"Number of MITRE techniques: {len(data.get('mitre_attcks', []))}", file=out)
            for entry in data.get("mitre_attcks", []):
                print(f"attck_id: {entry.get('attck_id', 'N/A')}", file=out)


def filter_equivocal_techniques(mitre_folder, output_folder, equivocal_file):
    """Filtra le tecniche equivoche dai file MITRE e le salva."""
    os.makedirs(output_folder, exist_ok=True)

    with open(equivocal_file, 'r') as file:
        equivocal_techniques = set(line.strip() for line in file.readlines())

    for file_name in os.listdir(mitre_folder):
        if file_name.startswith("Mitre") and file_name.endswith(".txt"):
            input_file = os.path.join(mitre_folder, file_name)
            output_file = os.path.join(output_folder, f"EQUIVOCAL_{file_name}")

            with open(input_file, 'r') as inp, open(output_file, 'w') as out:
                for line in inp:
                    attck_id = line.split(":")[1].strip().split(".")[0]
                    if attck_id in equivocal_techniques:
                        out.write(line)


def analyze_equivocal_behaviours(equivocal_folder, output_folder, behaviour_file):
    """Analizza i comportamenti equivoci associati alle tecniche filtrate."""
    os.makedirs(output_folder, exist_ok=True)

    with open(behaviour_file, "r") as file:
        equivocal_behaviours = json.load(file)

    for file_name in os.listdir(equivocal_folder):
        unique_behaviours = set()
        output_file = os.path.join(output_folder, file_name.replace("EQUIVOCAL_Tecnics", "Equivocal_Behaviours"))

        with open(output_file, "w") as out:
            out.write(f"Analysis for {file_name}\n")

            with open(os.path.join(equivocal_folder, file_name), "r") as inp:
                for line in inp:
                    analysis_result = line.split(":")[1].strip().split(".")[0]
                    found = False
                    for behaviour, techniques in equivocal_behaviours.items():
                        if analysis_result in techniques:
                            found = True
                            if behaviour not in unique_behaviours:
                                out.write(f"{behaviour}\n")
                                unique_behaviours.add(behaviour)
                    if not found:
                        out.write("ERROR\n")


def main():
    base_folders = [
        "MAC_Goodware", "MAC_Malware", "Linux_Goodware", "Linux_Malware"
    ]

    equivocal_file = "EquivocalTecnics.txt"
    behaviour_file = "EquivocalBehaviours.txt"

    for folder in base_folders:
        report_folder = f"Reports_{folder}"
        mitre_folder = f"Mitre_Signatures_{folder}"
        equivocal_folder = f"Equivocal_Tecnics_{folder}"
        behaviour_folder = f"Equivocal_Behaviours_{folder}"

        print(f"Processing: {folder}...")
        extract_mitre_techniques(report_folder, mitre_folder)
        filter_equivocal_techniques(mitre_folder, equivocal_folder, equivocal_file)
        analyze_equivocal_behaviours(equivocal_folder, behaviour_folder, behaviour_file)

    print("Analysis complete!")


if __name__ == "__main__":
    main()
