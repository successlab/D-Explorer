import os
import csv
import re

def process_directories(interaction_dir, invocation_dir, output_csv):
    """
    Processes interaction and invocation directories, counts unique requests per response between invocations,
    and writes the counts to a CSV. Loads the modified filename from interaction_dir into invocation_dir.
    Ignores commas and case.

    Args:
        interaction_dir (str): Path to the interaction directory.
        invocation_dir (str): Path to the invocation directory.
        output_csv (str): Path to the output CSV file.
    """

    response_counts = {}

    for dirpath, _, filenames in os.walk(interaction_dir):
        for filename in filenames:
            if filename.endswith("_results.txt"):
                interaction_filepath = os.path.join(dirpath, filename)
                invocation_filename = filename.replace("_results.txt", ".txt")
                invocation_filepath = os.path.join(invocation_dir, os.path.relpath(os.path.join(dirpath, invocation_filename), interaction_dir))

                if os.path.exists(invocation_filepath):
                    invocations = load_invocations(invocation_filepath)
                    counts = count_unique_requests_per_response(interaction_filepath, invocations)
                    for response, unique_count in counts.items():
                        if response not in response_counts:
                            response_counts[response] = {}
                        response_counts[response][unique_count] = response_counts[response].get(unique_count, 0) + 1

    write_counts_to_csv(response_counts, output_csv)

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

def count_unique_requests_per_response(interaction_filepath, invocations):
    """
    Counts unique requests per response between invocations in an interaction file. Ignores commas and case.

    Args:
        interaction_filepath (str): Path to the interaction file.
        invocations (list): List of invocations.

    Returns:
        dict: Dictionary of response and unique request counts.
    """
    response_request_counts = {}
    try:
        with open(interaction_filepath, "r") as f:
            lines = f.readlines()
            current_response = None
            unique_requests = set()
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
                            if type == "response":
                                if in_invocation_block and current_response is not None:
                                    response_request_counts[current_response] = len(unique_requests)
                                current_response = text
                                unique_requests = set()
                                in_invocation_block = True
                            elif type == "request" and in_invocation_block:
                                if invocations and invocation_index < len(invocations) and re.search(re.escape(invocations[invocation_index]), text, re.IGNORECASE):
                                    if current_response is not None:
                                        response_request_counts[current_response] = len(unique_requests)
                                    current_response = None
                                    unique_requests = set()
                                    invocation_index += 1
                                    in_invocation_block = False
                                else:
                                    unique_requests.add(text)
                    except (SyntaxError, TypeError, IndexError):
                        pass

            if in_invocation_block and current_response is not None:
                response_request_counts[current_response] = len(unique_requests)

        return response_request_counts

    except FileNotFoundError:
        print(f"File not found: {interaction_filepath}")
        return {}
    except Exception as e:
        print(f"Error processing {interaction_filepath}: {e}")
        return {}

def write_counts_to_csv(response_counts, output_csv):
    """
    Writes the response counts to a CSV file.

    Args:
        response_counts (dict): Dictionary of response and unique request counts.
        output_csv (str): Path to the output CSV file.
    """
    with open(output_csv, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Response", "Unique Request Count", "Occurrence"])
        for response, counts in response_counts.items():
            for unique_count, occurrence in sorted(counts.items()):
                writer.writerow([response, unique_count, occurrence])

# Example usage:
interaction_directory = "interaction_files"
invocation_directory = "invocation_files"
output_csv_file = "unique_request_counts.csv"
process_directories(interaction_directory, invocation_directory, output_csv_file)

print(f"Results written to {output_csv_file}")