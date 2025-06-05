import os
import fnmatch
import re

def find_pii_financial_info(directory, file_pattern="*.txt", output_file="pii_financial_info.txt"):
    """
    Searches text files within a directory tree for PII or financial information requests and classifies them.
    Excludes lines containing "Alexa app" (case-insensitive).

    Args:
        directory (str): The root directory to search.
        file_pattern (str): The file pattern to match (e.g., "*.txt").
        output_file (str): The name of the output file.
    """

    pii_financial_occurrences = {}
    pii_financial_patterns = {
        "Contact information": r"\b(what is your name|phone number|email|ssn|social security|dob|date of birth|birthday)\b",
        "Date of birth": r"\b(what is your dob|date of birth|birthday)\b",
        "Location information": r"\b(what is your location|address|p)\b",
        "SSN": r"\b(ssn|social security)\b",
        "Financial information": r"\b(credit card|debit card|bank account|routing number|account number)\b",
        "Login information": r"\b(password|security code)\b",
        "Personal Info": r"\b(my personal|my financial)\b",
        "Financial Action": r"\b(pay my|transfer funds|check my balance|what is my balance|buy stock|sell stock|buy crypto|sell crypto)\b",
        "Likely Address": r"\d{1,5}\s+[a-zA-Z]+\s+(?:st|ave|rd|dr|ln|blvd)\b",
        "Zip Code": r"\b\d{5}(?:-\d{4})?\b",
        "Credit Card Number": r"\b(?:\d{4}[- ]){3}\d{4}\b",
        "Phone Number": r"\b(?:\d{3}[-.\s]?)?\d{3}[-.\s]?\d{4}\b",
        "Social Security Number": r"\b\d{3}-\d{2}-\d{4}\b",
        # Lines containing data specific to our Alexa account, including name, address, phone number, and credit card.
    }

    for root, _, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, file_pattern):
            file_path = os.path.join(root, filename)
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    url_index = content.find("URLs:")
                    if url_index != -1:
                        content = content[:url_index]
                    lines = content.splitlines()

                    pii_financial_lines = []
                    for i, line in enumerate(lines):
                        line_lower = line.lower()
                        if "alexa app" in line_lower:
                            continue # Skip lines containing "alexa app"
                        for pii_type, pattern in pii_financial_patterns.items():
                            if re.search(pattern, line_lower):
                                pii_financial_lines.append(f"Line {i + 1}: {line.strip()} - Type: {pii_type}")
                                break  # Found a match, move to the next line

                    if pii_financial_lines:
                        pii_financial_occurrences[file_path] = pii_financial_lines
            except FileNotFoundError:
                print(f"File not found: {file_path}")
            except Exception as e:
                print(f"Error processing {file_path}: {e}")

    with open(output_file, "w", encoding="utf-8") as outfile:
        if pii_financial_occurrences:
            for file_path, lines in pii_financial_occurrences.items():
                outfile.write(f"PII or financial information found in: {file_path}\n")
                for line in lines:
                    outfile.write(f"  - {line}\n")
        else:
            outfile.write("No PII or financial information found in the specified directory.\n")

# Example usage:
directory_path = "../../alexa_chat_results"  # Replace with your directory path
find_pii_financial_info(directory_path)

print(f"Results written to pii_financial_info_labeled_2.txt")