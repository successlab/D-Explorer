import os

def count_matching_files(root_dir, urls_file=None, urls_list=None):
    """
    Iterates through files in a nested directory and counts files that contain
    URLs from a list and/or the string "CAPS-SSE" separately.

    Args:
        root_dir (str): The root directory to start the search.
        urls_file (str, optional): Path to a file containing URLs (one per line).
        urls_list (list, optional): A list of URLs.

    Returns:
        tuple: (count_urls, count_caps_sse) - Counts of files matching URLs and "CAPS-SSE".
    """

    if urls_file and urls_list:
        raise ValueError("Either urls_file or urls_list should be provided, not both.")

    urls = []
    if urls_file:
        try:
            with open(urls_file, 'r', encoding='utf-8') as f:
                urls = [line.strip() for line in f]
        except FileNotFoundError:
            print(f"Error: URLs file '{urls_file}' not found.")
            return 0, 0
    elif urls_list:
        urls = urls_list

    count_urls = 0
    count_caps_sse = 0

    for root, _, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    file_content = f.read()

                    url_found = False
                    caps_sse_found = False

                    if "CAPS-SSE" in file_content: #changed to CAPS-SSE
                        count_caps_sse += 1
                        caps_sse_found = True

                    for url in urls:
                        if url in file_content:
                            count_urls += 1
                            url_found = True
                            break  # Move to the next file

                    #If both are true, increment both.
                    if caps_sse_found and not url_found:
                        pass #Do nothing, count_caps_sse already incremented.
                    elif url_found and not caps_sse_found:
                        pass #Do nothing, count_urls already incremented.
                    elif url_found and caps_sse_found:
                        pass #Do nothing, both were already incremented.
            except Exception as e:
                print(f"Error processing file '{file_path}': {e}")

    return count_urls, count_caps_sse

root_directory = "./alexa_chat_results"

urls_file_path = "filtered_url_results.txt"

count_urls_file, count_caps_sse_file = count_matching_files(root_directory, urls_file=urls_file_path)
print(f"Matching files (using URLs file): URLs={count_urls_file}, CAPS-SSE={count_caps_sse_file}")