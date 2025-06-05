import os
import fnmatch
import re

def find_inappropriate_content(directory, file_pattern="*.txt", output_file="inapp_content.txt"):
    """
    Searches text files within a directory tree for inappropriate (sexual) content,
    ignoring lines after "URLs:".

    Args:
        directory (str): The root directory to search.
        file_pattern (str): The file pattern to match (e.g., "*.txt").
        output_file (str): The name of the output file.
    """

    inappropriate_occurrences = {}
    inappropriate_words = [
        r"\b(sex|sexual|porn|nude|naked|erotic|orgasm|masturbat|intercourse|genital|vagina|penis|clitoris|testicle|boobs|tits|ass|butt|cock|dick|pussy|whore|slut|bitch|fuck|cunt)\b",
        r"\b(hentai|yaoi|yuri|ecchi)\b",
        r"(18\+|nsfw|xxx)",
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

                    inappropriate_lines = []
                    for i, line in enumerate(lines):
                        line_lower = line.lower()
                        for pattern in inappropriate_words:
                            if re.search(pattern, line_lower):
                                inappropriate_lines.append(f"Line {i + 1}: {line.strip()}")
                                break

                    if inappropriate_lines:
                        inappropriate_occurrences[file_path] = inappropriate_lines
            except FileNotFoundError:
                print(f"File not found: {file_path}")
            except Exception as e:
                print(f"Error processing {file_path}: {e}")

    with open(output_file, "w", encoding="utf-8") as outfile:
        if inappropriate_occurrences:
            for file_path, lines in inappropriate_occurrences.items():
                outfile.write(f"Inappropriate content found in: {file_path}\n")
                for line in lines:
                    outfile.write(f"  - {line}\n")
        else:
            outfile.write("No inappropriate content found in the specified directory.\n")

directory_path = "./alexa_chat_results"  # Replace with your directory path
find_inappropriate_content(directory_path)

print(f"Results written to inapp_content.txt")