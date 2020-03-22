import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", 'r') as req:
    req_list = req.read().split()

setuptools.setup(
    name="rmidi",
    version="0.0.31",
    # scripts = ['MIDI.py', 'mutils.py', 'rmidi.py', 'sound.py'],
    packages= setuptools.find_packages(), # ['rmidi', 'rmidi.constant', 'rmidi.dataset'],
    author="rushike",
    author_email="rushike.ab1@gmail.com",
    description="Math Sequence to MIDI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rushike/rmidipy",
    install_requires=req_list,#['numpy'],
    # packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)