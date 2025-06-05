import re

def sort_file_by_number(filepath):
    """
    Sorts lines in a file by the number at the end of each line.

    Args:
        filepath (str): The path to the file.
    """
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()

        def get_number(line):
            """Extracts the number at the end of the line."""
            match = re.search(r':\s*(\d+)$', line)
            if match:
                return int(match.group(1))
            return 0  # Return 0 if no number is found (handle errors)

        sorted_lines = sorted(lines, key=get_number)

        for line in sorted_lines:
            print(line.strip())

    except FileNotFoundError:
        print(f"File not found: {filepath}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
file_path = "common_domain_counts.txt"  # Replace with your file path
sort_file_by_number(file_path)