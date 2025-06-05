import re

def count_pii_types(input_file, output_file="pii_counts.txt", threshold=0.6):
    """
    Counts PII types from an input file, filtering by score, and writes the results to an output file.

    Args:
        input_file (str): Path to the input file.
        output_file (str): Path to the output file.
        threshold (float): Minimum score for PII to be counted.
    """

    pii_counts = {}

    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            for line in infile:
                if "PII:" in line:
                    pii_entries = re.findall(r"type: (\w+),.*?score: (\d+\.\d+)", line)
                    for pii_type, score_str in pii_entries:
                        score = float(score_str)
                        if score >= threshold:
                            pii_counts[pii_type] = pii_counts.get(pii_type, 0) + 1

        with open(output_file, 'w', encoding='utf-8') as outfile:
            for pii_type, count in sorted(pii_counts.items()):
                outfile.write(f"{pii_type}: {count}\n")

        print(f"PII type counts written to {output_file}")

    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
input_file_path = 'presidio_results.txt'  # Replace with your input file path
count_pii_types(input_file_path)