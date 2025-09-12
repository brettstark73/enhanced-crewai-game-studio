#!/usr/bin/env python3
"""
Setup script for CrewAI Framework
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="crewai-framework",
    version="1.0.0",
    author="CrewAI Framework Team",
    author_email="framework@crewai.dev",
    description="A comprehensive framework for building reliable, debuggable CrewAI workflows",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-org/crewai-framework",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=[
        "crewai>=0.177.0",
        "crewai-tools>=0.71.0",
        "langchain-openai>=0.2.0",
        "python-dotenv>=1.0.0",
        "openai>=1.12.0",
        "pydantic>=2.6.1",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "isort>=5.10.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "crewai-validate=crewai_framework.cli:validate_command",
            "crewai-debug=crewai_framework.cli:debug_command",
        ],
    },
    include_package_data=True,
    package_data={
        "crewai_framework": ["templates/*.py", "examples/*.py"],
    },
)