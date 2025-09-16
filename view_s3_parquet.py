#!/usr/bin/env python3
"""
Script to retrieve a parquet file from S3 and display its first N rows.
Supports both AWS profile and IAM role authentication.
"""

import argparse
import sys
import boto3
import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa
from botocore.exceptions import ClientError, NoCredentialsError
from urllib.parse import urlparse
import logging

def setup_logging():
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def get_s3_client(aws_mode='profile', aws_profile='default', region='il-central-1'):
    """
    Create and return an S3 client with appropriate authentication.
    
    Args:
        aws_mode: Authentication mode - 'profile' or 'role'
        aws_profile: AWS profile name (for profile mode)
        region: AWS region
    
    Returns:
        boto3 S3 client
    """
    try:
        if aws_mode == 'profile':
            session = boto3.Session(profile_name=aws_profile, region_name=region)
            s3_client = session.client('s3')
        elif aws_mode == 'role':
            s3_client = boto3.client('s3', region_name=region)
        else:
            raise ValueError(f"Invalid aws_mode: {aws_mode}. Must be 'profile' or 'role'")
        
        # Test the connection
        s3_client.list_buckets()
        logging.info(f"Successfully connected to S3 using {aws_mode} mode")
        return s3_client
        
    except NoCredentialsError:
        logging.error("AWS credentials not found. Please configure your credentials.")
        sys.exit(1)
    except ClientError as e:
        logging.error(f"Failed to connect to S3: {e}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Unexpected error creating S3 client: {e}")
        sys.exit(1)

def parse_s3_url(s3_url):
    """
    Parse S3 URL to extract bucket and key.
    
    Args:
        s3_url: S3 URL in format s3://bucket/key
        
    Returns:
        tuple: (bucket, key)
    """
    if not s3_url.startswith('s3://'):
        raise ValueError("URL must start with 's3://'")
    
    parsed = urlparse(s3_url)
    bucket = parsed.netloc
    key = parsed.path.lstrip('/')
    
    if not bucket or not key:
        raise ValueError("Invalid S3 URL format. Expected: s3://bucket/key")
    
    return bucket, key

def read_parquet_from_s3(s3_client, bucket, key, max_rows=None):
    """
    Read parquet file from S3 and return as pandas DataFrame.
    
    Args:
        s3_client: boto3 S3 client
        bucket: S3 bucket name
        key: S3 object key
        max_rows: Maximum number of rows to read (None for all)
        
    Returns:
        pandas.DataFrame
    """
    try:
        logging.info(f"Reading parquet file from s3://{bucket}/{key}")
        
        # Read the parquet file from S3
        obj = s3_client.get_object(Bucket=bucket, Key=key)
        
        # Read the entire file content into memory
        file_content = obj['Body'].read()
        
        # Create a BytesIO object for pyarrow
        import io
        file_buffer = io.BytesIO(file_content)
        
        # Read parquet data using pyarrow
        parquet_file = pq.ParquetFile(file_buffer)
        
        # Read the data
        if max_rows:
            table = parquet_file.read(columns=None)  # Read all columns
            # Convert to pandas and limit rows
            df = table.to_pandas()
            df = df.head(max_rows)
        else:
            table = parquet_file.read(columns=None)
            df = table.to_pandas()
        
        logging.info(f"Successfully read parquet file with {len(df)} rows and {len(df.columns)} columns")
        return df
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'NoSuchKey':
            logging.error(f"Parquet file not found: s3://{bucket}/{key}")
        elif error_code == 'NoSuchBucket':
            logging.error(f"S3 bucket not found: {bucket}")
        elif error_code == 'AccessDenied':
            logging.error(f"Access denied to s3://{bucket}/{key}. Check your permissions.")
        else:
            logging.error(f"S3 error: {e}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Error reading parquet file: {e}")
        sys.exit(1)

def display_dataframe_info(df, show_rows=10):
    """
    Display information about the DataFrame and its first N rows.
    
    Args:
        df: pandas DataFrame
        show_rows: Number of rows to display
    """
    print(f"\n{'='*80}")
    print(f"DATAFRAME INFORMATION")
    print(f"{'='*80}")
    print(f"Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
    print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    print(f"\n{'='*80}")
    print(f"COLUMN INFORMATION")
    print(f"{'='*80}")
    print(f"{'Column':<30} {'Type':<15} {'Non-Null Count':<15} {'Null Count':<15}")
    print(f"{'-'*75}")
    for col in df.columns:
        non_null = df[col].count()
        null_count = len(df) - non_null
        print(f"{col:<30} {str(df[col].dtype):<15} {non_null:<15,} {null_count:<15,}")
    
    print(f"\n{'='*80}")
    print(f"FIRST {min(show_rows, len(df))} ROWS")
    print(f"{'='*80}")
    
    # Display first N rows with proper formatting
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', 50)
    
    print(df.head(show_rows).to_string(index=True))
    
    if len(df) > show_rows:
        print(f"\n... and {len(df) - show_rows:,} more rows")

def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description='Retrieve a parquet file from S3 and display its first N rows',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # View first 10 rows of a parquet file
  python view_s3_parquet.py s3://ais-research-data/parquet/year=2016/month=10/day=26/file.parquet

  # View first 50 rows with specific AWS profile
  python view_s3_parquet.py s3://ais-research-data/parquet/year=2016/month=10/day=26/file.parquet --rows 50 --aws-profile myprofile

  # Use IAM role authentication
  python view_s3_parquet.py s3://ais-research-data/parquet/year=2016/month=10/day=26/file.parquet --aws-mode role
        """
    )
    
    parser.add_argument('s3_url', help='S3 URL of the parquet file (e.g., s3://bucket/path/file.parquet)')
    parser.add_argument('--rows', '-r', type=int, default=10, help='Number of rows to display (default: 10)')
    parser.add_argument('--aws-mode', choices=['profile', 'role'], default='profile', 
                       help='AWS authentication mode (default: profile)')
    parser.add_argument('--aws-profile', default='default', 
                       help='AWS profile name for profile mode (default: default)')
    parser.add_argument('--region', default='il-central-1', 
                       help='AWS region (default: il-central-1)')
    parser.add_argument('--verbose', '-v', action='store_true', 
                       help='Enable verbose logging')
    
    args = parser.parse_args()
    
    # Setup logging
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    setup_logging()
    
    try:
        # Parse S3 URL
        bucket, key = parse_s3_url(args.s3_url)
        logging.info(f"Parsed S3 URL: bucket={bucket}, key={key}")
        
        # Create S3 client
        s3_client = get_s3_client(args.aws_mode, args.aws_profile, args.region)
        
        # Read parquet file
        df = read_parquet_from_s3(s3_client, bucket, key, args.rows)
        
        # Display information
        display_dataframe_info(df, args.rows)
        
        logging.info("Script completed successfully")
        
    except KeyboardInterrupt:
        logging.info("Script interrupted by user")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Script failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
