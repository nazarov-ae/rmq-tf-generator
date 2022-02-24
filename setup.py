import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rmq-tf-generator",
    version="0.0.1",
    author="pik-software",
    author_email="no-reply@pik-software.ru",
    description="Util for generate terraform config for rabbitmq",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pik-software/rmq-tf-generator",
    project_urls={
        "Bug Tracker": "https://github.com/pik-software/rmq-tf-generator/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
