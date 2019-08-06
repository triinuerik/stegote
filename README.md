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

For every requirement except for jpeg, a free package manager tool is reccomended to use (eg. Anaconda). For the jpeg library, a short installation manual is provided in wiki in French and in its rough translation to English (https://github.com/triinuerik/stegote/wiki/jpeg-library-installation-guide).

## Quick guide

To view a quick user manual of Stegote, navigate to the directory and enter:

```python main.py --help```

<img width="640" alt="Screenshot 2019-07-15 at 12 52 13" src="https://user-images.githubusercontent.com/29357315/62554616-13401b00-b87a-11e9-9a74-f3b4c8296927.png">

### Encoding a message

In order to encode a hidden message into a cover image, enter:

```python main.py --encode```

Answer the prompts to specify the manner of hiding, or use the flags to enter them straight on the command-line.

<img width="584" alt="Screenshot 2019-07-16 at 12 49 17" src="https://user-images.githubusercontent.com/29357315/62554834-83e73780-b87a-11e9-8417-946fdbcb2bed.png">

### Decoding a message

In order to decode a secret image to find the hidden message inside, enter:

```python main.py --decode```

NB! Be careful to decode the message in the same manner as it was encoded. 

### Generating a key

In order to generate a secret key, enter:

```python main.py --generate_key```

<img width="540" alt="Screenshot 2019-07-16 at 10 39 39" src="https://user-images.githubusercontent.com/29357315/62555003-d58fc200-b87a-11e9-974d-9b85dcdb3c1a.png">
