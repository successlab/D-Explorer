import re

def filter_urls(input_file, output_file):
    """
    Reads URLs from an input text file, filters out specific URLs, and writes the
    remaining URLs to an output text file.

    Args:
        input_file (str): Path to the input text file containing URLs.
        output_file (str): Path to the output text file to write filtered URLs.
    """

    try:
        with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
            for line in infile:
                url = line.strip()  # Remove leading/trailing whitespace
                if url: #check for blank lines
                    if not (re.search(r'developer\.amazon\.com', url, re.IGNORECASE) or
                            re.search(r'tts\.alexa\.amazon', url, re.IGNORECASE) or
                            re.search(r'CAPS-SSE', url, re.IGNORECASE)):
                        outfile.write(url + '\n')

    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
input_file_path = 'url_results.txt'  # Replace with your input file path
output_file_path = 'filtered_url_results.txt' # Replace with your desired output file path
filter_urls(input_file_path, output_file_path)

print(f"Filtered URLs written to {output_file_path}")