import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="codis_crawler",
    version="0.2.1",
    author="David Ho",
    author_email="davidho@gapp.nthu.edu.tw",
    description="This is a selenium based web crawler. This crawler aim to download the weather data from CODiS platform.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10.0',
    install_requires=[
        "click==8.1.7",
        "httpx==0.27.0",
        "selenium==4.18.1",
        "webdriver-manager==4.0.1",
    ]
)
