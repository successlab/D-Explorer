import json
import os

def calculate_zero_review_percentage(directory, category="Health&Fitness"):
    """Calculates the percentage of files with reviewnum 0 in a given category.

    Args:
        directory: The root directory to search.
        category: The specific category to analyze (default: "Health&Fitness").

    Returns:
        The percentage of files with reviewnum 0, or None if the category is not found.
    """

    category_path = os.path.join(directory, category)
    if not os.path.exists(category_path):
        print(f"Category '{category}' not found in directory '{directory}'.")
        return None

    total_files = 0
    zero_review_files = 0

    for root, _, files in os.walk(category_path):  # Walk only within the specified category
        for file in files:
            if file.endswith(".json"):  # Only process JSON files. Add this check!
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f: #Handle encoding
                        data = json.load(f)
                        review_num = data.get("reviewnum")
                        skdetail = data.get("skdetail")
                        if skdetail:
                            if "flash briefing" not in skdetail.lower():
                                try:
                                    review_num = int(review_num.strip()) if review_num else 0 #Handle if reviewnum is null or empty string
                                except (ValueError, AttributeError):
                                    review_num = 0
                                total_files += 1
                                if review_num == 0:
                                    zero_review_files += 1

                except (json.JSONDecodeError, FileNotFoundError, UnicodeDecodeError) as e:
                    print(f"Error reading JSON file {file_path}: {e}")
                    continue  # Skip to the next file

    if total_files == 0:
        return 0  # Avoid division by zero

    percentage = (zero_review_files / total_files) * 100
    return percentage


# Example usage:
directory = "../crawler_2.0/result/"  # Replace with the path to your directory
percentage = calculate_zero_review_percentage(directory)

if percentage is not None:
    print(f"Percentage of files in Health&Fitness with reviewnum 0: {percentage:.2f}%")

directory = './invocations_20%/'  # Replace with the path to your directory
percentage = calculate_zero_review_percentage(directory)

if percentage is not None:
    print(f"Percentage of files in Health&Fitness with reviewnum 0: {percentage:.2f}%")