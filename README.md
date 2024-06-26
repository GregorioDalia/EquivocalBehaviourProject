# EquivocalBehaviourProject

## Pipeline

This is the replication packege of the paper: "It’s Acting Odd! Exploring Equivocal Behaviors of Goodware".

This project contains all the necessary scripts used in the pipeline that led to the generation of the results mentioned in the paper.

In particular, it contains all the scripts that make it possible, starting from the executables or hashes, to generate the list of Equivocal Behaviour and all the necessary intermediate artefacts.

Before the scripts can be used to interact with the Hybrid Analisys platform, it is necessary to enter the api_key in the config.py file inside the ‘VxAPI-master’ folder, which is ‘A generic interface and CLI for all endpoints of the Falcon Sandbox API’ also available on github at the address:
https://github.com/PayloadSecurity/VxAPI/tree/master

The first scripts in the pipeline are :
1)H_A_Scanner.py
2)Submit_file_to_HA.py

The first is used to submit to the Hybrid analysis platform all the sha present in the ‘dataset.csv’ csv and where the sha is present in the platform's database, the reports are downloaded and saved in the ‘Report_from_DB’ folder. the script generates two ‘log’ files Sha_not_in_HA’ and “Sha_Present_in_HA” to keep track of which sha have been submitted and which are present on Hybrid Analisys

The second is used to submit to the platform all executables in the ‘Executables’ folder by generating scan reports that go into the ‘Scans’ folder.

Since the reports downloaded from the sha, and present in the ‘Report_from_DB’ folder, are an array of reports (one for each environment),and also composed of static analysis (useless in this context)

A script was written: ‘Get_report_from_Scanner.py’ which filters the static analyses (discarding them) and generates a single report for each scanning environment called ‘Report_{sha256}_{Environment}.txt’ and saves it in the ‘Reports’ folder.

In the Scans folder are the scan reports of the executables, through the script ‘Get_report_from_scan.py’ one interacts with the Hybrid Analysys platform to download the report (if ready) through the ‘job id’ . with the name ‘Report_{sha256}_Enviroment.txt’.

In the Reports folder there are all the reports generated by the Hybrid analysis platform, through the script ‘Get_MitreInfo_from_Report.py’. we extract all the Mitre techniques present in the report by generating a list of tecnique ids in a file called Mitre_{sha256}_enviroment.txt’ saved in the Mitre_Signatures folder.

At the next stage, the ‘Mitre_Analyzer.py’ script intervenes, which, using the list of techniques identified as useful and reported in the ‘EquivocalTecnics.txt’ file, generates a new file called ‘EQUIVOCAL_Tecnics_{sha256}_{enviroment}.txt’ for every file in the folder "Mitre_signatures" and saves it in the Equivocal_Tecnics folder.

Finally, the ‘Generate_Equivocal_behaviours.py’ script, analysing each file containing the list of filtered techniques, generates a file containing the Equivocal Behaviours, using the mapping of the ‘EquivocalBehaviours.txt’ file (a json that allows the individual behaviours to be associated with its own list of techniques). The generated files with the name ‘Equivocal_Behaviours_{sha256}_enviroment.txt’ end up in the ‘Equivocal_Behaviours’ folder.

## Dataset

The files "list_sta_malware.txt" and "list_sha_trusted" are the list of the sha codes used for the results section of paper.

## Dependences
The project was written in python 3.10 using the following mandatory libreries:
 
1)colorama	0.4.6
2)requests	2.32.2


