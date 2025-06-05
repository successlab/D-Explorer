def filter_lines(input_file, output_file):
    """
    Reads lines from input_file, removes lines containing specified URLs,
    and writes the filtered lines to output_file.
    """

    # URLs that show up in too high a percentage of results.
    bad_urls = [
        
    ]

    try:
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line in infile:
                if not any(bad_url in line for bad_url in bad_urls):
                    outfile.write(line)
        print(f"Filtered lines from '{input_file}' and wrote to '{output_file}'.")

    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
input_filename = 'filtered_url_results.txt'  # Replace with your input file name
output_filename = 'filtered_url_results_new.txt' # Replace with your output file name

filter_lines(input_filename, output_filename)

input_filename = 'top_level_folders.txt'  # Replace with your input file name
output_filename = 'top_level_folders_new.txt' # Replace with your output file name

filter_lines(input_filename, output_filename)