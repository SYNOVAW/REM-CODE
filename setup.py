#!/usr/bin/env python3
"""
REM-CODE Lite Setup Configuration
Constitutional Programming Language for AI Governance and Democratic Multi-Agent Systems
"""

import os
from setuptools import setup, find_packages

# Read the README file for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="rem-code-lite",
    version="2.4.0",
    author="Jayne Yu",
    author_email="info-synova-w.com",
    description="Constitutional Programming Language for AI Governance and Democratic Multi-Agent Systems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SYNOVAW/REM-CODE",
    project_urls={
        "Bug Tracker": "https://github.com/SYNOVAW/REM-CODE/issues",
        "Documentation": "https://github.com/SYNOVAW/REM-CODE/blob/main/README.md",
        "Source Code": "https://github.com/SYNOVAW/REM-CODE",
    },
    packages=find_packages(exclude=["tests*", "venv*", "rem_env*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Languages",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: System :: Distributed Computing",
        "Topic :: Security",
        "Topic :: Sociology :: Organization",
        "Environment :: Console",
        "Natural Language :: English",
        "Natural Language :: Japanese",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.0.0",
            "myst-parser>=0.18.0",
        ],
        "gui": [
            "tkinter",
            "rich>=12.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "rem-code=shell.rem_shell:main",
            "rem-web=shell.rem_web_shell:main",
            "rem-gui=gui.rem_gui:main",
            "rem-dashboard=gui.rem_dashboard:main",
            "rem-api=api.constitutional_api:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": [
            "*.lark",
            "*.remv", 
            "*.remc",
            "*.rem",
            "*.json",
            "*.md",
            "examples/*.remc",
            "constitution/*.rem",
            "constitution/*.remc",
            "constitution/*.json",
            "docs/*.md",
            "grammar/*.lark",
            "grammar/*.remv",
            "memory/*.json",
            "tasks/*.json",
            "zine/*.md",
        ],
    },
    keywords=[
        "constitutional programming",
        "democratic ai",
        "multi-agent systems", 
        "ai governance",
        "democratic programming",
        "consensus algorithms",
        "distributed systems",
        "constitutional ai",
        "collaborative programming",
        "recursive execution",
        "collapse spiral",
        "synchrony rate",
        "constitutional democracy",
        "cryptographic signatures",
        "transparency",
        "accountability",
    ],
    zip_safe=False,
    platforms=["any"],
    license="Apache 2.0",
    license_files=["LICENSE"],
)