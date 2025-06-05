import os

def read_search_strings(filepath):
    """Reads search strings from a text file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        print(f"Search strings file not found: {filepath}")
        return set()
    except Exception as e:
        print(f"Error reading search strings file: {e}")
        return set()

def find_common_strings(root_dir, search_strings):
    """
    Finds strings from search_strings that are present in every text file within a nested directory.

    Args:
        root_dir (str): The root directory to search.
        search_strings (set): The set of strings to search for.

    Returns:
        set: A set of strings from search_strings that are common to all text files.
    """

    all_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith((".txt", ".text")):
                filepath = os.path.join(dirpath, filename)
                all_files.append(filepath)

    if not all_files:
        return set()

    string_counts = {string: 0 for string in search_strings}
    file_count = len(all_files)

    for filepath in all_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                current_strings = set(line.strip() for line in f)
                for search_string in search_strings:
                    if any(search_string in string for string in current_strings):
                        string_counts[search_string] += 1
                
        except FileNotFoundError:
            print(f"File not found: {filepath}")
            return set()
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            return set()

    string_counts
    return string_counts

def main():
    root_directory = "../../alexa_chat_results/"
    search_strings_file = "unique_domains.txt"

    search_strings = read_search_strings(search_strings_file)

    if not search_strings:
        print("No search strings found. Exiting.")
        return

    common_strings = find_common_strings(root_directory, search_strings)

    if common_strings:
        print("Strings from search file common to all text files:")
        for key, value in common_strings.items():
            print(f"{key}: {value}")
    else:
        print("No common strings found or no text files were found.")

if __name__ == "__main__":
    main()