from setuptools import setup, find_packages

setup(
    name="nlp-iam-manager",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "boto3>=1.26.0",
        "spacy>=3.5.0",
        "python-dotenv>=0.19.0",
    ],
    extras_require={
        "dev": ["pytest>=7.0.0"],
    },
    python_requires=">=3.8",
)