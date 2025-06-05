import os
import fnmatch
from detoxify import Detoxify

def find_inappropriate_content(directory, file_pattern="*.txt", output_file="detoxify_content.txt", threshold=0.5):
    """
    Searches text files within a directory tree for inappropriate content using the unbiased Detoxify model.
    Not used due to significant overhead.

    Args:
        directory (str): The root directory to search.
        file_pattern (str): The file pattern to match (e.g., "*.txt").
        output_file (str): The name of the output file.
        threshold (float): The probability threshold for classifying content as toxic.
    """

    inappropriate_occurrences = {}
    model = Detoxify('unbiased')  # Use the unbiased model

    for root, _, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, file_pattern):
            file_path = os.path.join(root, filename)
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()
                    inappropriate_lines = []
                    for i, line in enumerate(lines):
                        results = model.predict(line)
                        toxicity_score = results['toxicity']  # Access toxicity score
                        if toxicity_score > threshold:
                            inappropriate_lines.append(f"Line {i + 1}: {line.strip()} (Toxicity Score: {toxicity_score:.4f})") #report toxicity score.
                    if inappropriate_lines:
                        inappropriate_occurrences[file_path] = inappropriate_lines
            except FileNotFoundError:
                print(f"File not found: {file_path}")
            except Exception as e:
                print(f"Error processing {file_path}: {e}")

    with open(output_file, "w", encoding="utf-8") as outfile:
        if inappropriate_occurrences:
            for file_path, lines in inappropriate_occurrences.items():
                outfile.write(f"Inappropriate content found in: {file_path}\n")
                for line in lines:
                    outfile.write(f"  - {line}\n")
        else:
            outfile.write("No inappropriate content found in the specified directory.\n")

directory_path = "./alexa_chat_results"  # Replace with your directory path
find_inappropriate_content(directory_path)

print(f"Results written to detoxify_content.txt")