import numpy
from numpy import random


def lsb_replacement_colour_encode(cover_image, message, path):
    """
    LSB embedding using LSB replacement method. The LSB of a value is changed either to 0 or 1 to match the secret
    message. Is used for colour images.

    Args:
        cover_image (numpy.ndarray): Cover image into where to hide the data.
        message (string): Secret message in bits.
        path (list): Path of coordinates where to hide the data.

    Returns:
        numpy.ndarray: The encoded cover image where the message is hidden.

    """

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
    """
    LSB embedding using LSB replacement method. The LSB of a value is changed either to 0 or 1 to match the secret
    message. Is used for greyscale images.

    Args:
        cover_image (numpy.ndarray): Cover image into where to hide the data.
        message (string): Secret message in bits.
        path (list): Path of coordinates where to hide the data.

    Returns:
        numpy.ndarray: The encoded cover image where the message is hidden.

    """

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
    """
    Method for decoding messages hidden using any kind of LSB embedding. Used for decoding colour images.

    Args:
        encoded_image (numpy.ndarray): Cover image into where the message is hidden.
        path (list): Path of coordinates where to hide the data.

    Returns:
        string: The hidden message in bits.

    """

    message = list()
    for coordinates in path:
        y, x, z = coordinates[0], coordinates[1], coordinates[2]
        message.append(int(encoded_image[y, x, z]) & 1)

    return ''.join(str(char) for char in message)


def lsb_embedding_greyscale_decode(encoded_image, path):
    """
    Method for decoding messages hidden using any kind of LSB embedding. Used for decoding greyscale images.

    Args:
        encoded_image (numpy.ndarray): Cover image into where the message is hidden.
        path (list): Path of coordinates where to hide the data.

    Returns:
        string: The hidden message in bits.

    """

    message = list()

    for coordinates in path:
        y, x = coordinates[0], coordinates[1]
        message.append(int(encoded_image[y, x]) & 1)

    return ''.join(str(char) for char in message)


def lsb_matching_colour_encode(cover_image, message, path):
    """
    LSB embedding using LSB matching method. The LSB of a value is either increased or decreased to match the secret
    message. The decision of increasing/decreasing is done randomly. Edge cases (0 and 255) are handled separately.
    Is used for plain colour images.

    Args:
        cover_image (numpy.ndarray): Cover image into where to hide the data.
        message (string): Secret message in bits.
        path (list): Path of coordinates where to hide the data.

    Returns:
        numpy.ndarray: The encoded cover image where the message is hidden.

    """

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
                cover_image[y, x, z] += sign
    except IndexError:
        pass

    return cover_image


def lsb_matching_greyscale_encode(cover_image, message, path):
    """
    LSB embedding using LSB matching method. The LSB of a value is either increased or decreased to match the secret
    message. The decision of increasing/decreasing is done randomly. Edge cases (0 and 255) are handled separately.
    Is used for plain greyscale images.

    Args:
        cover_image (numpy.ndarray): Cover image into where to hide the data.
        message (string): Secret message in bits.
        path (list): Path of coordinates where to hide the data.

    Returns:
        numpy.ndarray: The encoded cover image where the message is hidden.

    """

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
                cover_image[y, x] += sign
    except IndexError:
        pass

    return cover_image


def lsb_matching_colour_dct_encode(cover_image, message, path):
    """
    LSB embedding using LSB matching method. The LSB of a value is either increased or decreased to match the secret
    message. The decision of increasing/decreasing is done randomly. Is used for JPEG colour images. Because the
    coefficient values cannot change to 0, then edge cases (1 and -1) are handled separately.

    Args:
        cover_image (numpy.ndarray): Cover image into where to hide the data.
        message (string): Secret message in bits.
        path (list): Path of coordinates where to hide the data.

    Returns:
        numpy.ndarray: The encoded cover image where the message is hidden.

    """

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
                cover_image[y, x, z] += sign
    except IndexError:
        pass

    return cover_image


def lsb_matching_greyscale_dct_encode(cover_image, message, path):
    """
    LSB embedding using LSB matching method. The LSB of a value is either increased or decreased to match the secret
    message. The decision of increasing/decreasing is done randomly. Is used for JPEG greyscale images. Because the
    coefficient values cannot change to 0, then edge cases (1 and -1) are handled separately.

    Args:
        cover_image (numpy.ndarray): Cover image into where to hide the data.
        message (string): Secret message in bits.
        path (list): Path of coordinates where to hide the data.

    Returns:
        numpy.ndarray: The encoded cover image where the message is hidden.

    """

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
                cover_image[y, x] += sign
    except IndexError:
        pass

    return cover_image
