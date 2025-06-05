import os
import csv
import fnmatch

"""Looks at skill counts for vulnerable backends. Use like the resource file summary file."""

# def count_matching_files_per_directory(csv_file, root_dir, output_file="skill_counts_vulnerable_buckets.csv"):
# def count_matching_files_per_directory(csv_file, root_dir, output_file="skill_counts_vulnerable_non_buckets.csv"):
def count_matching_files_per_directory(csv_file, root_dir, output_file="skill_counts_vulnerable_cloudfront.csv"):
# def count_matching_files_per_directory(csv_file, root_dir, output_file="skill_counts_vulnerable_s3.csv"):
# def count_matching_files_per_directory(csv_file, root_dir, output_file="skill_counts_vulnerable_all.csv"):
    """
    Counts files in each directory that contain domains with status 200,
    checking each column independently.
    """

    try:
        with open(csv_file, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)

        if not data:
            print("Error: CSV file is empty.")
            return

        domains = [row[0] for row in data]
        num_columns = len(data[0]) - 1

        directory_counts = {}

        for root, dirs, files in os.walk(root_dir):
            folder_name = os.path.basename(root)
            directory_counts[folder_name] = [0] * num_columns

            for file in fnmatch.filter(files, "*.txt"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        file_content = f.read().lower()
                        # domain_found_in_column = False

                        for col_index in range(num_columns):
                            domain_found_in_column = False
                            for row_index, domain in enumerate(domains):
                                status = data[row_index][col_index + 1].lower()
                                # if 'cloudfront' in domain.lower() or '.s3' in domain.lower():
                                # if not 'cloudfront' in domain.lower() or not '.s3' in domain.lower():
                                if 'cloudfront' in domain.lower():
                                # if True:
                                # if '.s3' in domain.lower():
                                    if domain.lower() in file_content and "success (200)" in status:
                                        domain_found_in_column = True
                                        break
                            if domain_found_in_column:
                                    directory_counts[folder_name][col_index] += 1

                except Exception as e:
                    print(f"Error processing file '{file_path}': {e}")

        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
                writer = csv.writer(outfile)
                header = ["Directory"] + [f"Column {i+1}" for i in range(num_columns)]
                writer.writerow(header)

                for directory, counts in directory_counts.items():
                    writer.writerow([directory] + counts)

            print(f"Directory domain counts written to {output_file}")
        except Exception as e:
            print(f"Error writing to CSV file: {e}")

    except FileNotFoundError:
        print(f"Error: CSV file '{csv_file}' not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Example usage (create sample files for testing):
csv_file_path = "comparison_results.csv"
root_directory = "../../alexa_chat_results"



count_matching_files_per_directory(csv_file_path, root_directory)