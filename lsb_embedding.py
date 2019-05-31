import numpy
from numpy import random


def lsb_replacement_colour_encode(cover_image, message, path):
    message = list(message)

    try:
        for coordinates in path:
            y, x, z = coordinates[0], coordinates[1], coordinates[2]
            message_bit = message.pop(0)
            if int(cover_image[y, x, z]) & 1 != message_bit:
                if int(message_bit) == 1:
                    cover_image[y, x, z] = int(cover_image[y, x, z]) | 1
                else:
                    cover_image[y, x, z] = int(cover_image[y, x, z]) & ~ 1
    except IndexError:
        pass

    return cover_image


def lsb_replacement_greyscale_encode(cover_image, message, path):
    message = list(message)

    try:
        for coordinates in path:
            y, x = coordinates[0], coordinates[1]
            message_bit = message.pop(0)
            if int(cover_image[y, x]) & 1 != message_bit:
                if int(message_bit) == 1:
                    cover_image[y, x] = int(cover_image[y, x]) | 1
                else:
                    cover_image[y, x] = int(cover_image[y, x]) & ~ 1
    except IndexError:
        pass

    return cover_image


def lsb_embedding_colour_decode(encoded_image, path):
    message = list()
    for coordinates in path:
        y, x, z = coordinates[0], coordinates[1], coordinates[2]
        message.append(int(encoded_image[y, x, z]) & 1)

    return ''.join(str(char) for char in message)


def lsb_embedding_greyscale_decode(encoded_image, path):
    message = list()

    for coordinates in path:
        y, x = coordinates[0], coordinates[1]
        message.append(int(encoded_image[y, x]) & 1)

    return ''.join(str(char) for char in message)


def lsb_matching_colour_encode(cover_image, message, path):
    message = list(message)

    try:
        for coordinates in path:
            y, x, z = coordinates[0], coordinates[1], coordinates[2]
            message_bit = message.pop(0)
            pixel_lsb = int(cover_image[y, x, z]) & 1

            if int(message_bit) != pixel_lsb:
                sign = random.choice([-1, 1])
                if cover_image[y, x, z] == 255:
                    sign = -1
                if cover_image[y, x, z] == 0:
                    sign = +1
                # add or subtract 1 from the LSB
                cover_image[y, x, z] = int(bin(int(numpy.binary_repr(int(cover_image[y, x, z])), 2) + sign), 2)
    except IndexError:
        pass

    return cover_image


def lsb_matching_greyscale_encode(cover_image, message, path):
    message = list(message)

    try:
        for coordinates in path:
            y, x = coordinates[0], coordinates[1]
            message_bit = message.pop(0)
            pixel_lsb = int(cover_image[y, x]) & 1

            if int(message_bit) != pixel_lsb:
                sign = random.choice([-1, 1])
                if cover_image[y, x] == 255:
                    sign = -1
                if cover_image[y, x] == 0:
                    sign = +1
                # add or subtract 1 from the binary value of the pixel
                cover_image[y, x] = int(bin(int(numpy.binary_repr(int(cover_image[y, x])), 2) + sign), 2)
    except IndexError:
        pass

    return cover_image


def lsb_matching_colour_dct_encode(cover_image, message, path):
    message = list(message)

    try:
        for coordinates in path:
            y, x, z = coordinates[0], coordinates[1], coordinates[2]
            message_bit = message.pop(0)
            pixel_lsb = int(cover_image[y, x, z]) & 1

            if int(message_bit) != pixel_lsb:
                sign = random.choice([-1, 1])
                if cover_image[y, x, z] == 1:
                    sign = +1
                if cover_image[y, x, z] == -1:
                    sign = -1
                # add or subtract 1 from the LSB
                cover_image[y, x, z] = int(bin(int(numpy.binary_repr(int(cover_image[y, x, z])), 2) + sign), 2)
    except IndexError:
        pass

    return cover_image


def lsb_matching_greyscale_dct_encode(cover_image, message, path):
    message = list(message)

    try:
        for coordinates in path:
            y, x = coordinates[0], coordinates[1]
            message_bit = message.pop(0)
            pixel_lsb = int(cover_image[y, x]) & 1

            if int(message_bit) != pixel_lsb:
                sign = random.choice([-1, 1])
                if cover_image[y, x] == 1:
                    sign = +1
                if cover_image[y, x] == -1:
                    sign = -1
                # add or subtract 1 from the binary value of the pixel
                cover_image[y, x] = int(bin(int(numpy.binary_repr(int(cover_image[y, x])), 2) + sign), 2)
    except IndexError:
        pass

    return cover_image
