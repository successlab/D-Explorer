import json
import os
import re
import ast

def analyze_json_files(directory):
    """
    Analyzes JSON files and writes results to a text file.
    """

    file_data = {}
    review_data = {"0": 0, "1-10": 0, "11-25": 0, "25-50": 0, "50-100": 0, "100-250": 0, "250-500": 0, "500-1000": 0, "1000-5000": 0, "> 5000": 0}
    repeated_priv_lines = {}
    repeated_dev_lines = {}
    repeated_ratings = {}
    total_skills_dup_names = set()
    total_skills_dup_invocation_names = set()
    total_skills_dup_invocations = set()
    repeated_maturity_ratings = {}
    total_flash_briefing_skills = 0
    total_dynamic_content_skills = 0
    total_dev_terms = 0

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

                        rating = data.get("apprate")
                        reviewnum = int(data.get("reviewnum").strip().replace(",", ""))
                        priv_field = data.get("priv")
                        developer = data.get("publ")
                        skdetail = data.get("skdetail")
                    

                        if skdetail:
                            if "flash briefing" in skdetail.lower():
                                total_flash_briefing_skills = total_flash_briefing_skills + 1
                            if "dynamic content" in skdetail.lower():
                                total_dynamic_content_skills = total_dynamic_content_skills + 1
                            if "developer terms of use" in skdetail.lower():
                                total_dev_terms = total_dev_terms + 1
                            lines = skdetail.splitlines()
                            for line in lines:
                                if "Rated" in line:
                                    if line in repeated_maturity_ratings.keys():
                                        repeated_maturity_ratings[line] = repeated_maturity_ratings[line] + 1
                                    else:
                                        repeated_maturity_ratings[line] = 1
                                f

                        # Handle "0" field invocation repetition
                        if priv_field:
                            # 2. Split the string by newlines
                            lines = priv_field.splitlines()

                            # 3. Extract the invocations from each line
                            for line in lines:
                                if line in repeated_priv_lines.keys():
                                    repeated_priv_lines[line] = repeated_priv_lines[line] + 1
                                else:
                                    repeated_priv_lines[line] = 1
                        
                        if developer:
                            # 2. Split the string by newlines
                            if developer in repeated_priv_lines.keys():
                                repeated_dev_lines[developer] = repeated_dev_lines[developer] + 1
                            else:
                                repeated_dev_lines[developer] = 1
                        
                        if rating:
                            # 2. Split the string by newlines

                            # 3. Extract the invocations from each line
                            if rating in repeated_ratings.keys():
                                repeated_ratings[rating] = repeated_ratings[rating] + 1
                            else:
                                repeated_ratings[rating] = 1
                        
                        if reviewnum:
                            if reviewnum == 0:
                                review_data["0"] = review_data["0"] + 1
                            elif reviewnum < 10:
                                review_data["1-10"] = review_data["1-10"] + 1
                            elif reviewnum < 25:
                                review_data["11-25"] = review_data["11-25"] + 1
                            elif reviewnum < 50:
                                review_data["25-50"] = review_data["25-50"] + 1
                            elif reviewnum < 100:
                                review_data["50-100"] = review_data["50-100"] + 1
                            elif reviewnum < 250:
                                review_data["100-250"] = review_data["100-250"] + 1
                            elif reviewnum < 500:
                                review_data["250-500"] = review_data["250-500"] + 1
                            elif reviewnum < 1000:
                                review_data["500-1000"] = review_data["500-1000"] + 1
                            elif reviewnum < 5000:
                                review_data["1000-5000"] = review_data["1000-5000"] + 1
                            else:
                                review_data["> 5000"] = review_data["> 5000"] + 1

                except json.JSONDecodeError:
                    print(f"Error: Could not parse JSON in {file_path}")
                except Exception as e:
                    print(f"An unexpected error occurred: {e} in {file_path}")
        #         break_value = break_value + 1
        # if break_value >= 3:
        #     break
        

    # Write to text file
    priv_output = "priv_data.txt"
    dev_output = "dev_data.txt"
    other_output = "misc_data.txt"

    with open(priv_output, 'w', encoding='utf-8') as outfile:
        outfile.write("Privacy Data:\n")

        for name, counts in repeated_priv_lines.items():
            outfile.write(f"- {name}: {counts}\n\n")
    
    with open(dev_output, 'w', encoding='utf-8') as outfile:
        outfile.write("Developer Data:\n")

        for name, counts in repeated_dev_lines.items():
            outfile.write(f"- {name}: {counts}\n\n")

    with open(other_output, 'w', encoding='utf-8') as outfile:
        outfile.write("Misc. Data:\n")
        outfile.write("Ratings Data:\n")
        for name, counts in repeated_ratings.items():
            outfile.write(f"- {name}: {counts}\n\n")
        outfile.write("Review Numbers Data:\n")
        for name, counts in review_data.items():
            outfile.write(f"- {name}: {counts}\n\n")
        outfile.write("Maturity Ratings Data:\n")
        for name, counts in repeated_maturity_ratings.items():
            outfile.write(f"- {name}: {counts}\n\n")
        outfile.write(f"Flash Briefing Skills: {total_flash_briefing_skills}\n")
        outfile.write(f"Dynamic Content Skills: {total_dynamic_content_skills}\n")
        outfile.write(f"Developer Terms of Service Skills: {total_dev_terms}\n")

        


    return True


# Example usage:
print("starting")
directory_path = "../crawler_2.0/result"
analyze_json_files(directory_path)

print("Analysis complete. Results written to duplicate_names_and_invocations.txt")

# Optional console output (uncomment if needed)
# print("Repeated Names:")
# for name, paths in repeated_names.items():
#     print(f"- {name}: {paths}")

# print("\nRepeated Invocations:")
# for invocation, paths in repeated_invocations.items():
#     print(f"- {invocation}: {paths}")