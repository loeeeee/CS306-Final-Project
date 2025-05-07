from setuptools import setup, find_packages

setup(
    name="diary_kivy_app",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "kivy>=2.2.1",
        "plyer>=2.1.0",
    ],
    python_requires=">=3.12",
    author="Your Name",
    author_email="your.email@example.com",
    description="A multi-platform diary application with metadata collection",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.12",
    ],
) 