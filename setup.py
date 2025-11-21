"""
bAUTO Setup Script
==================

AI-powered browser automation framework.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="bauto",
    version="1.0.0",
    author="bAUTO Contributors",
    description="AI-powered browser automation framework with natural language instructions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SwintexD/bAUTO",
    packages=find_packages(exclude=["tests", "tests.*", "docs", "examples"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "selenium>=4.15.0",
        "webdriver-manager>=4.0.0",
        "google-generativeai>=0.3.0",
        "python-dotenv>=1.0.0",
        "click>=8.1.0",
        "pyyaml>=6.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.12.0",
            "pytest-timeout>=2.2.0",
            "pytest-xdist>=3.5.0",
            "black>=23.0.0",
            "ruff>=0.1.0",
            "mypy>=1.7.0",
            "pre-commit>=3.5.0",
        ],
        "docs": [
            "sphinx>=7.2.0",
            "sphinx-rtd-theme>=2.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "bauto=bauto.cli:cli",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    project_urls={
        "Bug Reports": "https://github.com/SwintexD/bAUTO/issues",
        "Source": "https://github.com/SwintexD/bAUTO",
        "Documentation": "https://github.com/SwintexD/bAUTO#readme",
    },
)
