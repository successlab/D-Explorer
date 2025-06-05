import os
import ast

def find_dangerous_instructions_from_files(root_directory):
    """
    Searches Alexa interaction text files in a nested directory structure for
    potentially dangerous instructions. Not used.

    Args:
        root_directory: The root directory containing the Alexa interaction files.

    Returns:
        A list of dangerous instructions found in the files, along with the file path.
    """

    dangerous_instructions_found = []
    dangerous_keywords = [
        " harm ",
        " hurt ",
        " kill ",
        " injure ",
        " self-destruct ",
        " destroy ",
        " explode ",
        " poison ",
        " suffocate ",
        " choke ",
        " burn ",
        " stab ",
        " cut ",
        " shoot ",
        " attack ",
        " die ",
        " suicide ",
        "self harm",
        "self-harm",
        "self harm",
        "take your life",
        " challenge "
    ]

    for root, _, files in os.walk(root_directory):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r") as f:
                        lines = f.readlines()
                        alexa_interactions = []
                        for line in lines:
                            line = line.strip()
                            if line:
                                try:
                                    interaction = ast.literal_eval(line)
                                    if isinstance(interaction, list) and all(isinstance(item, str) for item in interaction):
                                        alexa_interactions.append(interaction)
                                except (ValueError, SyntaxError):
                                    pass #ignore lines that are not lists of strings.

                    for interaction in alexa_interactions:
                        if len(interaction) == 2 and interaction[1].lower() == 'response':
                            request = interaction[0].lower()
                            for keyword in dangerous_keywords:
                                if keyword in request:
                                    dangerous_instructions_found.append(
                                        (interaction[0], file_path)
                                    )
                                    break

                except FileNotFoundError:
                    print(f"File not found: {file_path}")
                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")

    return dangerous_instructions_found

root_directory = "../../alexa_chat_results/"  # Replace with the path to your data directory.
dangerous_instructions = find_dangerous_instructions_from_files(root_directory)

if dangerous_instructions:
    print("Potentially dangerous instructions found:")
    for instruction, file_path in dangerous_instructions:
        print(f"- {instruction} (in {file_path})")
else:
    print("No potentially dangerous instructions found.")