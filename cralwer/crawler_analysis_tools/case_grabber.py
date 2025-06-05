"This skill randomly grabs skill metadata for case studies. Not used."
import random

def choose_random_lines(filepath, num_lines=10):
    """
    Chooses a specified number of random lines from a text file.

    Args:
        filepath (str): The path to the text file.
        num_lines (int): The number of random lines to choose. Defaults to 10.

    Returns:
        list: A list of randomly selected lines, or None if an error occurs.
    """
    try:
        with open(filepath, 'r') as file:
            lines = file.readlines()

        if not lines:
            print("The file is empty.")
            return []

        num_lines = min(num_lines, len(lines))  # Ensure we don't try to select more lines than exist
        random_lines = random.sample(lines, num_lines)
        return random_lines

    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

# Example usage:
filepath = 'terms_file_names.txt'  # Replace with your file path
selected_lines = choose_random_lines(filepath)

if selected_lines:
    for line in selected_lines:
        print(line.strip()) #remove trailing newlines