import json
import os
import re
import ast

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
            invocations.append(match.group(1))

    return invocations

def analyze_json_files(directory, output_file="duplicate_names_and_invocations.txt"):
    """
    Analyzes JSON files and writes results to a text file.
    """

    file_data = {}
    repeated_names = {}
    repeated_invocations = {}
    repeated_invocation_names = {}
    total_skills_dup_names = set()
    total_skills_dup_invocation_names = set()
    total_skills_dup_invocations = set()

    for root, _, files in os.walk(directory):
        print(root)
        break_value = 0
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        filename = os.path.basename(file_path)

                        if filename not in file_data:
                            file_data[filename] = data
                        else:
                            # print(f"Warning: Duplicate filename found: {file_path}")
                            continue

                        name = data.get("name")
                        skdetail_invocation = data.get("skdetail")
                        zero_invocation_field = data.get("0")
                        description_field = data.get("des")

                        # Handle name repetition
                        if name:
                            if name in repeated_names:
                                repeated_names[name].append(file_path)
                                total_skills_dup_names.add(file_path)
                            elif any(data_item.get("name") == name and os.path.basename(data_file) != filename for data_file, data_item in file_data.items()):
                                repeated_names[name] = [file_path]
                                for data_file, data_item in file_data.items():
                                    if data_item.get("name") == name and os.path.basename(data_file) != filename:
                                        repeated_names[name].append(os.path.join(os.path.dirname(data_file),os.path.basename(data_file)))

                        # Handle skdetail invocation repetition
                        if skdetail_invocation:
                            match = re.search(r"Invocation Name:\s*(.+?)(?:\n|$)", skdetail_invocation)  # Improved regex
                            if match:
                                invocation = match.group(1).strip()  # Extract and strip whitespace
                                if invocation in repeated_invocation_names:
                                    repeated_invocation_names[invocation].append(file_path)
                                    total_skills_dup_invocation_names.add(file_path)
                                elif any(data_item.get("skdetail") and re.search(r"Invocation Name:\s*(.+?)(?:\n|$)", data_item.get("skdetail")) and re.search(r"Invocation Name:\s*(.+?)(?:\n|$)", data_item.get("skdetail")).group(1).strip() == invocation and os.path.basename(data_file) != filename for data_file, data_item in file_data.items()):
                                    repeated_invocation_names[invocation] = [file_path]
                                    for data_file, data_item in file_data.items():
                                        if data_item.get("skdetail") and re.search(r"Invocation Name:\s*(.+?)(?:\n|$)", data_item.get("skdetail")) and re.search(r"Invocation Name:\s*(.+?)(?:\n|$)", data_item.get("skdetail")).group(1).strip() == invocation and os.path.basename(data_file) != filename:
                                            repeated_invocation_names[invocation].append(os.path.join(os.path.dirname(data_file),os.path.basename(data_file)))

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
                                    
                                    invocations = extract_alexa_invocations(description_field)
                                else:
                                    invocations = []
                                    # 1. Replace non-standard quotes with standard double quotes
                                zero_invocation_field = zero_invocation_field.replace("”", "\"").replace("“", "\"").replace("’", "'").replace("‘", "'")

                                # 2. Split the string by newlines
                                lines = zero_invocation_field.splitlines()

                                # 3. Extract the invocations from each line
                                for line in lines:
                                    line_processed = line.strip("\"")
                                    if line_processed not in invocations:
                                        invocations.append(line_processed)
                                # print(invocations)

                                for invocation in invocations:
                                    if invocation and ("Alexa, stop" == invocation or  "Flash Briefing" in invocation or invocation=="None"):
                                        pass
                                    elif invocation in repeated_invocations:
                                        repeated_invocations[invocation].append(file_path)
                                        total_skills_dup_invocations.add(file_path)
                                    else:
                                        repeated_invocations[invocation] = [file_path]

                            except (SyntaxError, ValueError) as e:
                                print(f"Error: Could not parse field '0' in {file_path}: {e} in {file_path}. Value: {zero_invocation_field}") # Include the value in the error message

                except json.JSONDecodeError:
                    print(f"Error: Could not parse JSON in {file_path}")
                # except Exception as e:
                #     print(f"An unexpected error occurred: {e} in {file_path}")
                # break_value = break_value + 1
        # if break_value >= 3:
        #     break
        

    # Write to text file
    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write("Repeated Names:\n")

        for name, paths in repeated_names.items():
            if len(paths) > 1:
                outfile.write(f"- {name}: {len(paths)}\n {paths}\n\n")
        outfile.write(f"Total Skills: {len(total_skills_dup_names)}\n")


        outfile.write("\nRepeated Invocation Names:\n")
        for invocation, paths in repeated_invocation_names.items():
            if len(paths) > 1:
                outfile.write(f"- {invocation}: {len(paths)}\n {paths}\n\n")
        outfile.write(f"Total Skills: {len(total_skills_dup_invocation_names)}\n")


        outfile.write("\nRepeated Invocations:\n")
        for invocation, paths in repeated_invocations.items():
            if len(paths) > 1:
                outfile.write(f"- {invocation}: {len(paths)}\n {paths}\n\n")
        outfile.write(f"Total Skills: {len(total_skills_dup_invocations)}\n")

    return repeated_names, repeated_invocations


# Example usage:
print("starting")
directory_path = "../crawler_2.0/result"
repeated_names, repeated_invocations = analyze_json_files(directory_path)

print("Analysis complete. Results written to duplicate_names_and_invocations.txt")

# Optional console output (uncomment if needed)
# print("Repeated Names:")
# for name, paths in repeated_names.items():
#     print(f"- {name}: {paths}")

# print("\nRepeated Invocations:")
# for invocation, paths in repeated_invocations.items():
#     print(f"- {invocation}: {paths}")