# AIS Parquet Query

A comprehensive toolkit for querying parquet files from Amazon S3 using multiple methods and libraries.

## Overview

This project provides various approaches to read and query parquet files stored in Amazon S3, including:
- **DuckDB**: Direct SQL queries on S3 parquet files
- **Boto3 + Pandas**: Traditional approach with full control
- **PyArrow**: High-performance columnar data processing
- **S3FS**: Seamless S3 filesystem integration

## Quick Start

### Automated Setup (Recommended)

The easiest way to get started is using the automated setup script:

```bash
python setup.py
```

This script will:
- ✅ Check Python version compatibility (3.8+)
- ✅ Create a virtual environment (`venv`)
- ✅ Install all required dependencies
- ✅ Set up Jupyter kernel for the project
- ✅ Provide next steps instructions

### AWS Credentials Setup

#### Option 1: Interactive Setup Script (Recommended)
Use the provided setup script for easy credential configuration:

```bash
source set_env.sh
```

This script will:
- ✅ Prompt for your AWS credentials securely
- ✅ Set up environment variables for `il-central-1` region
- ✅ Create a `.env` file for future use
- ✅ Verify your credentials with AWS
- ✅ Add `.env` to `.gitignore` for security

**Note**: After running `set_env.sh`, you need to source the `.env` file in each new terminal session:
```bash
source .env
```

#### Option 2: Manual Environment Variables
```bash
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_DEFAULT_REGION="il-central-1"
```

#### Option 3: AWS Credentials File
Create `~/.aws/credentials`:
```ini
[default]
aws_access_key_id = your-access-key
aws_secret_access_key = your-secret-key
```

#### Option 4: IAM Roles (for EC2/ECS)
If running on AWS infrastructure, use IAM roles for automatic credential management.

## How to Run the Notebook

### Option 1: Using Jupyter Lab (Recommended)
1. **Install Jupyter Lab**:
   ```bash
   pip install jupyterlab
   ```

2. **Start Jupyter Lab**:
   ```bash
   jupyter lab
   ```

3. **Open the notebook**:
   - Navigate to your project directory
   - Click on `parquet_query.ipynb` to open it
   - The notebook will open in a new tab

### Option 2: Using Jupyter Notebook (Classic)
1. **Install Jupyter Notebook**:
   ```bash
   pip install notebook
   ```

2. **Start Jupyter Notebook**:
   ```bash
   jupyter notebook
   ```

3. **Open the notebook**:
   - Navigate to your project directory
   - Click on `parquet_query.ipynb` to open it

### Option 3: Using VS Code
1. **Install VS Code Jupyter extension**
2. **Open the notebook**:
   - Open VS Code in your project directory
   - Click on `parquet_query.ipynb`
   - The notebook will open with an integrated kernel

### Option 4: Using Google Colab
1. **Upload the notebook**:
   - Go to [Google Colab](https://colab.research.google.com/)
   - Upload `parquet_query.ipynb` or open it from GitHub

2. **Install dependencies**:
   ```python
   !pip install duckdb pandas boto3 pyarrow s3fs
   ```

### Running the Notebook

1. **Set up AWS credentials** (see AWS Credentials Setup section below)
2. **Source environment variables**:
   ```bash
   source .env
   ```
3. **Activate virtual environment**:
   ```bash
   source venv/bin/activate
   ```
4. **Start Jupyter Lab**:
   ```bash
   jupyter lab
   ```
5. **Execute cells sequentially**:
   - Use `Shift + Enter` to run individual cells
   - Use `Ctrl + Enter` (or `Cmd + Enter` on Mac) to run a cell and stay on it
   - Use `Cell > Run All` to execute the entire notebook

6. **Update S3 paths**:
   - Replace placeholder S3 URIs with your actual bucket and file paths
   - Modify the examples to match your data structure

### Complete Workflow

For a complete setup from scratch:

```bash
# 1. Set up the project environment
python setup.py

# 2. Configure AWS credentials
source set_env.sh

# 3. Quick start (for future sessions)
source .env && source venv/bin/activate && jupyter lab
```

## Using the Notebook

The notebook contains all the examples and functions for querying parquet files from S3.

### Basic Usage Examples

#### 1. Simple S3 Parquet Query with DuckDB
```python
import duckdb

# Connect and configure DuckDB for S3
con = duckdb.connect()
con.execute("INSTALL httpfs")
con.execute("LOAD httpfs")

# Query a parquet file directly from S3
s3_uri = "s3://your-bucket/path/to/file.parquet"
result = con.execute(f"SELECT * FROM '{s3_uri}' LIMIT 10").fetchdf()
print(result)
```

#### 2. Using Boto3 + Pandas
```python
# Use the provided function
bucket_name = "your-bucket"
key = "path/to/file.parquet"
df = read_parquet_from_s3(bucket_name, key)
print(df.head())
```

#### 3. Query Multiple Files
```python
# List parquet files in a bucket prefix
parquet_files = list_and_query_s3_parquet_files("your-bucket", "data/", 5)

# Query all files together
results = query_multiple_parquet_files_s3(parquet_files, "SELECT COUNT(*) FROM parquet_files")
```

## Features

### Available Methods

1. **DuckDB with S3 Support**
   - Direct SQL queries on S3 parquet files
   - No need to download files locally
   - Supports complex joins and aggregations
   - Most efficient for analytical queries

2. **Boto3 + Pandas**
   - Full control over S3 operations
   - Good for smaller files or when you need the raw data
   - Easy to understand and debug

3. **PyArrow Integration**
   - High-performance columnar processing
   - Memory efficient for large datasets
   - Better type handling

4. **S3FS Filesystem**
   - Treats S3 like a local filesystem
   - Seamless integration with pandas/pyarrow
   - Great for exploratory analysis

### Advanced Features

- **Multi-file queries**: Query across multiple parquet files simultaneously
- **Filtering and aggregation**: Built-in functions for data analysis
- **Automatic file discovery**: List and query parquet files in S3 prefixes
- **Error handling**: Robust error handling and informative messages
- **Flexible authentication**: Support for multiple AWS credential methods

## Example Workflows

### Analyzing AIS Data
```python
# Query AIS vessel data with filtering
ais_data = analyze_s3_parquet_data(
    s3_uri="s3://your-bucket/ais-data/2024/01/data.parquet",
    filter_column="vessel_type",
    filter_value="CARGO",
    group_by="mmsi"
)
```

### Batch Processing
```python
# Process multiple files in a date range
date_range = ["2024-01-01", "2024-01-02", "2024-01-03"]
parquet_files = [f"s3://your-bucket/ais-data/{date}/data.parquet" for date in date_range]

# Aggregate across all files
summary = query_multiple_parquet_files_s3(
    parquet_files, 
    "SELECT COUNT(*) as total_records, AVG(speed) as avg_speed FROM parquet_files"
)
```

## Performance Tips

1. **Use DuckDB for analytical queries**: Most efficient for complex SQL operations
2. **Use PyArrow for large files**: Better memory management for big datasets
3. **Filter early**: Apply WHERE clauses to reduce data transfer
4. **Use column selection**: Only select needed columns to minimize I/O
5. **Consider partitioning**: Organize your S3 data in a way that allows partition pruning

## Troubleshooting

### Common Issues

1. **Environment Variables Not Set**
   ```bash
   # Check if variables are set
   echo $AWS_ACCESS_KEY_ID
   
   # If not set, source the .env file
   source .env
   ```

2. **Authentication Errors**
   - Verify AWS credentials are correctly set
   - Check IAM permissions for S3 access
   - Ensure the bucket/object exists and is accessible
   - Test credentials with: `aws sts get-caller-identity`

3. **Script Not Returning to Prompt**
   - Make sure you're sourcing the script: `source set_env.sh`
   - Don't execute it directly: `./set_env.sh` (this won't work)

4. **Memory Issues**
   - Use PyArrow for large files
   - Apply filters to reduce data size
   - Consider processing files in batches

5. **Network Issues**
   - Check internet connectivity
   - Verify S3 bucket region settings
   - Consider using S3 Transfer Acceleration for large files

### Quick Verification Commands

```bash
# Check environment variables
env | grep AWS

# Test AWS credentials
aws sts get-caller-identity

# Check if virtual environment is active
which python

# List installed packages
pip list | grep -E "(duckdb|pandas|boto3|pyarrow)"
```

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License