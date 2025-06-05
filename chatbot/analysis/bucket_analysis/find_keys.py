import re

def find_non_image_non_txt_keys(input_file, output_file="non_image_non_txt_keys.txt"):
    """
    Finds file keys that are not images or text files from an input text file.

    Args:
        input_file (str): Path to the input text file.
        output_file (str, optional): Path to the output text file.
    """

    non_matching_keys = []

    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            content = infile.read()

        key_matches = re.findall(r'<Key>(.*?)</Key>', content, re.DOTALL)

        for key in key_matches:
            if not (key.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.txt'))):
                non_matching_keys.append(key)

        with open(output_file, 'w', encoding='utf-8') as outfile:
            for key in non_matching_keys:
                outfile.write(key + '\n')

        print(f"Non-image, non-txt keys written to {output_file}")

    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

input_file_path = "bucketdata.txt"

find_non_image_non_txt_keys(input_file_path)