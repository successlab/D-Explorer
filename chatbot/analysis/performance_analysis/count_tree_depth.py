import os
import csv
import re

def process_directories(interaction_dir, invocation_dir, output_csv):
    """
    Processes interaction and invocation directories, counts max tree depth per file,
    and writes the counts to a CSV. Loads the modified filename from interaction_dir into invocation_dir.
    Ignores commas and case.

    Args:
        interaction_dir (str): Path to the interaction directory.
        invocation_dir (str): Path to the invocation directory.
        output_csv (str): Path to the output CSV file.
    """

    max_depth_counts = {}

    for dirpath, _, filenames in os.walk(interaction_dir):
        for filename in filenames:
            if filename.endswith("_results.txt"):
                interaction_filepath = os.path.join(dirpath, filename)
                invocation_filename = filename.replace("_results.txt", ".txt")
                invocation_filepath = os.path.join(invocation_dir, os.path.relpath(os.path.join(dirpath, invocation_filename), interaction_dir))

                if os.path.exists(invocation_filepath):
                    invocations = load_invocations(invocation_filepath)
                    counts = count_responses_between_invocations(interaction_filepath, invocations)
                    if counts:
                        max_depth = max(counts)
                        max_depth_counts[max_depth] = max_depth_counts.get(max_depth, 0) + 1
                    else:
                        max_depth_counts[0] = max_depth_counts.get(0, 0) +1 #add 0 if there are no counts.

    write_counts_to_csv(max_depth_counts, output_csv)

def load_invocations(filepath):
    """
    Loads invocations from a file into a list. Ignores commas and case.

    Args:
        filepath (str): Path to the invocation file.

    Returns:
        list: List of invocations.
    """
    invocations = []
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip().lower().replace(",", "")
            invocations.append(line)
    return invocations

def count_responses_between_invocations(interaction_filepath, invocations):
    """
    Counts responses between invocations in an interaction file. Ignores commas and case.

    Args:
        interaction_filepath (str): Path to the interaction file.
        invocations (list): List of invocations.

    Returns:
        list: List of response counts between invocations.
    """
    response_counts = []
    try:
        with open(interaction_filepath, "r") as f:
            lines = f.readlines()
            current_count = 0
            in_invocation_block = False
            invocation_index = 0

            for line in lines:
                line = line.strip()

                if line.startswith("URLs:"):
                    break

                if line.startswith("["):
                    try:
                        line_list = eval(line)
                        if len(line_list) == 2:
                            text, type = line_list
                            text = text.lower().replace(",", "")
                            if type == "request":
                                if invocations and invocation_index < len(invocations) and re.search(re.escape(invocations[invocation_index]), text, re.IGNORECASE):
                                    if in_invocation_block:
                                        response_counts.append(current_count)
                                    current_count = 0
                                    in_invocation_block = True
                                    invocation_index += 1
                            elif type == "response" and in_invocation_block:
                                current_count += 1

                    except (SyntaxError, TypeError, IndexError):
                        pass

            if in_invocation_block:
                response_counts.append(current_count)

        return response_counts

    except FileNotFoundError:
        print(f"File not found: {interaction_filepath}")
        return []
    except Exception as e:
        print(f"Error processing {interaction_filepath}: {e}")
        return []

def write_counts_to_csv(max_depth_counts, output_csv):
    """
    Writes the max tree depth counts to a CSV file.

    Args:
        max_depth_counts (dict): Dictionary of max tree depth counts and their occurrences.
        output_csv (str): Path to the output CSV file.
    """
    with open(output_csv, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Max Tree Depth", "File Count"])
        for count, occurrence in sorted(max_depth_counts.items()):
            writer.writerow([count, occurrence])

# Example usage:
interaction_directory = "../../alexa_chat_results"  # Replace with your interaction directory
invocation_directory = "../../invocations"  # Replace with your invocation directory
output_csv_file = "max_tree_depth_counts.csv"
process_directories(interaction_directory, invocation_directory, output_csv_file)

print(f"Results written to {output_csv_file}")