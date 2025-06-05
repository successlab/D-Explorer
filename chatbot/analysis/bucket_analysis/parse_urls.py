import re
from urllib.parse import urlparse

def extract_domains_and_folders(input_file, domains_file, folders_file):
    """
    Extracts unique domains and top-level folders from URLs in an input text file.

    Args:
        input_file (str): Path to the input text file containing URLs.
        domains_file (str): Path to the output file for unique domains.
        folders_file (str): Path to the output file for top-level folders.
    """

    unique_domains = set()
    unique_folders = set()

    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            for line in infile:
                url = line.strip()
                if url:
                    parsed_url = urlparse(url)
                    if parsed_url.netloc:  # Check if netloc (domain) exists
                        domain = f"{parsed_url.scheme}://{parsed_url.netloc}"
                        unique_domains.add(domain)

                        path = parsed_url.path
                        if path:
                            parts = path.split('/')
                            if len(parts) > 1:
                                folder = f"{domain}/{parts[1]}" #grab the first folder
                                unique_folders.add(folder)

    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        return
    except Exception as e:
        print(f"An error occurred: {e}")
        return

    try:
        with open(domains_file, 'w', encoding='utf-8') as domains_outfile:
            for domain in sorted(unique_domains):
                domains_outfile.write(domain + '\n')

        with open(folders_file, 'w', encoding='utf-8') as folders_outfile:
            for folder in sorted(unique_folders):
                folders_outfile.write(folder + '\n')
    except Exception as e:
        print(f"An error occurred writing output files: {e}")
        return

    print(f"Unique domains written to {domains_file}")
    print(f"Top-level folders written to {folders_file}")

# Example usage:
input_file_path = 'filtered_url_results.txt'
domains_file_path = 'unique_domains.txt'
folders_file_path = 'top_level_folders.txt'

extract_domains_and_folders(input_file_path, domains_file_path, folders_file_path)