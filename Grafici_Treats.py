import os
import json
import matplotlib.pyplot as plt
import numpy as np


def load_behaviour_mapping(file_path="EquivocalBehaviours.txt"):
    """Load the mapping between extended behaviour names and ESB labels from a JSON file."""
    with open(file_path, "r") as file:
        behaviour_data = json.load(file)

    return {k: f"ESB{i + 1}" for i, k in enumerate(behaviour_data.keys())}


def count_equivocal_behaviours(folder, behaviour_mapping):
    """Count the occurrences of each Equivocal Behaviour in a folder."""
    behaviour_counts = {key: 0 for key in behaviour_mapping.values()}
    total_files = 0

    for file_name in os.listdir(folder):
        file_path = os.path.join(folder, file_name)
        total_files += 1

        with open(file_path, 'r') as file:
            behaviours = set(file.read().splitlines()[1:])  # Skip the first description line
            for behaviour in behaviours:
                mapped_behaviour = behaviour_mapping.get(behaviour, None)
                if mapped_behaviour:
                    behaviour_counts[mapped_behaviour] += 1

    # Convert to percentage
    behaviour_percentages = {k: (v / total_files) * 100 for k, v in behaviour_counts.items()}
    return behaviour_percentages


def plot_equivocal_behaviours(mac_good, mac_mal, linux_good, linux_mal, behaviour_mapping):
    """Generate and save bar charts for Mac and Linux environments with Y-axis scaled above 100% for clarity."""
    behaviours = list(behaviour_mapping.values())  # Ensure labels are ESB1, ESB2, ...
    x = np.arange(len(behaviours))
    width = 0.4  # Bar width

    colors = {'Malware': '#E69F00', 'Trusted': '#666666'}

    # Set Y-axis limit slightly above 100% for clarity
    max_value = 110

    def style_plot(ax, title):
        ax.set_xlabel('Equivocal Behaviours')
        ax.set_ylabel('Percentage (%)')
        ax.set_title(title)
        ax.set_xticks(x)
        ax.set_xticklabels(behaviours, rotation=45, ha="right")
        ax.set_ylim(0, max_value)
        ax.legend()
        ax.grid(axis='y', linestyle='--', linewidth=0.7, alpha=0.7)
        plt.tight_layout()

    # Mac environment chart
    fig, ax = plt.subplots()
    ax.bar(x - width / 2, [mac_mal.get(b, 0) for b in behaviours], width, label='Malware', color=colors['Malware'])
    ax.bar(x + width / 2, [mac_good.get(b, 0) for b in behaviours], width, label='Trusted', color=colors['Trusted'])
    style_plot(ax, 'Equivocal Behaviours Distribution in Mac Environment')
    plt.savefig("Equivocal_Behaviours_Mac.jpg")
    plt.close()

    # Linux environment chart
    fig, ax = plt.subplots()
    ax.bar(x - width / 2, [linux_mal.get(b, 0) for b in behaviours], width, label='Malware', color=colors['Malware'])
    ax.bar(x + width / 2, [linux_good.get(b, 0) for b in behaviours], width, label='Trusted', color=colors['Trusted'])
    style_plot(ax, 'Equivocal Behaviours Distribution in Linux Environment')
    plt.savefig("Equivocal_Behaviours_Linux.jpg")
    plt.close()


def main():
    behaviour_mapping = load_behaviour_mapping()

    folders = {
        "MAC_Goodware": "Equivocal_Behaviours_MAC_Goodware",
        "MAC_Malware": "Equivocal_Behaviours_MAC_Malware",
        "Linux_Goodware": "Equivocal_Behaviours_Linux_Goodware",
        "Linux_Malware": "Equivocal_Behaviours_Linux_Malware",
    }

    mac_good = count_equivocal_behaviours(folders["MAC_Goodware"], behaviour_mapping)
    mac_mal = count_equivocal_behaviours(folders["MAC_Malware"], behaviour_mapping)
    linux_good = count_equivocal_behaviours(folders["Linux_Goodware"], behaviour_mapping)
    linux_mal = count_equivocal_behaviours(folders["Linux_Malware"], behaviour_mapping)

    plot_equivocal_behaviours(mac_good, mac_mal, linux_good, linux_mal, behaviour_mapping)

    print("Analysis completed. Charts saved as Equivocal_Behaviours_Mac.jpg and Equivocal_Behaviours_Linux.jpg.")


if __name__ == "__main__":
    main()
