from secrets import randbelow, token_hex
from jpeg_compression import image_is_greyscale
from numpy import random


def generate_key():
    return token_hex(6)


def generate_path(image, message):
    path = list()
    for bit in range(len(message)):
        coordinates = list()
        y = randbelow(image.shape[0])
        coordinates.append(y)
        x = randbelow(image.shape[1])
        coordinates.append(x)
        if not image_is_greyscale(image):
            z = randbelow(image.shape[2])
            coordinates.append(z)
        path.append(coordinates)
    return path


def generate_path_from_key(image, message, key):
    path = list()
    key_y, key_x, key_z = int(key[0:3], 16), int(key[4:7], 16), int(key[8:11], 16)  # translating the hex key

    random.seed(key_y)
    y_coordinates = random.randint(0, image.shape[0], len(message)).tolist()
    random.seed(key_x)
    x_coordinates = random.randint(0, image.shape[1], len(message)).tolist()
    random.seed(key_z)
    z_coordinates = random.randint(0, image.shape[2], len(message)).tolist()

    for bit in range(len(message)):
        if not image_is_greyscale(image):
            coordinates = [y_coordinates.pop(0), x_coordinates.pop(0), z_coordinates.pop(0)]
        else:
            coordinates = [y_coordinates.pop(0), x_coordinates.pop(0)]
        path.append(coordinates)
    return path


def lsb_replacement_simple_colour_encode(compressed_image, message):
    message = list(message)
    try:
        for z in range(len(compressed_image[0, 0, :])):
            for x in range(len(compressed_image[0, :, 0])):
                for y in range(len(compressed_image[:, 0, 0])):
                    message_bit = message.pop(0)
                    if int(message_bit) == 1:
                        compressed_image[y, x, z] = int(compressed_image[y, x, z]) | 1  # change the LSB to 1
                    else:
                        compressed_image[y, x, z] = int(compressed_image[y, x, z]) & ~ 1  # change the LSB to 0
    except IndexError:
        pass
    return compressed_image


def lsb_replacement_simple_greyscale_encode(compressed_image, message):
    message = list(message)
    try:
        for x in range(len(compressed_image[0, :, 0])):
            for y in range(len(compressed_image[:, 0, 0])):
                message_bit = message.pop(0)
                if int(message_bit) == 1:
                    compressed_image[y, x] = int(compressed_image[y, x]) | 1  # change the LSB to 1
                else:
                    compressed_image[y, x] = int(compressed_image[y, x]) & ~ 1  # change the LSB to 0
    except IndexError:
        pass
    return compressed_image


def lsb_replacement_simple_colour_decode(encoded_image):
    message = list()
    try:
        for z in range(len(encoded_image[0, 0, :])):
            for x in range(len(encoded_image[0, :, 0])):
                for y in range(len(encoded_image[:, 0, 0])):
                    message.append(int(encoded_image[y, x, z]) & 1)
    except IndexError:
        pass
    return ''.join(str(char) for char in message)


def lsb_replacement_simple_greyscale_decode(encoded_image):
    message = list()
    try:
        for x in range(len(encoded_image[0, :, 0])):
            for y in range(len(encoded_image[:, 0, 0])):
                message.append(int(encoded_image[y, x]) & 1)
    except IndexError:
        pass
    return ''.join(str(char) for char in message)


def lsb_replacement_random_colour_encode(compressed_image, message, path):
    message = list(message)
    for coordinates in path:
        y, x, z = coordinates[0], coordinates[1], coordinates[2]
        message_bit = message.pop(0)
        if int(message_bit) == 1:
            compressed_image[y, x, z] = int(compressed_image[y, x, z]) | 1  # change the LSB to 1
        else:
            compressed_image[y, x, z] = int(compressed_image[y, x, z]) & ~ 1  # change the LSB to 0
    return compressed_image


def lsb_replacement_random_greyscale_encode(compressed_image, message, path):
    message = list(message)
    for coordinates in path:
        y, x = coordinates[0], coordinates[1]
        message_bit = message.pop(0)
        if int(message_bit) == 1:
            compressed_image[y, x] = int(compressed_image[y, x]) | 1  # change the LSB to 1
        else:
            compressed_image[y, x] = int(compressed_image[y, x]) & ~ 1  # change the LSB to 0
    return compressed_image


def lsb_replacement_random_colour_decode(encoded_image, path):
    message = list()
    for coordinates in path:
        y, x, z = coordinates[0], coordinates[1], coordinates[2]
        message.append(int(encoded_image[y, x, z]) & 1)
    return ''.join(str(char) for char in message)


def lsb_replacement_random_greyscale_decode(encoded_image, path):
    message = list()
    for coordinates in path:
        y, x = coordinates[0], coordinates[1]
        message.append(int(encoded_image[y, x]) & 1)
    return ''.join(str(char) for char in message)
