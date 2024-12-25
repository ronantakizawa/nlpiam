from setuptools import setup, find_packages

setup(
    name="nlpiam",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "boto3>=1.26.0",
        "openai>=1.0.0",
        "python-dotenv>=0.19.0",
        "click>=8.0.0",
    ],
    entry_points={
        'console_scripts': [
            'nlpiam=nlpiam.cli:main',
        ],
    },
    python_requires=">=3.8",
)