"For finding files the crawler skips."
import json
import os
import subprocess  # For running shell commands

def find_false_contexts(directory):
    """
    Finds all instances of "completion": false in JSON files, extracts the 
    entire JSON object, and then processes it with cut, sort, and grep.

    Args:
        directory: The directory to search.

    Returns:
        The count of unique third fields after cutting, sorting, and grepping.
        Returns None if there is an error in the shell commands.
    """
    unique_contexts = set()
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        if isinstance(data, list):
                            for item in data:
                                if isinstance(item, dict) and item.get("completion") == False:
                                    unique_contexts.add(json.dumps(item, sort_keys=True))
                        elif isinstance(data, dict) and data.get("completion") == False:
                            unique_contexts.add(json.dumps(data, sort_keys=True))
                        else:
                            print(f"Warning: JSON structure is not a list or dictionary in {file_path}")

                except json.JSONDecodeError:
                    print(f"Error: Could not parse JSON in {file_path}")
                except Exception as e:
                    print(f"An unexpected error occurred: {e} in {file_path}")

    # Process with cut, sort, and grep
    try:
        json_strings = "\n".join(unique_contexts)  # Join with newlines
        process = subprocess.Popen(
            ["cut", "-d", ":", "-f", "3"],  # Cut command
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        cut_output, cut_error = process.communicate(input=json_strings.encode()) # Pass JSON strings to cut command

        if cut_error:
            raise Exception(f"Cut error: {cut_error.decode()}")

        process = subprocess.Popen(
            ["sort", "-u"],  # Sort command
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        sort_output, sort_error = process.communicate(input=cut_output)

        if sort_error:
            raise Exception(f"Sort error: {sort_error.decode()}")

        process = subprocess.Popen(
            ["grep", "-c", ""],  # Grep command (empty string)
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        grep_output, grep_error = process.communicate(input=sort_output)

        if grep_error:
            raise Exception(f"Grep error: {grep_error.decode()}")
        
        count = int(grep_output.decode().strip()) # Get integer count from grep output
        return count

    except Exception as e:
        print(f"Error in cut/sort/grep pipeline: {e}")
        return None  # Indicate an error

# Example usage:
directory_path = "../crawler_2.0/metadata"
count = find_false_contexts(directory_path)

if count is not None:
    print(f"Missed Files: {count}")