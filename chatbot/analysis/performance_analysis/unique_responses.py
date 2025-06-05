import os
import csv

def process_directory(root_dir, output_csv):
    """
    Processes a directory tree, counts unique responses, and writes to a CSV.

    Args:
        root_dir (str): The root directory to start processing.
        output_csv (str): The output CSV file path.
    """

    file_counts = {}  # Dictionary to store file counts for each unique response count

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".txt"):  # Assuming text files
                filepath = os.path.join(dirpath, filename)
                unique_responses = count_unique_responses(filepath)
                if unique_responses is not None:
                    count = len(unique_responses)
                    file_counts[count] = file_counts.get(count, 0) + 1

    write_to_csv(file_counts, output_csv)

def count_unique_responses(filepath):
    """
    Counts unique responses in a file.

    Args:
        filepath (str): The path to the file.

    Returns:
        set: A set of unique responses, or None if an error occurs.
    """
    unique_responses = set()
    try:
        with open(filepath, "r") as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if line.startswith("["):
                    try:
                        line = eval(line)  # Safely evaluate the list
                        if len(line) == 2 and line[1] == "response":
                            unique_responses.add(line[0])
                    except (SyntaxError, TypeError, IndexError):
                        # Handle potential issues with malformed lines.
                        pass

                elif line.startswith("URLs:"):
                  break #Stop parsing when urls are found.
        return unique_responses

    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return None
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return None

def write_to_csv(file_counts, output_csv):
    """
    Writes the file counts to a CSV file.

    Args:
        file_counts (dict): A dictionary of unique response counts and file counts.
        output_csv (str): The output CSV file path.
    """
    with open(output_csv, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Unique Responses", "File Count"])
        for count, file_count in sorted(file_counts.items()):
            writer.writerow([count, file_count])

# Example usage:
root_directory = "../../alexa_chat_results"  # Replace with your directory
output_csv_file = "response_counts.csv"
process_directory(root_directory, output_csv_file)

print(f"Results written to {output_csv_file}")