"""
Mini 语言语法分析器安装脚本
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mini-language-parser",
    version="1.0.0",
    author="Compiler Principles Course",
    author_email="",
    description="Mini Language Parser - A complete compiler frontend implementation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Dictatora0/Mini-Language-Parser",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Education",
        "Topic :: Education",
        "Topic :: Software Development :: Compilers",
        "License :: Educational Use Only",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "mini-parser=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt"],
    },
)
