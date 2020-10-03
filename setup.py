import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python_eutils",
    version="0.0.1",
    author="Giulio Piemontese",
    description="Client-side, Python NCBI EUtils",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/bio.info/NCBI/python_eutils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache License 2.0",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'main': [
            'python_eutils=python_eutils.__main__:main',
        ],
    },
    python_requires='>=3.7',
)
