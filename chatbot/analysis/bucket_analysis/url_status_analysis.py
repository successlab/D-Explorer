import re
from urllib.parse import urlparse

def extract_unique_domains_with_status_from_file(input_file, output_file="domain_statuses.txt"):
    """
    Reads URLs and statuses from an input text file, extracts unique domain-status
    pairs, and writes the results to an output text file.

    Args:
        input_file (str): Path to the input text file.
        output_file (str): Path to the output text file.
    """

    unique_pairs = set()
    results = []

    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            for line in infile:
                item = line.strip()  # Remove leading/trailing whitespace
                parts = item.split(" - ")
                if len(parts) >= 2:
                    url = parts[0].strip()
                    status = " - ".join(parts[1:]).strip()  # Handle multiple " - "
                    try:
                        parsed_url = urlparse(url)
                        domain = parsed_url.netloc
                        if domain:
                            pair = (domain, status)
                            if pair not in unique_pairs:
                                unique_pairs.add(pair)
                                results.append(pair)
                    except ValueError:
                        print(f"Invalid URL: {url}")

        with open(output_file, 'w', encoding='utf-8') as outfile:
            for domain, status in results:
                outfile.write(f"Domain: {domain}, Status: {status}\n")
        print(f"Results written to {output_file}")

    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Example usage:
input_file_path = "access_results_2.txt"  # Replace with your input file name

extract_unique_domains_with_status_from_file(input_file_path)