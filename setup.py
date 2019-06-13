import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rmidi",
    version="0.0.4",
    # scripts = ['MIDI.py', 'mutils.py', 'rmidi.py', 'sound.py'],
    author="rushike",
    author_email="rushike.ab1@gmail.com",
    description="Math Sequence to MIDI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rushike/rmidipy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)