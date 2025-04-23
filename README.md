## Boto3 MFA Cache

This package patches boto3 to use the AWS CLI credential cache. This uses the same cache as the AWS CLI, 
which is stored in `~/.aws/cli/cache`. This allows you to use MFA with boto3 without having to 
enter your credentials every time. The environment variable AWS_CREDENTIAL_CACHE can be set to a 
different path if `~/.aws/cli/cache` is not what you want to use.

This pull is the primary reference for this package: https://github.com/boto/botocore/pull/1338

## Best Practices

This is designed for use with role-assumption based MFA. That's you if your `~/.aws/config` looks something like this:

```ini
[default]
role_arn = arn:aws:iam::123456789012:role/MyRole
source_profile = base
region = us-east-2
mfa_serial = arn:aws:iam::123456789012:mfa/my-device
duration_seconds = 43200
```

This project is only useful on development environments that require MFA. Servers and other automated resources
should not require MFA, and thus should not require this package.

```bash
python -m pip install boto3-mfa-cache
```

## Methodology

The patch works by loading a .pth file that imports a monkeypatch replacing `boto3.setup_default_session`
with a patched version. The patched version applies the JSONFileCache from botocore (also used by the CLI)
to the default credential provider.

```python
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
```
