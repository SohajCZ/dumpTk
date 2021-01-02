import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="qtinter",
    version="0.0.1",
    author="Matěj Schuh",
    author_email="schuhmat@fit.cvut.cz",
    license='MIT',
    description="Interface for Tkinter to use Qt toolkit.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SohajCZ/dumpTk",
    packages=['qtinter'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    zip_safe=False,
)
