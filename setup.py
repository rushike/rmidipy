import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", 'r') as req:
    req_list = req.read().split()

setuptools.setup(
    name="rmidi",
    version="0.0.36",
    # scripts = ['MIDI.py', 'mutils.py', 'rmidi.py', 'sound.py'],
    packages= setuptools.find_packages(), # ['rmidi', 'rmidi.constant', 'rmidi.dataset'],
    author="rushike",
    author_email="rushike.ab1@gmail.com",
    description="Math Sequence to MIDI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rushike/rmidipy",
    install_requires=['astroid==2.3.3', 'colorama==0.4.3', 'cycler==0.10.0', 'isort==4.3.21', 'kiwisolver==1.1.0', 'lazy-object-proxy==1.4.3', 'matplotlib==3.2.0', 'mccabe==0.6.1', 'numpy==1.18.1', 'pylint==2.4.4', 'pyparsing==2.4.6', 'python-dateutil==2.8.1', 'six==1.14.0', 'typed-ast==1.4.1', 'wrapt==1.11.2'],
    # packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)