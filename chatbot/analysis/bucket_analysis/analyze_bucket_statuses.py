import csv
import re

def analyze_domain_statuses(csv_file, output_csv):
    """
    Analyzes domain statuses from a CSV file, only including domains with "s3." or "cloudfront" and counts unique domains for each status.
    Writes the results to a CSV file.

    Args:
        csv_file (str): Path to the input CSV file.
        output_csv (str): Path to the output CSV file.
    """

    status_counts = {
        "Status(full_url_statuses.txt)": {},
        "Status(top_level_folder_statuses.txt)": {},
        "Status(domain_statuses.txt)": {}
    }

    try:
        with open(csv_file, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                domain = row["Domain"]
                if "s3." in domain or "cloudfront" in domain:
                    for status_column in status_counts:
                        status = row[status_column]
                        if status not in status_counts[status_column]:
                            status_counts[status_column][status] = set()
                        status_counts[status_column][status].add(domain)

        with open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(["Status Column", "Status", "Unique Domains Count"]) #Header Row

            for status_column, status_data in status_counts.items():
                for status, domains in status_data.items():
                    writer.writerow([status_column, status, len(domains)])

        print(f"Results written to {output_csv}")

    except FileNotFoundError:
        print(f"Error: CSV file '{csv_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    input_csv_file = "comparison_results.csv"  # Replace with your input CSV file path
    output_csv_file = "domain_status_counts.csv" #Replace with desired output file name.
    analyze_domain_statuses(input_csv_file, output_csv_file)