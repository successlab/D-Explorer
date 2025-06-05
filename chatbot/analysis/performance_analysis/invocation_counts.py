import os
import csv

def count_line_occurrences(root_dir, output_csv="invocation_counts.csv"):
    """
    Traverses a nested directory tree, counts line occurrences in .txt files,
    and writes the results to a CSV file.

    Args:
        root_dir: The root directory to start the search from.
        output_csv: The name of the CSV file to write the results to.
    """
    line_count_occurrences = {}

    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".txt"):
                filepath = os.path.join(dirpath, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        line_count = len(lines)
                        line_count_occurrences[line_count] = line_count_occurrences.get(line_count, 0) + 1
                except FileNotFoundError:
                    print(f"File not found: {filepath}")
                except PermissionError:
                    print(f"Permission denied: {filepath}")
                except UnicodeDecodeError:
                    print(f"Unicode decode error: {filepath}. Trying latin-1 encoding.")
                    try:
                        with open(filepath, 'r', encoding='latin-1') as f:
                            lines = f.readlines()
                            line_count = len(lines)
                            line_count_occurrences[line_count] = line_count_occurrences.get(line_count, 0) + 1
                    except:
                        print(f"Latin-1 decode also failed: {filepath}")

    # Write results to CSV
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Line Count", "File Occurrences"])
        for count, occurrences in sorted(line_count_occurrences.items()):
            writer.writerow([count, occurrences])

    print(f"Line count occurrences written to {output_csv}")

# Example usage:
root_directory = "../../invocations"  # Replace with the actual directory path if necessary
count_line_occurrences(root_directory)