import boto3
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# MySQL connection details
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')

# S3 bucket details
SOURCE_BUCKET = os.getenv('SOURCE_BUCKET')  # Source bucket
DESTINATION_BUCKET = os.getenv('DESTINATION_BUCKET')  # Destination bucket for backups
AWS_REGION = os.getenv('AWS_REGION')

# AWS Credentials (Optional if configured globally)
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')


def get_ids_with_limit(table_name, offset, limit):
    """Fetch a limited number of IDs with offset from the specified table in the database."""
    try:
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            database=MYSQL_DATABASE,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD
        )
        if connection.is_connected():
            cursor = connection.cursor()
            query = f"""
                SELECT id 
                FROM {table_name}
                LIMIT {offset}, {limit};
            """
            cursor.execute(query)
            ids = [str(row[0]) for row in cursor.fetchall()]  # Ensure IDs are strings
            return ids
    except Error as e:
        print(f"Error fetching IDs from table {table_name}: {e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def copy_s3_objects_for_ids(ids, s3_client, table_name):
    """Copy objects for each ID from the source bucket to the destination bucket."""
    # Construct the S3 prefix dynamically using the plural of the table name
    s3_prefix = f"{table_name}s/"  # Plural form of the table name
    print(f"Using S3 prefix: {s3_prefix}")

    for id_value in ids:
        # Construct the prefix for each ID
        prefix = f"{s3_prefix}{id_value}/"
        print(f"Processing prefix: {prefix}")

        # List objects under the prefix
        response = s3_client.list_objects_v2(Bucket=SOURCE_BUCKET, Prefix=prefix)
        if 'Contents' in response:
            for obj in response['Contents']:
                source_key = obj['Key']
                destination_key = source_key  # Maintain the same key structure

                print(f"Copying {source_key} to {DESTINATION_BUCKET}/{destination_key}")

                # Copy the object
                s3_client.copy_object(
                    Bucket=DESTINATION_BUCKET,
                    CopySource={'Bucket': SOURCE_BUCKET, 'Key': source_key},
                    Key=destination_key
                )
        else:
            print(f"No objects found for ID {id_value}")


if __name__ == "__main__":
    # Prompt user for the table name
    table_name = input("Enter the table name from which to fetch IDs: ").strip()

    # Define the offset and limit
    offset = int(input("Enter the offset (starting point, e.g., 0): ").strip())
    limit = int(input("Enter the limit (number of IDs to fetch, e.g., 30): ").strip())

    # Fetch limited IDs from the database
    ids = get_ids_with_limit(table_name, offset, limit)

    if ids:
        print(f"Fetched {len(ids)} IDs: {ids}")
        # Create S3 client
        s3_client = boto3.client(
            's3',
            region_name=AWS_REGION,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )

        # Copy objects for the IDs
        copy_s3_objects_for_ids(ids, s3_client, table_name)
    else:
        print(f"No IDs found in table '{table_name}' with the given offset and limit.")
