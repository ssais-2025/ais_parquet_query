# AIS Parquet Query

Query parquet files from Amazon S3 using multiple methods.

## Quick Start

### Setup
```bash
# 1. Set up the project environment
python setup.py

# 2. Configure AWS credentials (first time only)
source set_env.sh

# 3. Quick start (for future sessions)
source .env && source venv/bin/activate && jupyter lab
```

## Installation (CLI only)

### Automated Setup
```bash
python setup.py
```

### Manual Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Jupyter
pip install jupyterlab

# Start Jupyter
jupyter lab
```

## AWS Credentials

### First Time Setup
```bash
source set_env.sh
```

### Future Sessions (if set_env.sh was run already)
```bash
source .env
```

### Manual Setup
```bash
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_DEFAULT_REGION="il-central-1"
```

## Usage

Open `parquet_query.ipynb` in Jupyter Lab and run the cells to query parquet files from S3.

## Troubleshooting

```bash
# Check environment variables
env | grep AWS

# Test AWS credentials
aws sts get-caller-identity

# Check virtual environment
which python

# Verify packages
pip list | grep -E "(duckdb|pandas|boto3|pyarrow)"
```