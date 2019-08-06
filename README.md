# Stegote

This tool was created as a Bachelor's thesis.

STEGANOGRAPHY TOOL FOR HIDING INFORMATION IN JPEG AND PNG IMAGES

TalTech 2019

Stegote is a simple command-line tool to hide data into digital images. What sets it apart from others is that YOU can choose in which manner the data will be hidden into the image. It is possible to choose between two image formats (JPEG and PNG), two embedding methods (LSB replacement and LSB matching) and three path generation algorithms (simple, secret key or path token)!

To use the tool, the following libraries and packages needs to be installed:
* jpeg (http://www.ifs.schaathun.net/pysteg/starting.html) - for creating JPEG images
* PIL (https://pillow.readthedocs.io/en/stable/installation.html) - Python imaging library
* NumPy and SciPy (https://www.scipy.org/scipylib/download.html) - for scientific computations
* Bitarray (https://pypi.org/project/bitarray/) - for bit to byte conversions
* Secrets and Fernet from the Cryptography library (https://cryptography.io/en/latest/installation/) - for cryptography and secret key generation

For every requirement except for jpeg, a free package manager tool is reccomended to use (eg. Anaconda). For the jpeg library, a short installation manual is provided in French and in its rough translation to English.

## Quick guide

To view a quick user manual of Stegote, navigate to the directory and enter:

```python main.py --help```









