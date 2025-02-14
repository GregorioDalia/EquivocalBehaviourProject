
#API_KEY = "mefmiic044729c708xiw6hx95d4d9c82m46vi8za2537b889t805f2pacba51a1e"  # Inserisci la tua API Key
import os
import json
import requests
import time

# Configurazione API Hybrid Analysis
API_KEY = "mefmiic044729c708xiw6hx95d4d9c82m46vi8za2537b889t805f2pacba51a1e"  # Inserisci la tua API Key
HEADERS = {
    "accept": "application/json",
    "api-key": API_KEY,
    "Content-Type": "application/x-www-form-urlencoded"
}
BASE_URL = "https://www.hybrid-analysis.com/api/v2"

# Limiti API
API_CALL_DELAY = 60 / 199  # Attendere per evitare più di 199 richieste al minuto

# Definizione delle configurazioni per i diversi download
CONFIGS = [
    {"verdict": 3, "env_id": "400", "filetype": "macho", "folder": "Reports_MAC_Goodware",
     "sha_file": "Reports_MAC_Goodware_list.txt"},
    {"verdict": 5, "env_id": "400", "filetype": "macho", "folder": "Reports_MAC_Malware",
     "sha_file": "Reports_MAC_Malware_list.txt"},
    {"verdict": 3, "env_id": "310", "filetype": "elf", "folder": "Reports_Linux_Goodware",
     "sha_file": "Reports_Linux_Goodware_list.txt"},
    {"verdict": 5, "env_id": "310", "filetype": "elf", "folder": "Reports_Linux_Malware",
     "sha_file": "Reports_Linux_Malware_list.txt"}
]


def search_reports(verdict, env_id, filetype):
    """Effettua una ricerca per ottenere i report in base ai filtri specificati."""
    params = {
        "env_id": env_id,
        "verdict": verdict,
        "filetype": filetype
    }

    response = requests.post(f"{BASE_URL}/search/terms", headers=HEADERS, data=params)
    time.sleep(API_CALL_DELAY)  # Rispetta il rate limit

    if response.status_code != 200:
        print(f"Errore nella richiesta API ({verdict}, {env_id}, {filetype}):", response.text)
        return []

    try:
        data = response.json()

        # Controlliamo che "result" esista e sia una lista
        if "result" not in data or not isinstance(data["result"], list):
            print(f"Errore: Risultato inatteso dalla ricerca API ({verdict}, {env_id}, {filetype}):",
                  json.dumps(data, indent=4))
            return []

        return data["result"]  # Ora ritorniamo la lista corretta dei risultati

    except json.JSONDecodeError:
        print("Errore nel parsing della risposta API.")
        return []


def download_reports():
    for config in CONFIGS:
        folder = config["folder"]
        sha_file = config["sha_file"]
        os.makedirs(folder, exist_ok=True)

        results = search_reports(config["verdict"], config["env_id"], config["filetype"])
        print(f"Trovati {len(results)} report per {folder}. Inizio download...")

        with open(sha_file, "a") as sha_fp:
            for report in results:
                try:
                    report_id = report.get("job_id")
                    report_sha = report.get("sha256")

                    if not report_id or not report_sha:
                        print("Dati report mancanti, salto...")
                        continue

                    report_filename = os.path.join(folder, f"Report_{report_id}.json")

                    if os.path.exists(report_filename):
                        print(f"Report {report_id} già scaricato. Skipping...")
                        continue

                    response = requests.get(f"{BASE_URL}/report/{report_id}/summary", headers=HEADERS)
                    time.sleep(API_CALL_DELAY)  # Rispetta il rate limit

                    if response.status_code != 200:
                        print(f"Errore nel download del report {report_id}: {response.text}")
                        continue

                    try:
                        final_report = response.json()
                    except json.JSONDecodeError:
                        print(f"Errore nel parsing del report {report_id}.")
                        continue

                    if final_report.get("state") != "SUCCESS":
                        print(f"Errore nel report {report_id}, stato: {final_report.get('state')}")
                        continue

                    with open(report_filename, "w") as f:
                        json.dump(final_report, f, indent=4)
                    print(f"Report {report_id} salvato con successo.")

                    # Scrivi lo SHA nel file di testo
                    sha_fp.write(f"{report_sha}\n")

                except Exception as e:
                    print(f"Errore nel processamento del report {report_id}: {str(e)}")

        print(f"Download completato per {folder}.")


if __name__ == "__main__":
    download_reports()
