import json
import os
import re
import ast
import os
import shutil
from collections import defaultdict  # For efficient grouping

threshold = 20

file_data = {}
repeated_names = {}
repeated_invocations = {}

import os
import json

def extract_alexa_invocations(text):
    """
    Extracts Alexa invocations from a string, handling various formats.
    Invocations must be enclosed in quotes and start with "Alexa, ".

    Args:
        text: The input string.

    Returns:
        A list of strings, where each string is an invocation (including "Alexa, ").
        Returns an empty list if no invocations are found.
    """
    invocations = []
    if text:
        # Combine all regexes into one and use finditer
        for match in re.finditer(r'"(Alexa,.*?)"|“(Alexa,.*?)”|«(Alexa,.*?)»|„(Alexa,.*?)“|\"(Alexa,.*?)\"', text):
            if match.group(1):
                invocations.append(match.group(1))
    return invocations


def top_files_by_review_num(directory, top_percent=0.25):
    folder_top_files = defaultdict(list)
    added_filenames = set()  # Keep track of filenames added *globally*

    for root, _, files in os.walk(directory):
        file_review_nums_in_folder = []  # Files and review nums *for this folder*
        json_files = (f for f in files if f.endswith(".json"))
        # if root != "../crawler_2.0/result/Social":
        #     continue
        for file in json_files:
            if file not in added_filenames:  # Check globally for duplicates
                added_filenames.add(file)
                file_path = os.path.join(root, file)
                if file[0] == "_":
                    continue
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        review_num = data.get("reviewnum")
                        review_num = review_num.replace(",", "")
                        skdetail = data.get("skdetail")
                        if skdetail:
                            if "flash briefing" not in skdetail.lower():
                                try:
                                    review_num = int(review_num.strip()) if review_num else 0
                                except (ValueError, AttributeError):
                                    review_num = 0
                                file_review_nums_in_folder.append((file, review_num))

                except (json.JSONDecodeError, FileNotFoundError) as e:
                    print(f"Error reading JSON file {file_path}: {e}")
                    continue

        file_review_nums_in_folder.sort(key=lambda x: x[1], reverse=True)  # Sort *per folder*

        num_top_files = int(len(file_review_nums_in_folder) * top_percent)
        for file, _ in file_review_nums_in_folder[:num_top_files]: # Iterate through top files in folder
            # if file not in added_filenames:  # Check globally for duplicates
            # added_filenames.add(file)
            folder_top_files[root].append(file)


    return folder_top_files

def make_skill_invocation_files(source_dir, destination_dir, approved_files):
    """
    Duplicates the directory structure from source_dir to destination_dir and
    copies the contents of each file.

    Args:
        source_dir: The path to the source directory.
        destination_dir: The path to the destination directory.
    """

    for key, value in approved_files.items():
        list_length = len(value)
        print(f"Length of {key}: {list_length}")

    try:
        break_value = 0

        for root, dirs, files in os.walk(source_dir):
            print(root)
            # if root != "../crawler_2.0/result/Social":
            #     continue
            # 1. Create the corresponding directories in the destination
            relative_path = os.path.relpath(root, source_dir) #Path relative to source directory
            destination_path = os.path.join(destination_dir, relative_path)
            os.makedirs(destination_path, exist_ok=True)  # exist_ok prevents error if dir exists
            # 2. Copy the contents of each file
            for file in files:
                if file in approved_files[root]:
                    file_path = os.path.join(root, file)
                    destination_file_path = os.path.join(destination_path, file).replace("json", "txt")
                    if file.endswith(".json"):
                        try:
                            with open(file_path, 'r', encoding='utf-8') as source_file, open(destination_file_path, 'w', encoding='utf-8') as dest_file: #Handle encoding
                                data = json.load(source_file)
                                try:
                                    filename = os.path.basename(file_path)

                                    if filename not in file_data:
                                        file_data[filename] = data
                                    else:
                                        # print(f"Warning: Duplicate filename found: {file_path}")
                                        continue

                                    skdetail_invocation = data.get("skdetail")
                                    name = data.get("name")
                                    zero_invocation_field = data.get("0")
                                    description_field = data.get("des")
                                    invocations = []


                                    # Handle skdetail invocation repetition
                                    if skdetail_invocation:
                                        match = re.search(r"Invocation Name:\s*(.+?)(?:\n|$)", skdetail_invocation)  # Improved regex
                                        if match:
                                            invocation = "Alexa, open " + match.group(1).strip()  # Extract and strip whitespace    
                                            invocations.append(invocation) 
                                            ending_string = "Alexa, disable " + match.group(1).strip()   
                                        elif name:
                                                invocation = "Alexa, open " + name.strip()
                                                ending_string = "Alexa, disable " + name.strip()
                                        else:
                                            continue
                                        # else:
                                        #     print(f"Warning: Could not extract invocation name from 'skdetail' in {file_path}: {skdetail_invocation}")

                                    # Handle "0" field invocation repetition
                                    if zero_invocation_field:
                                        try:
                                        #     # 1. Replace non-standard quotes with standard quotes
                                        #     zero_invocation_field = zero_invocation_field.replace("”", "\"").replace("“", "\"").replace("’", "'").replace("‘", "'")

                                        #     # 2. Handle escaped characters
                                        #     zero_invocation_field = zero_invocation_field.encode('unicode_escape').decode('utf-8')

                                        #     # 3. Split the string by newlines
                                        #     invocations_str = zero_invocation_field.splitlines()
                                        #     invocations = []
                                        #     for invocation_str in invocations_str:
                                        #         try:
                                        #             value = ast.literal_eval(f'"{invocation_str}"') # Evaluate each line separately
                                        #             invocations.append(value)
                                        #         except (SyntaxError, ValueError) as e:
                                        #             print(f"Error parsing line in '0' field: {e}. Line: {invocation_str}")
                                            if description_field:
                                                
                                                zero_inv_field = extract_alexa_invocations(description_field)
                                            else:
                                                zero_inv_field = []
                                                # 1. Replace non-standard quotes with standard double quotes
                                            zero_invocation_field = zero_invocation_field.replace("”", "\"").replace("“", "\"").replace("’", "'").replace("‘", "'")

                                            # 2. Split the string by newlines
                                            lines = zero_invocation_field.splitlines()

                                            # 3. Extract the invocations from each line
                                            for line in lines:
                                                line_processed = line.strip("\"")
                                                if line_processed not in zero_inv_field and line:
                                                    zero_inv_field.append(line_processed)

                                            for invocation in zero_inv_field:
                                                try:
                                                    if invocation.replace(",", "").lower() != invocations[0].replace(",", "").lower():
                                                        invocations.append(invocation)  
                                                except:
                                                    invocations.append(invocation)
                                            invocations.append(ending_string)
                                            for invocation in invocations:
                                                dest_file.write(invocation + "\n")


                                        except (SyntaxError, ValueError) as e:
                                            print(f"Error: Could not parse field '0' in {file_path}: {e} in {file_path}. Value: {zero_invocation_field}") # Include the value in the error message

                                except json.JSONDecodeError:
                                    print(f"Error: Could not parse JSON in {file_path}")
                                # except Exception as e:
                                #     print(f"An unexpected error occurred: {e} in {file_path}")
                                

                        except UnicodeDecodeError:
                            print(f"Skipping file {file_path} due to encoding error.")
                        # except Exception as e:
                        #     print(f"Error copying {file_path}: {e}")
            #             break_value = break_value + 1
            # if break_value >= 3:
            #     break

    except FileNotFoundError:
        print(f"Error: Source directory '{source_dir}' not found.")
    # except Exception as e:
    #     print(f"An unexpected error occurred: {e}")


# Example usage:
source_directory = "../crawler_2.0/result/"  # Replace with your source directory
destination_directory = "./invocations" # Replace with your destination directory
print("Starting")
approved_skills = top_files_by_review_num(source_directory)
make_skill_invocation_files(source_directory, destination_directory, approved_skills)

                