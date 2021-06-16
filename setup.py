import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='supermarktconnector',
    version='0.5',
    author="Bart Machielsen",
    author_email="bartmachielsen@gmail.com",
    description="Collecting product information from Dutch supermarkets: Albert Heijn and Jumbo",
    long_description=long_description,
    install_requires=[
        'requests'
    ],
    long_description_content_type="text/markdown",
    url="https://github.com/bartmachielsen/SupermarktConnector",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
