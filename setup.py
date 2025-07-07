#!/usr/bin/env python3
import os

from setuptools import find_packages, setup


# Read the README file for long description
def read_readme():
    """Read README.md for long description"""
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, encoding="utf-8") as fh:
            return fh.read()
    return "ML Systems Evaluation Framework - Industrial AI Reliability Assessment"


# Read requirements
def read_requirements(filename):
    """Read requirements from file"""
    requirements_path = os.path.join(os.path.dirname(__file__), filename)
    if os.path.exists(requirements_path):
        with open(requirements_path, encoding="utf-8") as fh:
            return [
                line.strip() for line in fh if line.strip() and not line.startswith("#")
            ]
    return []


# Package configuration
setup(
    name="ml-eval",
    version="0.1.0",
    author="ML Systems Evaluation Team",
    author_email="team@ml-systems-evaluation.com",
    description="A reliability-focused evaluation framework for Industrial AI systems",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/ml-systems-evaluation/framework",
    project_urls={
        "Bug Tracker": "https://github.com/ml-systems-evaluation/framework/issues",
        "Documentation": "https://ml-systems-evaluation.readthedocs.io/",
        "Source Code": "https://github.com/ml-systems-evaluation/framework",
    },
    packages=find_packages(),
    package_data={
        "ml_eval": [
            "templates/*.yaml",
            "templates/*.yml",
            "examples/*.yaml",
            "examples/*.yml",
        ]
    },
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Manufacturing",
        "Intended Audience :: Aviation",
        "Intended Audience :: Energy",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Reliability",
        "Topic :: System :: Safety",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Framework :: Pytest",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements("requirements.txt"),
    extras_require={
        "test": read_requirements("requirements-test.txt"),
        "dev": [
            "black>=23.7.0",
            "ruff>=0.0.292",
            "pre-commit>=3.3.0",
        ],
        "docs": [
            "sphinx>=7.0.0",
            "sphinx-rtd-theme>=1.3.0",
            "myst-parser>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "ml-eval=ml_eval.cli.main:main",
        ],
    },
    keywords=[
        "machine learning",
        "ml",
        "ai",
        "evaluation",
        "reliability",
        "safety",
        "compliance",
        "industrial",
        "manufacturing",
        "aviation",
        "energy",
        "sre",
        "site reliability engineering",
        "slo",
        "service level objectives",
        "error budget",
        "monitoring",
        "assessment",
    ],
    zip_safe=False,
    platforms=["any"],
    license="MIT",
    license_files=["LICENSE"],
)
