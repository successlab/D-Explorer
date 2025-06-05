import os

def count_files_and_write_to_file(root_dir, output_file):
    """
    Counts unique and total files, and writes results to a file.

    Args:
        root_dir: The path to the root directory.
        output_file: The path to the output text file.
    """

    try:
        all_unique_files = set()
        results = {}
        total_file_count = 0  # Initialize total file count
        

        for dirpath, dirnames, filenames in os.walk(root_dir):
            unique_files_in_dir = set()
            total_files_in_dir = len(filenames) # Total files in this directory
            total_file_count += total_files_in_dir # Add to overall count

            for filename in filenames:
                all_unique_files.add(filename)  # Add to the overall set (duplicates ignored)
                unique_files_in_dir.add(filename) # Add to the per-folder set (duplicates ignored)
            results[dirpath] = (unique_files_in_dir, total_files_in_dir) # Store both unique and total counts


        with open(output_file, "w") as f:
            for folder, (unique_files, total_files) in results.items():
                f.write(f"Folder: {folder}\n")
                f.write(f"  Unique files: {len(unique_files)}\n")
                f.write(f"  Total files: {total_files}\n") # Write total file count for this folder
                # Optionally write the unique file names for each directory
                # f.write(f"  File names: {', '.join(sorted(list(unique_files)))}\n") # Uncomment if you want filenames listed
                f.write("\n")

            f.write(f"Total unique files across all folders: {len(all_unique_files)}\n")
            f.write(f"Total files across all folders: {total_file_count}\n")


    except FileNotFoundError:
        print(f"Error: Directory '{root_dir}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
root_directory = "../crawler_2.0/result/"  # Replace with the actual path
output_file = "crawler_skill_numbers.txt"
count_files_and_write_to_file(root_directory, output_file)
