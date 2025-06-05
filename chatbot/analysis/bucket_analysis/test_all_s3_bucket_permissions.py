import boto3
import botocore.exceptions
import random
import string
import csv

def test_s3_permissions(bucket_name):
    """
    Tests S3 bucket permissions for list, read, write, and delete.

    Args:
        bucket_name (str): The name of the S3 bucket.

    Returns:
        dict: A dictionary containing the results of each test (True/False).
    """
    s3 = boto3.client('s3')
    results = {
        'list': False,
        'read': False,
        'write': False,
        'delete': False,
    }

    # Test List
    try:
        response = s3.list_objects_v2(Bucket=bucket_name, MaxKeys=1)
        if 'Contents' in response or 'KeyCount' in response and response['KeyCount'] == 0:
            results['list'] = True
        else:
            print(f"List failed: Could not list objects in {bucket_name}.")

    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'AccessDenied':
            print(f"List failed: Access denied to list objects in {bucket_name}.")
        else:
            print(f"List failed: An error occurred during list: {e}")

    except Exception as e:
        print(f"List failed: An unexpected error occurred: {e}")

    # Test Read (download)
    if results['list']:
        try:
            if 'Contents' in response:
                object_key = response['Contents'][0]['Key']
                local_file_path = "temp_download.txt"
                s3.download_file(bucket_name, object_key, local_file_path)
                results['read'] = True
            else:
                results['read'] = True  # Empty bucket read "works"
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'AccessDenied':
                print(f"Read failed: Access denied to download objects from {bucket_name}.")
            else:
                print(f"Read failed: An error occurred during download: {e}")
        except Exception as e:
            print(f"Read failed: An unexpected error occurred: {e}")

    # Test Write and Delete
    random_key = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    object_key = f"test-write-{random_key}.txt"
    test_content = "This is a temporary test object."

    try:
        s3.put_object(Bucket=bucket_name, Key=object_key, Body=test_content.encode('utf-8'))
        results['write'] = True
        s3.delete_object(Bucket=bucket_name, Key=object_key)
        results['delete'] = True

    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'AccessDenied':
            print(f"Write/Delete failed: Access denied to write/delete objects in {bucket_name}.")
        else:
            print(f"Write/Delete failed: An error occurred during write/delete: {e}")
    except Exception as e:
        print(f"Write/Delete failed: An unexpected error occurred: {e}")

    return results

def test_buckets_from_csv(csv_file):
    """
    Tests permissions for S3 buckets listed in a CSV file, only including .s3 domains.

    Args:
        csv_file (str): Path to the CSV file.
    """
    try:
        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                domain = row[0]
                expected_result = row[3]
                if ".s3" in domain and "200" in expected_result: #Only test s3 domains that have a 200 result in the last column.
                    bucket_name = domain.split(".s3")[0] #get the bucket name from the domain.
                    results = test_s3_permissions(bucket_name)
                    print(f"\nResults for bucket: {bucket_name}")
                    for permission, result in results.items():
                        print(f"{permission.capitalize()}: {result}")
    except FileNotFoundError:
        print(f"Error: CSV file '{csv_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    csv_file = "comparison_results.csv"  # Replace with your CSV file path
    test_buckets_from_csv(csv_file)