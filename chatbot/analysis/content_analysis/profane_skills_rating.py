import os
import json
import csv

# def extract_ratings(input_file, output_file="rating_info_profane.txt", count_output_file="rating_counts_profane.csv"):
def extract_ratings(input_file, output_file="profane_info.txt", count_output_file="rating_counts_profane.csv"):
    """
    Extracts ratings from JSON files based on profanity analysis results, and
    counts unique ratings, writing both to files.

    Args:
        input_file (str): Path to the profanity analysis text file.
        output_file (str): Path to the output text file for ratings.
        count_output_file (str): Path to the output CSV file for rating counts.
    """

    ratings = []  # Store all extracted ratings
    rating_counts = {}  # Store counts of each unique rating

    try:
        with open(input_file, 'r', encoding='utf-8') as infile, \
             open(output_file, 'w', encoding='utf-8') as outfile:
            for line in infile:
                print(line)
                line = line.strip()
                if True:
                    file_path = line
                # if line.startswith("Inappropriate content found in: "):
                #     file_path = line.replace("Inappropriate content found in: ", "").strip()
                # if line.startswith("Profanity found in: "):
                #     file_path = line.replace("Profanity found in: ", "").strip()
                    json_file_path = file_path.replace("./alexa_chat_results/", "../../../cralwer/crawler_2.0/result/").replace("_results.txt", ".json")
                    print(json_file_path)
                    try:
                        with open(json_file_path, 'r', encoding='utf-8') as json_file:
                            data = json.load(json_file)
                            skdetail = data.get("skdetail", "")
                            rating = "No rating found"

                            if skdetail:
                                rating_start = skdetail.find("Rated: ")
                                if rating_start != -1:
                                    rating_start += len("Rated: ")
                                    rating_end = skdetail.find(".", rating_start)
                                    if rating_end != -1:
                                        rating = skdetail[rating_start:rating_end].strip()

                            ratings.append(rating)  # Add rating to the list
                            outfile.write(f"{file_path}, Rating: {rating}\n")

                    except FileNotFoundError:
                        ratings.append("File not found")
                        outfile.write(f"{file_path}, Rating: File not found\n")
                    except json.JSONDecodeError:
                        ratings.append("Invalid JSON")
                        outfile.write(f"{file_path}, Rating: Invalid JSON\n")
                    except Exception as e:
                        ratings.append(f"Error - {e}")
                        outfile.write(f"{file_path}, Rating: Error - {e}\n")

        print(f"Ratings written to {output_file}")

        # Count unique ratings
        for rating in ratings:
            rating_counts[rating] = rating_counts.get(rating, 0) + 1

        # Write rating counts to CSV
        try:
            with open(count_output_file, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Rating", "Count"])
                for rating, count in rating_counts.items():
                    writer.writerow([rating, count])
            print(f"Rating counts written to {count_output_file}")

        except Exception as e:
            print(f"Error writing rating counts to CSV: {e}")

    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

input_file_path = "profane_files.txt"


extract_ratings(input_file_path)