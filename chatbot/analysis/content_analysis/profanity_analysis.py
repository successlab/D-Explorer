import os
import fnmatch
from profanity_check import predict, predict_prob

def find_profanity(directory, file_pattern="*.txt"):
    """
    Searches text files within a directory tree for profanity using profanity-check.

    Args:
        directory (str): The root directory to search.
        file_pattern (str): The file pattern to match (e.g., "*.txt").

    Returns:
        dict: A dictionary where keys are file paths and values are lists of
              lines containing profanity.
    """

    profanity_occurrences = {}

    for root, _, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, file_pattern):
            file_path = os.path.join(root, filename)
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()
                    profane_lines = []
                    for i, line in enumerate(lines):
                        if predict([line])[0] == 1:  # Check if the line is predicted as profane
                            profane_lines.append(f"Line {i + 1}: {line.strip()}")
                    if profane_lines:
                        profanity_occurrences[file_path] = profane_lines
            except FileNotFoundError:
                print(f"File not found: {file_path}")
            except Exception as e:
                print(f"Error processing {file_path}: {e}")

    return profanity_occurrences

def write_profanity_results(occurrences, output_file="profanity_analysis.txt"):
    """
    Writes the profanity detection results to a text file.

    Args:
        occurrences (dict): The dictionary of profanity occurrences.
        output_file (str): The name of the output file.
    """

    with open(output_file, "w", encoding="utf-8") as f:
        if occurrences:
            for file_path, lines in occurrences.items():
                f.write(f"Profanity found in: {file_path}\n")
                for line in lines:
                    f.write(f"  - {line}\n")
        else:
            f.write("No profanity found in the specified directory.\n")

directory_path = "./alexa_chat_results"  # Replace with your directory path
file_pattern = "*.txt"

occurrences = find_profanity(directory_path, file_pattern)
write_profanity_results(occurrences)

print(f"Results written to profanity_analysis.txt")