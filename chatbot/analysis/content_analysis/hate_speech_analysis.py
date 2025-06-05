import os
import re
import fnmatch
from transformers import pipeline

def find_hate_speech_hateBERT(directory, file_pattern="*.txt"):
    """
    Finds hate speech occurrences in text files within a nested directory tree using HateBERT.

    Args:
        directory (str): The root directory to search.
        file_pattern (str): The file pattern to match (e.g., "*.txt").

    Returns:
        dict: A dictionary where keys are file paths and values are lists of
              lines containing hate speech.
    """

    hate_speech_occurrences = {}
    classifier = pipeline("text-classification", model="GroNLP/hateBERT")

    for root, _, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, file_pattern):
            file_path = os.path.join(root, filename)
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f: #added errors='ignore'
                    content = f.read()

                    url_index = content.find("URLs:")
                    if url_index != -1:
                        content = content[:url_index]

                    lines = content.splitlines()
                    hate_lines = []
                    for line in lines:
                        try:
                            result = classifier(line)
                            if result and result[0]['label'] == 'hate':
                                hate_lines.append(line)
                        except Exception as e:
                            print(f"Error classifying line: {line}, Error: {e}")
                            continue

                    if hate_lines:
                        hate_speech_occurrences[file_path] = hate_lines
            except FileNotFoundError:
                print(f"File not found: {file_path}")
            except Exception as e:
                print(f"Error processing {file_path}: {e}")

    return hate_speech_occurrences

def write_results_to_file(occurrences, output_file="hate_speech_analysis.txt"):
    """
    Writes the hate speech analysis results to a text file.

    Args:
        occurrences (dict): The dictionary of hate speech occurrences.
        output_file (str): The name of the output file.
    """

    with open(output_file, "w", encoding="utf-8") as f:
        if occurrences:
            for file_path, lines in occurrences.items(): #changed filename to filepath.
                f.write(f"Hate speech found in {file_path}:\n")
                for line in lines:
                    f.write(f"  - {line}\n")
        else:
            f.write("No hate speech found in the specified directory.\n")

directory_path = "./alexa_chat_results/"  # Replace with your directory path
file_pattern = "*.txt" # Added a file pattern.

occurrences = find_hate_speech_hateBERT(directory_path, file_pattern)
write_results_to_file(occurrences)

print(f"Results written to hate_speech_analysis.txt")