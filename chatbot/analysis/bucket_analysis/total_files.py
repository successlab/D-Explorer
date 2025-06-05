import os

def count_txt_files_per_directory(root_dir):
    """
    Counts the number of .txt files in each directory within a nested directory structure.

    Args:
        root_dir (str): The root directory to start the search from.

    Returns:
        dict: A dictionary where keys are directory paths and values are the counts of .txt files.
    """
    directory_txt_counts = {}

    for root, dirs, files in os.walk(root_dir):
        txt_count = 0
        for file in files:
            if file.endswith(".txt"):
                txt_count += 1
        directory_txt_counts[root] = txt_count

    return directory_txt_counts

def print_txt_counts(directory_txt_counts):
    """
    Prints the directory and its corresponding .txt file count.

    Args:
        directory_txt_counts (dict): A dictionary containing directory paths and .txt file counts.
    """
    for directory, count in directory_txt_counts.items():
        print(f"Directory: {directory}, .txt files: {count}")

# Example usage:
root_directory = "../../alexa_chat_results"  # Replace with the path to your root directory
txt_counts = count_txt_files_per_directory(root_directory)
print_txt_counts(txt_counts)