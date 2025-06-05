import os
import fnmatch
import re

def detect_dynamic_content(directory, file_pattern="*.txt", output_file="dynamic_content.txt"):
    """
    Detects dynamic content (websites, URLs, blogs, RSS feeds, stored data, time/dates, audio streams) in text files.
    Includes the matching pattern at the end of each matching line.

    Args:
        directory (str): The root directory to search.
        file_pattern (str): The file pattern to match (e.g., "*.txt").
        output_file (str): The name of the output file.
    """

    dynamic_content_occurrences = {}
    dynamic_content_patterns = [
        r"(https?://\S+)",  # URLs
        r"www\.\S+",  # URLs without http/https
        r"\b(website|web site|webpage|web page|url|blog|rss feed|podcast|online article|news feed|web link)\b", #keywords.
        r"\b(dot com|dot org|dot net|dot edu|dot gov|dot io)\b", # TLDs
        r"\b(click here|visit this site|go to this page|check out this link)\b", #call to actions
        r"\b(weather|score|news|traffic|stock|updates?)\b",  # Time/date/info
        r"\b(random|generate|different|variable|changes?|updates?)\b",  # Variability
        r"\b(depending on|based on|what happens|context|user)\b", #contextual/conditional
        r"\b(live|real-time|up-to-date| this week| of the week)\b", #Realtime data.
        r"\b(personalized|customized)\b", #personalized data.
        r"\b(as of|at the moment)\b", #Time sensitive.
        r"(\d{1,2}:\d{2}(?::\d{2})?\s*(?:AM|PM|am|pm))", #time formats
        r"(\d{4}-\d{2}-\d{2})", #date formats
        r"(\d{1,2}/\d{1,2}/\d{4})", #date formats
        r"(\d{1,2}/\d{1,2}/\d{2})", #date formats
        r"\b(stored data|saved data|database|history|previous|record|log)\b", #Stored Data
        r"\b(radio station|live stream|audio stream|play music|listen to|tune in)\b", #Audio Streams
        # Line here about specific dynamic content of our Alexa account. Removed for privacy reasons.
        r"\b(what is your name|address|phone number|email|ssn|social security|dob|date of birth|birthday)\b",
    ]

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

                    dynamic_lines = []
                    for i, line in enumerate(lines):
                        line_lower = line.lower()
                        for pattern in dynamic_content_patterns:
                            if re.search(pattern, line_lower):
                                dynamic_lines.append(f"Line {i + 1}: {line.strip()}")
                                break

                    if dynamic_lines:
                        dynamic_content_occurrences[file_path] = dynamic_lines
            except FileNotFoundError:
                print(f"File not found: {file_path}")
            except Exception as e:
                print(f"Error processing {file_path}: {e}")

    with open(output_file, "w", encoding="utf-8") as outfile:
        if dynamic_content_occurrences:
            for file_path, lines in dynamic_content_occurrences.items():
                outfile.write(f"Dynamic content found in: {file_path}\n")
                for line in lines:
                    outfile.write(f"  - {line}\n")
        else:
            outfile.write("No dynamic content found in the specified directory.\n")

# Example usage:
directory_path = "../../alexa_chat_results"  # Replace with your directory path
detect_dynamic_content(directory_path)

print(f"Results written to dynamic_content.txt")