"File percentage counter. Used to determine chatbot coverage."
import os
from collections import defaultdict

def count_files_and_calculate_percentages(root_dir_1, root_dir_2):
    """
    Counts unique files, excluding "flash briefing" files, and calculates percentages.
    """

    file_counts_1 = defaultdict(int)
    file_counts_2 = defaultdict(int)
    seen_files_1 = set()
    seen_files_2 = set()

    def is_flash_briefing(filepath):
        """Checks if a file contains the phrase "flash briefing" (case-insensitive)."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:  # Handle encoding
                content = f.read()
                return "flash briefing" in content.lower()  # Case-insensitive check
        except UnicodeDecodeError:
            print(f"Skipping file {filepath} due to encoding error.")
            return False  # Treat as not a flash briefing if encoding error
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            return False

    try:
        for dirpath, _, filenames in os.walk(root_dir_1):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                if filepath not in seen_files_1 and not is_flash_briefing(filepath):
                    seen_files_1.add(filepath)
                    category = os.path.basename(dirpath)
                    file_counts_1[category] += 1

        for dirpath, _, filenames in os.walk(root_dir_2):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                if filepath not in seen_files_2 and not is_flash_briefing(filepath):
                    seen_files_2.add(filepath)
                    category = os.path.basename(dirpath)
                    file_counts_2[category] += 1

        # ... (rest of your code)

        for category in set(file_counts_1.keys()).union(file_counts_2.keys()):
            count1 = file_counts_1.get(category, 0)
            count2 = file_counts_2.get(category, 0)

            if count2 > 0:  # Avoid division by zero
                percentage = (count1 / count2) * 100
            else:
                percentage = 0  # Or handle as you see fit

            print(f"Category: {category}, Dir1 Count: {count1}, Dir2 Count: {count2}, Percentage: {percentage:.1f}%")


    except FileNotFoundError:
        print("One or both directories not found.")
    except PermissionError:
        print("Permission denied accessing one or both directories.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# Example usage:
root_directory_1 = './invocations/'
root_directory_2 = '../../chatbot/alexa_chat_results/'
count_files_and_calculate_percentages(root_directory_2, root_directory_1)