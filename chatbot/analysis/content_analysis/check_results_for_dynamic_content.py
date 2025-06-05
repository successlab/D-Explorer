import re
import os

def count_dynamic_content_sets(filepath, keywords, matched_files, print_matches=False):
    """
    Counts the number of conversation file name sets in a text file that contain at least one match to the dynamic keyword list.
    Handles "Dynamic content", "Profanity found", "Inappropriate content", "PII or financial information found", and "PII found in:" file types.
    Optionally prints the lines containing matches.

    Args:
        filepath (str): Path to the input text file.
        keywords (list): List of dynamic keyword regular expression patterns.
        matched_files (set): Set to store matching file names.
        print_matches (bool): If True, prints the lines containing matches.

    Returns:
        int: Number of conversation file name sets with at least one match.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return 0
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        return 0

    delimiters = [
        "Dynamic content found in: ",
        "Profanity found in: ",
        "Inappropriate content found in: ",
        "PII or financial information found in: ",
        "PII found in:"
    ]

    total_file_set = set()
    sets = []
    for delimiter in delimiters:
        if delimiter in content:
            parts = content.split(delimiter)
            for part in parts[1:]:
                sets.append(delimiter + part)  # Include the delimiter in the set

    count = 0
    for file_set in sets:
        found_match = False
        if os.path.basename(filepath).startswith("inapp_content.txt"): #skip regex checks if file starts with inap_content.txt
            found_match = True
            match = re.search(r"(\.\./\.\./|\./)alexa_chat_results/.*/(.*_results\.txt)", file_set)
            if match:
                matched_files.add(match.group(2))
            if print_matches:
                print(file_set.strip())

        else:
            for keyword_pattern in keywords:
                if re.search(keyword_pattern, file_set, re.IGNORECASE):
                    found_match = True
                    match = re.search(r"(\.\./\.\./|\./)alexa_chat_results/.*/(.*_results\.txt)", file_set)
                    if match:
                        matched_files.add(match.group(2))
                    if print_matches:
                        print(file_set.strip())
                    break
        if found_match:
            count += 1
    return count

def main():
    keywords = [
        r"(https?://\S+)",
        r"www\.\S+",
        r"\b(website|web site|webpage|web page|url|blog|rss feed|podcast|online article|news feed|web link)\b",
        r"\b(dot com|dot org|dot net|dot edu|dot gov|dot io)\b",
        r"\b(click here|visit this site|go to this page|check out this link)\b",
        r"\b(weather|score|news|traffic|stock|updates?)\b",
        r"\b(random|generate|different|variable|changes?|updates?)\b",
        r"\b(depending on|based on|what happens|context|user)\b",
        r"\b(live|real-time|up-to-date| this week| of the week)\b",
        r"\b(personalized|customized)\b",
        r"\b(as of|at the moment)\b",
        r"(\d{1,2}:\d{2}(?::\d{2})?\s*(?:AM|PM|am|pm))",
        r"(\d{4}-\d{2}-\d{2})",
        r"(\d{1,2}/\d{1,2}/\d{4})",
        r"(\d{1,2}/\d{1,2}/\d{2})",
        r"\b(stored data|saved data|database|history|previous|record|log)\b",
        r"\b(radio station|live stream|audio stream|play music|listen to|tune in)\b",
        # Account Specific Patterns
        r"\b(what is your name|address|phone number|email|ssn|social security|dob|date of birth|birthday)\b",
    ]
    matched_files = set()

    filepath = "pii_financial_info.txt"
    count = count_dynamic_content_sets(filepath, keywords, matched_files, print_matches=False)
    print(f"Number of sets from {filepath} with at least one dynamic keyword match: {count}")

    filepath = "inapp_content.txt"
    count = count_dynamic_content_sets(filepath, keywords, matched_files, print_matches=False)
    print(f"Number of sets from {filepath} with at least one dynamic keyword match: {count}")

    filepath = "presidio_results_request_only.txt"
    count = count_dynamic_content_sets(filepath, keywords, matched_files, print_matches=True)
    print(f"Number of sets from {filepath} with at least one dynamic keyword match: {count}")

    filepath = "profanity_analysis.txt"
    count = count_dynamic_content_sets(filepath, keywords, matched_files, print_matches=False)
    print(f"Number of sets from {filepath} with at least one dynamic keyword match: {count}")

    print(f"\nNumber of unique matching files: {len(matched_files)}")

if __name__ == "__main__":
    main()