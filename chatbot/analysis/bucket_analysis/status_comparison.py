import csv

def compare_domain_statuses(file1, file2, file3, output_file="comparison_results.csv"):
    """
    Compares domain statuses from three text files and writes the results to a CSV file.
    Replaces any status containing "Error" with "Error".
    """

    def read_domain_statuses(filename):
        """Helper function to read domain statuses from a file."""
        domain_statuses = {}
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if line:
                        parts = line.split(", Status: ")
                        if len(parts) == 2:
                            domain_str = parts[0].replace("Domain: ", "").strip()
                            status = parts[1].strip()
                            if "Error" in status:
                                status = "Error"
                            domain_statuses[domain_str] = status
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        except Exception as e:
            print(f"Error reading file '{filename}': {e}")
        return domain_statuses

    statuses1 = read_domain_statuses(file1)
    statuses2 = read_domain_statuses(file2)
    statuses3 = read_domain_statuses(file3)

    all_domains = set(list(statuses1.keys()) + list(statuses2.keys()) + list(statuses3.keys()))

    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Domain", f"Status({file1})", f"Status({file2})", f"Status({file3})"])

            for domain in sorted(all_domains):
                status1 = statuses1.get(domain, "N/A")
                status2 = statuses2.get(domain, "N/A")
                status3 = statuses3.get(domain, "N/A")
                writer.writerow([domain, status1, status2, status3])

        print(f"Comparison results written to {output_file}")

    except Exception as e:
        print(f"Error writing to CSV file: {e}")

file1_path = "full_url_statuses.txt"
file2_path = "top_level_folder_statuses.txt"
file3_path = "domain_statuses.txt"



compare_domain_statuses(file1_path, file2_path, file3_path)