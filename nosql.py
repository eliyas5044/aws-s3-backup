import boto3
from dotenv import load_dotenv
import os
import time

# Load environment variables from .env file
load_dotenv()

# S3 bucket details
SOURCE_BUCKET = os.getenv('SOURCE_BUCKET')
DESTINATION_BUCKET = os.getenv('DESTINATION_BUCKET')
AWS_REGION = os.getenv('AWS_REGION')

# AWS Credentials (Optional if configured globally)
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')


def get_s3_prefix(table_name):
    """Determine the S3 prefix based on the table name."""
    if table_name.endswith('s'):
        return table_name
    return f"{table_name}s"


def process_batch(ids_batch, s3_client, prefix):
    """Process a single batch of IDs."""
    for id_value in ids_batch:
        s3_prefix = f"{prefix}/{id_value}/"
        print(f"Processing prefix: {s3_prefix}")

        try:
            # List objects under the prefix
            response = s3_client.list_objects_v2(Bucket=SOURCE_BUCKET, Prefix=s3_prefix)
            if 'Contents' in response:
                for obj in response['Contents']:
                    source_key = obj['Key']
                    destination_key = source_key
                    print(f"Copying {source_key} to {DESTINATION_BUCKET}/{destination_key}")
                    s3_client.copy_object(
                        Bucket=DESTINATION_BUCKET,
                        CopySource={'Bucket': SOURCE_BUCKET, 'Key': source_key},
                        Key=destination_key
                    )
            else:
                print(f"No objects found for ID {id_value}")
        except Exception as e:
            print(f"Error processing ID {id_value}: {e}")


def copy_s3_objects_for_ids(ids, s3_client, table_name, batch_size=50):
    """Copy objects in batches with logging and feedback."""
    s3_prefix = get_s3_prefix(table_name)
    total_ids = len(ids)

    if total_ids == 0:
        print("No IDs to process. Exiting.")
        return

    print(f"Total IDs to process: {total_ids}")
    for i in range(0, total_ids, batch_size):
        batch = ids[i:i + batch_size]
        print(f"\nProcessing batch {i // batch_size + 1} (IDs {batch[0]} to {batch[-1]}).")
        process_batch(batch, s3_client, s3_prefix)
        print(f"Completed batch {i // batch_size + 1}.")
        time.sleep(1)  # Add a slight delay to avoid overloading the API


if __name__ == "__main__":
    # Prompt user for table name
    table_name = input("Enter the table name corresponding to the S3 prefix: ").strip()

    # Prompt user to paste IDs
    ids_input = input("Paste the IDs (comma-separated, e.g., 1,2,3,4): ").strip()

    # Parse and validate IDs
    ids = [id.strip() for id in ids_input.split(",") if id.strip().isdigit()]

    if ids:
        print(f"Parsed {len(ids)} IDs successfully: {ids[:10]}{'...' if len(ids) > 10 else ''}")

        # Create S3 client
        s3_client = boto3.client(
            's3',
            region_name=AWS_REGION,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )

        # Copy objects for the IDs in batches
        copy_s3_objects_for_ids(ids, s3_client, table_name, batch_size=50)
    else:
        print("No valid IDs provided. Please check your input.")
