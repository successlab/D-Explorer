import re
import csv
from urllib.parse import urlparse

def analyze_url_file(filepath):
    """
    Analyzes a text file containing URLs, parses them, and counts file types.
    Logs URLs without identifiable file extensions as "unknown".

    Args:
        filepath (str): Path to the input text file.

    Returns:
        dict: Dictionary containing counts of each file type.
    """
    file_type_counts = {
        "s3": {},
        "cloudfront": {},
        "other": {}
    }

    try:
        with open(filepath, 'r') as f:
            urls = [line.strip() for line in f]
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return file_type_counts
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        return file_type_counts

    for url in urls:
        parsed_url = urlparse(url)
        path = parsed_url.path
        match = re.search(r"\.([a-zA-Z0-9]+)(\?.*)?$", path)
        if match:
            file_extension = match.group(1).lower()
            if "s3." in parsed_url.netloc:
                file_type_counts["s3"][file_extension] = file_type_counts["s3"].get(file_extension, 0) + 1
            elif "cloudfront.net" in parsed_url.netloc:
                file_type_counts["cloudfront"][file_extension] = file_type_counts["cloudfront"].get(file_extension, 0) + 1
            else:
                file_type_counts["other"][file_extension] = file_type_counts["other"].get(file_extension, 0) + 1
        else:
            if "s3." in parsed_url.netloc:
                file_type_counts["s3"]["unknown"] = file_type_counts["s3"].get("unknown", 0) + 1
            elif "cloudfront.net" in parsed_url.netloc:
                file_type_counts["cloudfront"]["unknown"] = file_type_counts["cloudfront"].get("unknown", 0) + 1
            else:
                file_type_counts["other"]["unknown"] = file_type_counts["other"].get("unknown", 0) + 1

    return file_type_counts

def write_to_csv(file_type_counts, output_csv="url_file_types.csv"):
    """
    Writes the file type counts to a CSV file.

    Args:
        file_type_counts (dict): Dictionary containing file type counts.
        output_csv (str): Path to the output CSV file.
    """
    all_file_types = set()
    for category in file_type_counts.values():
        all_file_types.update(category.keys())

    all_file_types = sorted(list(all_file_types))

    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["File Type", "S3", "CloudFront", "Other"])

        for file_type in all_file_types:
            s3_count = file_type_counts["s3"].get(file_type, 0)
            cloudfront_count = file_type_counts["cloudfront"].get(file_type, 0)
            other_count = file_type_counts["other"].get(file_type, 0)
            writer.writerow([file_type, s3_count, cloudfront_count, other_count])

    print(f"File type counts written to {output_csv}")

def main():
    filepath = "filtered_url_results.txt"  # Replace with your file path
    file_type_counts = analyze_url_file(filepath)
    write_to_csv(file_type_counts)

if __name__ == "__main__":
    main()