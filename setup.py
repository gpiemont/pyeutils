import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyeutils",
    version="0.9",
    author="Giulio Piemontese",
    description="Client-side, Python NCBI EUtils",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/bio.info/NCBI/python-eutils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache License 2.0",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'main': [
            'pyeutils=pyeutils.__main__:main',
        ],
    },
    python_requires='>=3.7',
)
