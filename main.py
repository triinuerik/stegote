import os
from scipy import misc
from scipy.misc import toimage, imsave, imread
import imageio
import jpeg_compression
from codec import *
from path_generating import *
import argparse
import sys
from PIL import Image
import jpeg as jpeg


def write_token():
    file = open(str(destination_path) + "/path_token.txt", "w")
    file.write(path_token.decode("utf-8"))
    file.close()
    print("Path token can be found in: ", str(destination_path) + "/path_token.txt")


def write_secret_message(secret_message):
    file = open(str(os.path.dirname(path)) + "/secret_message.txt", "w")
    file.write(secret_message)
    file.close()
    print("Secret message can be found in: ", str(os.path.dirname(path)) + "/secret_message.txt")


def save_jpeg(secret_image, destination_path, file_name):
    if image_is_greyscale(secret_image):
        img = numpy.zeros([secret_image.shape[0], secret_image.shape[1]], dtype=numpy.uint8)
    else:
        img = numpy.zeros([secret_image.shape[0], secret_image.shape[1], secret_image.shape[2]], dtype=numpy.uint8)
    img.fill(0)
    img = Image.fromarray(img)
    img.save("temp.jpg", subsampling=0)
    file = jpeg.jpeg("temp.jpg")
    for i in r_[:secret_image.shape[0]:8]:
        for j in r_[:secret_image.shape[1]:8]:
            if image_is_greyscale(secret_image):
                file.coef_arrays[0][i:(i + 8), j:(j + 8)] = secret_image[i:(i + 8), j:(j + 8)]
            else:
                file.coef_arrays[0][i:(i + 8), j:(j + 8)] = secret_image[i:(i + 8), j:(j + 8), 0]
                file.coef_arrays[1][i:(i + 8), j:(j + 8)] = secret_image[i:(i + 8), j:(j + 8), 1]
                file.coef_arrays[2][i:(i + 8), j:(j + 8)] = secret_image[i:(i + 8), j:(j + 8), 2]
    file.save(destination_path + "/" + file_name + ".jpg")
    print("Secret image saved to ", destination_path)


def verify_and_initialize():
    global path, secret_message, destination_path, compression, encoding, embedding, secret_key, path_token
    quality = 75
    if not args.encode and not args.decode:
        print("Please try again and input whether you want to encode or decode.")
        sys.exit()
    if args.path is None:
        path = input("Input the path of the cover image: ")
        if not path:
            print("Please try again and input the path for the directory to save the secret image")
            sys.exit()
    else:
        path = args.path
    if args.encode:
        secret_message = input("Input the secret message to hide: ")
        if not secret_message:
            print("The secret message cannot be empty")
            sys.exit()
        secret_message = text_to_bits(secret_message)
        if args.dest_path is None:
            destination_path = input("Input the path of the directory to save the secret image: ")
            if not destination_path:
                print("Please try again and input the path for the directory to save the secret image")
                sys.exit()
        else:
            destination_path = args.dest_path
    if not args.compression:
        compression = input(
            "Do you want to JPEG compress the image (press Enter for default)? [y/n] ")
    else:
        compression = args.compression
    if not compression:
        compression = "n"
    if compression not in ["y", "n"]:
        print("Please try again and input a correct option for JPEG compression")
        sys.exit()
    if not args.encoding:
        encoding = input("Do you want to use SIMPLE encoding, encoding using a KEY or encoding using a PATH token"
                         " encrypted with the shared key? (press Enter for default)? [s/k/p] ")
    else:
        encoding = args.encoding
    if not encoding:
        encoding = "s"
    if encoding not in ["s", "k", "p"]:
        print("Please try again and input a correct option for the encoding method")
        sys.exit()
    if args.encode and (not (compression == "y" and encoding == "s") or not (compression == "y" and encoding == "k")):
        if not args.embedding:
            embedding = input(
                "Do you want to use LSB REPLACEMENT embedding or LSB MATCHING embedding? (press Enter for default)? [r/m] ")
        else:
            embedding = args.embedding
        if not embedding:
            embedding = "m"
        if embedding not in ["m", "r"]:
            print("Please try again and input a correct option for the embedding method")
            sys.exit()
    if encoding == "k" or encoding == "p":
        if not args.key:
            secret_key = input("Input the secret key: ")
        else:
            secret_key = args.key
        secret_key = secret_key.encode("utf-8")
        if not secret_key:
            print("Please try again and input the secret key")
            sys.exit()
    if args.decode and encoding == "p":
        if not args.path_token:
            path_token_path = input("Input the file path for the path token for decoding: ")
        else:
            path_token_path = args.path_token
        if not path_token_path:
            print("Please try again and input the file path")
            sys.exit()
        file = open(path_token_path, "r")
        path_token = file.read()
        path_token = path_token.encode("utf-8")
        file.close()
    if compression == "y":
        # quality_factor = int(quality)
        # TODO implement matrix calculation for other qualities too
        jpeg_compression.quantization_luminance_matrix = calculate_quantization_luminance_matrix(75)
        jpeg_compression.quantization_chrominance_matrix = calculate_quantization_chrominance_matrix(75)


def encode():
    global secret_image, path_token
    if compression == "y":
        if encoding == "s":
            secret_image = jpeg_zigzag_encode(cover_image, secret_message)
            print("Secret JPEG image encoded with zigzag encoding.")

        elif encoding == "k":
            secret_image = jpeg_key_encode_matching(cover_image, secret_message, secret_key)
            print("Secret JPEG image encoded using the shared secret key")

        elif encoding == "p":
            if embedding == "m":
                secret_image, path_token = jpeg_path_encode_matching(cover_image, secret_message, secret_key)
                print("Secret JPEG image encoded using the path token encrypted with the shared secret key using LSB matching")

            elif embedding == "r":
                secret_image, path_token = jpeg_path_encode_replacement(cover_image, secret_message, secret_key)
                print("Secret JPEG image encoded using the path token encrypted with the shared secret key using LSB replacement")
            write_token()

    elif compression == "n":
        if encoding == "s":
            if embedding == "m":
                secret_image = image_simple_encode_matching(cover_image, secret_message)
                print("Secret image encoded using simple encoding and LSB matching")
            elif embedding == "r":
                secret_image = image_simple_encode_replacement(cover_image, secret_message)
                print("Secret image encoded using simple encoding and LSB replacement")

        elif encoding == "k":
            if embedding == "m":
                secret_image = image_key_encode_matching(cover_image, secret_message, secret_key)
                print("Secret image encoded using the shared secret key and LSB matching")
            elif embedding == "r":
                secret_image = image_key_encode_replacement(cover_image, secret_message, secret_key)
                print("Secret image encoded using the shared secret key and LSB replacement")

        elif encoding == "p":
            if embedding == "m":
                secret_image, path_token = image_path_encode_matching(cover_image, secret_message, secret_key)
                print("Secret image encoded using the path token encrypted with the shared secret key using LSB matching")
            elif embedding == "r":
                secret_image, path_token = image_path_encode_replacement(cover_image, secret_message, secret_key)
                print("Secret image encoded using the path token encrypted with the shared secret key using LSB replacement")
            write_token()
    try:
        if compression == "y":
            save_jpeg(secret_image, destination_path, "secret_image")
        elif compression == "n":
            imageio.imwrite(str(destination_path) + "/secret_image.png", secret_image.astype(numpy.uint8))
    except FileNotFoundError:
        print("The destination folder to save the secret image does not exist. Please verify your path")
        sys.exit()
    except PermissionError:
        print("You do not have permission to save to the entered destination folder. Please verify your path")
        sys.exit()


def decode():
    global secret_message
    if compression == "y":
        if encoding == "s":
            secret_message = jpeg_zigzag_decode(cover_image)
            print("Secret message decoded from JPEG image using zigzag decoding.")
        elif encoding == "k":
            secret_message = jpeg_key_decode(cover_image, secret_key)
            print("Secret message decoded from JPEG image using the shared secret key.")
        elif encoding == "p":
            secret_message = jpeg_path_decode(cover_image, secret_key, path_token)
            print("Secret message decoded from JPEG image using the path token encrypted with the shared secret key.")
    elif compression == "n":
        if encoding == "s":
            secret_message = image_simple_decode(cover_image)
            print("Secret message decoded from the image using the simple decoding.")
        elif encoding == "k":
            secret_message = image_key_decode(cover_image, secret_key)
            print("Secret message decoded from the image using the shared secret key.")
        elif encoding == "p":
            secret_message = image_path_decode(cover_image, secret_key, path_token)
            print("Secret message decoded from the image using the path token encrypted with the shared secret key.")
    if encoding == "p":
        print("Secret message: ", secret_message)
    elif encoding == "s" or encoding == "k":
        write_secret_message(secret_message)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Application for hiding messages in images. Bachelor thesis 2019')
    parser.add_argument('--path',
                        help="Path of the cover image")
    parser.add_argument('--dest_path',
                        help="Destination folder path to save the secret image")
    parser.add_argument('--generate_key',
                        help="Enter this argument to generate a secret key.",
                        action='store_true')
    parser.add_argument('--encode',
                        help="Enter this argument to encode a message into an image.",
                        action='store_true')
    parser.add_argument('--decode',
                        help="Enter this argument to decode a message from an image.",
                        action='store_true')
    parser.add_argument('--compression',
                        help="Enter this argument if you want to specify whether you want to hide the message in a"
                             "JPEG compressed image or not. [y/n] for YES or NO",
                        action='store_true')
    parser.add_argument('--embedding',
                        help="Enter this argument if you want to specify the embedding strategy. [r/m] for LSB "
                             "REPLACEMENT of LSB MATCHING.",
                        action='store_true')
    parser.add_argument('--encoding',
                        help="Enter this argument if you want to specify the encoding. [s/k/p] for SIMPLE encoding, "
                             "encoding using a shared KEY or encoding using a PATH token encrypted with the shared key.",
                        action='store_true')
    parser.add_argument('--key',
                        help="Enter this argument if you need to use a secret key. Enter the key. ",
                        action='store_true')
    parser.add_argument('--path_token',
                        help="Enter this argument if you need to use a path token. Enter the token path. ",
                        action='store_true')
    args = parser.parse_args(sys.argv[1:])

    try:
        if args.generate_key:
            print("Your shared secret key is: ", generate_key().decode("utf-8"))
            print("Share this key with the person you wish to send messages to. Don't lose it!")
            sys.exit()

        verify_and_initialize()

        try:
            cover_image = imageio.imread(path).astype(float)
        except FileNotFoundError:
            print("This file for the cover image does not exist. Please verify your path")
            sys.exit()
        except ValueError:
            print("It was not possible to read the file. Please verify your input.")
            sys.exit()

        if image_is_unconventional_size(cover_image):
            cover_image = crop_image(cover_image)

        if args.encode:
            encode()
        elif args.decode:
            decode()
    except KeyboardInterrupt:
        pass
