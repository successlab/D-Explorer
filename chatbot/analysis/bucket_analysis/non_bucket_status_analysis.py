import csv

def count_success_200_non_s3_cloudfront(csv_file, output_file="success_counts.csv"):
    """
    Counts domains with "Success (200)" in each status column, excluding .s3 and cloudfront domains,
    and writes the results (counts and percentages) to a CSV file.

    Args:
        csv_file (str): Path to the input CSV file.
        output_file (str): Path to the output CSV file.
    """
    counts = [0, 0, 0]  # Initialize counts for each column
    total_domains = 0

    try:
        with open(csv_file, 'r', newline='', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            for row in reader:
                domain = row[0].lower()
                if ".s3" not in domain and "cloudfront" not in domain:
                    total_domains += 1
                    for i in range(1, 4):  # Iterate through status columns (1, 2, 3)
                        if "success (200)" in row[i].lower():
                            counts[i - 1] += 1

        percentages = [(count / total_domains) * 100 if total_domains > 0 else 0 for count in counts]

        with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(["Column", "Success (200) Count", "Percentage of Total Domains"])
            for i, (count, percentage) in enumerate(zip(counts, percentages)):
                writer.writerow([f"Column {i + 1}", count, f"{percentage:.2f}%"])

        print(f"Success (200) counts and percentages written to {output_file}")

    except FileNotFoundError:
        print(f"Error: CSV file '{csv_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
csv_file_path = "comparison_results.csv"  # Replace with your CSV file path
count_success_200_non_s3_cloudfront(csv_file_path)