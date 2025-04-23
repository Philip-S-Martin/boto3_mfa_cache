import os
from setuptools import setup
from setuptools.command.build_py import build_py as _build_py
from pathlib import Path

class build_py_with_pth(_build_py):
    """Include our .pth file in the wheel/sdist’s build_lib."""
    def run(self):
        super().run()
        src_pth = os.path.join(os.path.dirname(__file__), "boto3_mfa_cache_patch.pth")
        dst_pth = os.path.join(self.build_lib, "boto3_mfa_cache_patch.pth")
        self.copy_file(src_pth, dst_pth, preserve_mode=False)

setup(
    name="boto3-mfa-cache",
    version="1.0.0",
    author="Philip Martin",
    description="""A patch for boto3 to use the AWS CLI credential cache. This uses 
    the same cache as the AWS CLI.""",
    long_description=Path("README.md").read_text(),
    long_description_content_type='text/markdown',
    packages=["boto3_mfa_cache"],
    cmdclass={"build_py": build_py_with_pth},
    requires=["boto3", "botocore"],
    include_package_data=True,
)

