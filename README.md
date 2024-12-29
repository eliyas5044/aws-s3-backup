## AWS-S3-Backup

### Overview
AWS-S3-Backup is a Python project designed to automate the backup of S3 objects based on IDs fetched from relational databases like **MySQL** or **PostgreSQL**, or provided manually. This script helps ensure your files are securely backed up between S3 buckets based on specific database records.

### Features
- **Database Integration**:
  - Supports fetching IDs from **MySQL** and **PostgreSQL** using SQL queries.
- **Manual Input**:
  - Provides a fallback script (`nosql.py`) for manually inputting IDs if no database connection is available.
- **S3 Object Backup**:
  - Copies files from a source S3 bucket to a destination S3 bucket based on the database IDs.
- **Batch Processing**:
  - Handles large datasets efficiently using `LIMIT` and `OFFSET` queries or manual batching.
- **Environment Variables**:
  - Fully configurable via a `.env` file for sensitive credentials and settings.
- **Cross-Platform**:
  - Works seamlessly on Windows, macOS, and Linux.

### Requirements
- Python 3.7 or higher.
- AWS IAM role with S3 access (`s3:ListObjects`, `s3:GetObject`, `s3:PutObject`).
- MySQL or PostgreSQL access (optional for `mysql.py` and `postgresql.py` scripts).

### Use Cases
1. Backing up files in S3 that correspond to specific database records.
2. Automating file management and synchronization between S3 buckets.
3. Processing large datasets in a controlled, batch-oriented manner.

---

### File Structure
```
AWS-S3-BACKUP/
│
├── .env              # Environment variables for configuration
├── .env.example      # Example environment file for reference
├── .gitignore        # Git ignore file to exclude sensitive or unnecessary files
├── mysql.py          # MySQL database integration script
├── postgresql.py     # PostgreSQL database integration script
├── nosql.py          # Script for manual ID input
├── requirements.txt  # Python dependencies
├── README.md         # Project documentation
└── venv/             # Virtual environment (not included in version control)
```

---

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/eliyas5044/aws-s3-backup.git
   cd aws-s3-backup
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure the `.env` file:
   - Copy the `.env.example` file:
     ```bash
     cp .env.example .env
     ```
   - Fill in the AWS, MySQL/PostgreSQL credentials, and bucket information.

---

### Usage

#### **1. MySQL Script**
Run the script to fetch IDs from a MySQL database and back up corresponding S3 objects:
```bash
python mysql.py
```

#### **2. PostgreSQL Script**
Run the script to fetch IDs from a PostgreSQL database and back up corresponding S3 objects:
```bash
python postgresql.py
```

#### **3. Manual ID Input**
Use this script if no database is required:
```bash
python nosql.py
```
Paste comma-separated IDs when prompted (e.g., `1,2,3,4`).

---

### Environment Variables

The `.env` file contains the configuration for the project. Example:

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

---

### Contributing
Contributions are welcome! Feel free to fork the repository, submit issues, or create pull requests.

---

### License
This project is licensed under the MIT License. See the `LICENSE` file for details.
