import requests
import os
from requests.exceptions import ChunkedEncodingError, ConnectionError, ReadTimeout

def check_url_access(input_file, output_file="fultered_url_analysis.txt"):
    """
    Reads URLs from a text file, checks their access status, and writes the
    results to an output text file. Handles infinite streams.

    Args:
        input_file (str): Path to the input text file containing URLs.
        output_file (str): Path to the output text file to write access results.
    """

    results = []

    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            for line in infile:
                url = line.strip()
                if url:  # check for blank lines
                    try:
                        response = requests.get(url, stream=True, timeout=(5, 10))  # stream=True
                        print(f"Checking: {url}") #print the url being checked
                        if response.status_code == 200:
                            # Check if the content is chunked and handle potential hangs
                            try:
                                # Attempt to read a small chunk to see if it hangs
                                chunk = next(response.iter_content(chunk_size=1024)) #1kb chunk
                                results.append(f"{url} - Success (200)")
                            except (StopIteration, ChunkedEncodingError): #stream ended normally or chunked encoding problem.
                                results.append(f"{url} - Success (200)")
                            except ReadTimeout:
                                results.append(f"{url} - Success (200) - Stream Timeout")
                            except ConnectionError:
                                results.append(f"{url} - Success (200) - Connection Error during stream")
                            except Exception as e:
                                results.append(f"{url} - Success (200) - Stream Error: {e}")

                        elif response.status_code == 403:
                            results.append(f"{url} - Forbidden (403)")
                        elif response.status_code == 404:
                            results.append(f"{url} - Not Found (404)")
                        else:
                            results.append(f"{url} - Status Code: {response.status_code}")

                    except requests.exceptions.RequestException as e:
                        results.append(f"{url} - Error: {e}")
                    except Exception as e:
                        results.append(f"{url} - Unexpected Error: {e}")

        with open(output_file, 'w', encoding='utf-8') as outfile:
            for result in results:
                outfile.write(result + '\n')

        print(f"URL access results written to {output_file}")

    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Example usage:
input_file_path = 'filtered_url_results.txt'  # Replace with your input file path
check_url_access(input_file_path)