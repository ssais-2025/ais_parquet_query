#!/bin/bash

# AWS Environment Setup Script for AIS Parquet Query
# This script sets up AWS credentials and region for the project

# Ensure we're being sourced
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    echo "⚠️  This script should be sourced, not executed directly"
    echo "   Use: source set_env.sh"
    echo "   Or: . set_env.sh"
    return 1 2>/dev/null || exit 1
fi

echo "🚀 Setting up AWS environment for AIS Parquet Query..."
echo "Region: il-central-1 (Israel Central)"
echo ""

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to prompt for AWS credentials
prompt_credentials() {
    echo "Please enter your AWS credentials:"
    echo ""
    
    echo -n "AWS Access Key ID: "
    read aws_access_key_id
    
    echo -n "AWS Secret Access Key: "
    read -s aws_secret_access_key
    echo ""
    
    echo -n "AWS Session Token (optional, leave blank if not using temporary credentials): "
    read aws_session_token
    echo ""
    
    # Validate required fields
    if [ -z "$aws_access_key_id" ] || [ -z "$aws_secret_access_key" ]; then
        echo "❌ Error: AWS Access Key ID and Secret Access Key are required"
        return 1
    fi
}

# Function to set environment variables
set_env_vars() {
    echo "Setting AWS environment variables..."
    
    export AWS_ACCESS_KEY_ID="$aws_access_key_id"
    export AWS_SECRET_ACCESS_KEY="$aws_secret_access_key"
    export AWS_DEFAULT_REGION="il-central-1"
    
    # Set session token if provided
    if [ -n "$aws_session_token" ]; then
        export AWS_SESSION_TOKEN="$aws_session_token"
    fi
    
    # Additional AWS configurations
    export AWS_DEFAULT_OUTPUT="json"
    
    echo "✅ Environment variables set successfully!"
}

# Function to create .env file
create_env_file() {
    echo ""
    echo -n "Would you like to create a .env file for future use? (y/n): "
    read create_env
    echo ""
    
    if [[ $create_env =~ ^[Yy]$ ]]; then
        cat > .env << EOF
# AWS Configuration for AIS Parquet Query
AWS_ACCESS_KEY_ID=$aws_access_key_id
AWS_SECRET_ACCESS_KEY=$aws_secret_access_key
AWS_DEFAULT_REGION=il-central-1
AWS_DEFAULT_OUTPUT=json
EOF
        
        if [ -n "$aws_session_token" ]; then
            echo "AWS_SESSION_TOKEN=$aws_session_token" >> .env
        fi
        
        echo "✅ .env file created successfully!"
        echo "   You can source this file in the future with: source .env"
        echo "   ⚠️  Remember to add .env to your .gitignore file!"
        
        # Check if .gitignore exists and add .env if not present
        if [ -f .gitignore ]; then
            if ! grep -q "^\.env$" .gitignore; then
                echo "" >> .gitignore
                echo "# Environment variables" >> .gitignore
                echo ".env" >> .gitignore
                echo "✅ Added .env to .gitignore"
            fi
        else
            echo "# Environment variables" > .gitignore
            echo ".env" >> .gitignore
            echo "✅ Created .gitignore with .env entry"
        fi
    fi
}

# Function to verify AWS credentials
verify_credentials() {
    echo ""
    echo "Verifying AWS credentials..."
    
    if command_exists aws; then
        if aws sts get-caller-identity >/dev/null 2>&1; then
            echo "✅ AWS credentials are valid!"
            echo ""
            echo "Account information:"
            aws sts get-caller-identity
            return 0
        else
            echo "⚠️  AWS credentials verification failed"
            echo "   This could be due to:"
            echo "   - Incorrect credentials"
            echo "   - Network connectivity issues"
            echo "   - Insufficient permissions"
            echo ""
            echo "   You can still proceed - credentials will be set in environment"
            echo "   Test them later with: aws sts get-caller-identity"
            return 1
        fi
    else
        echo "⚠️  AWS CLI not found. Cannot verify credentials."
        echo "   Install AWS CLI: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html"
        echo "   Or use: brew install awscli"
        echo ""
        echo "   Credentials are still set in environment for use with Python libraries"
        return 1
    fi
}

# Function to show usage instructions
show_usage() {
    echo ""
    echo "🎉 Setup complete! Next steps:"
    echo ""
    echo "1. Activate your virtual environment:"
    echo "   source venv/bin/activate"
    echo ""
    echo "2. Start Jupyter Lab:"
    echo "   jupyter lab"
    echo ""
    echo "3. Open parquet_query.ipynb and start querying!"
    echo ""
    echo "4. To use these environment variables in future sessions:"
    echo "   source set_env.sh"
    echo ""
    echo "💡 Quick start command:"
    echo "   source venv/bin/activate && jupyter lab"
}

# Main execution
main() {
    
    # Check if AWS credentials are already set
    if [ -n "$AWS_ACCESS_KEY_ID" ] && [ -n "$AWS_SECRET_ACCESS_KEY" ]; then
        echo "AWS credentials are already set in the environment"
        echo "Current region: ${AWS_DEFAULT_REGION:-'not set'}"
        echo ""
        echo -n "Would you like to update them? (y/n): "
        read update_creds
        
        if [[ ! $update_creds =~ ^[Yy]$ ]]; then
            echo "Using existing AWS credentials..."
            export AWS_DEFAULT_REGION="il-central-1"
            export AWS_DEFAULT_OUTPUT="json"
            verify_credentials
            show_usage
            return 0
        fi
    fi
    
    # Prompt for credentials
    if ! prompt_credentials; then
        echo "❌ Failed to get valid credentials"
        return 1
    fi
    
    # Set environment variables
    set_env_vars
    
    # Create .env file if requested
    create_env_file
    
    # Verify credentials (non-blocking)
    verify_credentials
    
    # Show usage instructions
    show_usage
    
    # Ensure script completes and returns to prompt
    return 0
}

# Run main function
main
