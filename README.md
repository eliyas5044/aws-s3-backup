# AWS-S3-BACKUP

This project provides Python scripts for managing and backing up data from a PostgreSQL or MySQL database and synchronizing corresponding S3 objects. The scripts fetch IDs from the database and copy associated files from one S3 bucket to another for backup.

## Features
- Fetch IDs dynamically from MySQL or PostgreSQL.
- Supports `LIMIT` and `OFFSET` for efficient data processing.
- Copies S3 objects corresponding to database IDs.
- Configurable through an `.env` file.

## Prerequisites

1. **Python**: Version 3.7 or higher.
2. **AWS Credentials**: Ensure your AWS access and secret keys are set in the `.env` file or globally configured.
3. **Database Access**: Set up MySQL or PostgreSQL credentials in the `.env` file.
4. **Python Libraries**: Install required dependencies listed in `requirements.txt`.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/eliyas5044/aws-s3-backup.git
   cd aws-s3-backup
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   - Copy the `.env.example` file:
     ```bash
     cp .env.example .env
     ```
   - Update the `.env` file with your AWS, MySQL, or PostgreSQL credentials and bucket details.

## Usage

### MySQL Script
1. Run the MySQL backup script:
   ```bash
   python mysql.py
   ```
2. Enter the table name and adjust offset/limit when prompted.

### PostgreSQL Script
1. Run the PostgreSQL backup script:
   ```bash
   python postgresql.py
   ```
2. Enter the table name and adjust offset/limit when prompted.

### NoSQL or Manual Input Script
1. Run the manual input script:
   ```bash
   python nosql.py
   ```
2. Paste comma-separated IDs when prompted.

## File Structure

```
AWS-S3-BACKUP/
│
├── .env              # Your environment variables (not tracked by git)
├── .env.example      # Example environment file
├── .gitignore        # Git ignore file
├── mysql.py          # MySQL database script
├── postgresql.py     # PostgreSQL database script
├── nosql.py          # Script for manual ID input
├── requirements.txt  # Python dependencies
├── README.md         # Project documentation
└── venv/             # Virtual environment (not tracked by git)
```

## Environment Variables

The `.env` file should include the following:

```env
# AWS S3 Configuration
SOURCE_BUCKET=your_source_bucket
DESTINATION_BUCKET=your_destination_bucket
AWS_REGION=your_region
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key

# MySQL Configuration
MYSQL_HOST=your_mysql_host
MYSQL_DATABASE=your_database_name
MYSQL_USER=your_username
MYSQL_PASSWORD=your_password

# PostgreSQL Configuration
POSTGRES_HOST=your_postgres_host
POSTGRES_DATABASE=your_database_name
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
POSTGRES_PORT=5432
```

## Notes
- Use `nosql.py` for manual ID inputs if you don't want to connect to a database.
- Ensure your AWS IAM role has permissions for `s3:ListObjects`, `s3:GetObject`, and `s3:PutObject`.

## License
This project is licensed under the MIT License.
