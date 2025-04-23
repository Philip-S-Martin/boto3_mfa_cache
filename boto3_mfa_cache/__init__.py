import os
import boto3
import botocore.session
from botocore.utils import JSONFileCache

def _setup_default_session_patch(**kwargs):
    cli_cache_path = os.environ.get(
        "AWS_CREDENTIAL_CACHE",
        os.path.join(os.path.expanduser("~"), ".aws", "cli", "cache")
    )
    os.makedirs(cli_cache_path, exist_ok=True)
    botocore_session = botocore.session.Session()
    file_cache = JSONFileCache(cli_cache_path)
    botocore_session.get_component("credential_provider").get_provider("assume-role").cache = file_cache
    boto3.DEFAULT_SESSION = boto3.Session(botocore_session=botocore_session, **kwargs)

boto3.setup_default_session = _setup_default_session_patch