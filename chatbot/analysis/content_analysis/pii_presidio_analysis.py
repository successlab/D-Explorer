import os
import fnmatch
from presidio_analyzer import AnalyzerEngine, PatternRecognizer
from presidio_anonymizer import AnonymizerEngine

def find_pii_presidio(directory, file_pattern="*.txt", output_file="presidio_results_request_only.txt"):
    """
    Detects PII using Presidio in text files within a directory tree, only including results with a score of 0.85 or above.

    Args:
        directory (str): The root directory to search.
        file_pattern (str): The file pattern to match (e.g., "*.txt").
        output_file (str): The name of the output file.
    """

    pii_occurrences = {}
    analyzer = AnalyzerEngine()
    anonymizer = AnonymizerEngine() #used for anonymization, if needed.

    for root, _, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, file_pattern):
            file_path = os.path.join(root, filename)
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    url_index = content.find("URLs:")
                    if url_index != -1:
                        content = content[:url_index]
                    lines = content.splitlines()

                    pii_lines = []
                    for i, line in enumerate(lines):
                        if not "'response'" in line:
                            results = analyzer.analyze(text=line, language='en')
                            if results:
                                filtered_results = [result for result in results if result.score >= 1.0]
                                if filtered_results:
                                    pii_lines.append(f"Line {i + 1}: {line.strip()} - PII: {filtered_results}")

                    if pii_lines:
                        pii_occurrences[file_path] = pii_lines
            except FileNotFoundError:
                print(f"File not found: {file_path}")
            except Exception as e:
                print(f"Error processing {file_path}: {e}")

    with open(output_file, "w", encoding="utf-8") as outfile:
        if pii_occurrences:
            for file_path, lines in pii_occurrences.items():
                outfile.write(f"PII found in: {file_path}\n")
                for line in lines:
                    outfile.write(f"  - {line}\n")
        else:
            outfile.write("No PII found with a score of 0.85 or above in the specified directory.\n")

directory_path = "../../alexa_chat_results"  # Replace with your directory path
find_pii_presidio(directory_path)

print(f"Results written to presidio_results.txt")