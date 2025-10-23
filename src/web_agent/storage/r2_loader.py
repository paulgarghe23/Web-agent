import os
import boto3
import logging
from pathlib import Path
from typing import List

log = logging.getLogger(__name__)

def download_files_from_r2(target_dir: str = "/tmp/data") -> None:
    """
    Download files from Cloudflare R2 bucket to local directory.
    Uses environment variables for credentials.
    """
    # Get credentials from environment
    access_key = os.getenv("R2_ACCESS_KEY")
    secret_key = os.getenv("R2_SECRET_KEY")
    bucket_name = os.getenv("R2_BUCKET")
    endpoint_url = os.getenv("R2_ENDPOINT")
    
    if not all([access_key, secret_key, bucket_name, endpoint_url]):
        raise RuntimeError(
            "Missing R2 credentials. Required: R2_ACCESS_KEY, R2_SECRET_KEY, "
            "R2_BUCKET, R2_ENDPOINT"
        )
    
    # Create S3 client for R2
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        endpoint_url=endpoint_url,
    )
    
    # Files to download from the data/ directory in R2
    files_to_download = [
        "data/Paul_G_CV.pdf",
        "data/context.md",
        "data/work_stories.xlsx",
    ]
    
    # Create target directory if it doesn't exist
    target_path = Path(target_dir)
    target_path.mkdir(parents=True, exist_ok=True)
    
    log.info(f"r2_loader: downloading {len(files_to_download)} files from R2 bucket '{bucket_name}'")
    
    # Download each file
    for file_key in files_to_download:
        # Extract filename from key (e.g., "data/context.md" -> "context.md")
        filename = file_key.split("/")[-1]
        local_path = target_path / filename
        
        try:
            log.info(f"r2_loader: downloading {file_key} -> {local_path}")
            s3_client.download_file(bucket_name, file_key, str(local_path))
            log.info(f"r2_loader: downloaded {filename} successfully")
        except Exception as e:
            log.error(f"r2_loader: failed to download {file_key}: {e}")
            raise
    
    log.info(f"r2_loader: all files downloaded to {target_dir}")

