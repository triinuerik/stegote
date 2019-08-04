from secrets import randbelow
from jpeg_compression import image_is_greyscale
import numpy
from numpy import random
from cryptography.fernet import Fernet
import ast
from numpy import r_


zigzag_order_to_coordinates_dictionary = {
    0 : [0, 0], 1 : [0, 1], 2 : [1, 0], 3 : [2, 0], 4 : [1, 1], 5 : [0, 2], 6 : [0, 3], 7 : [1, 2], 8 : [2, 1],
    9 : [3, 0], 10 : [4, 0], 11 : [3, 1], 12 : [2, 2], 13 : [1, 3], 14 : [0, 4], 15 : [0, 5], 16 : [1, 4], 17 : [2, 3],
    18 : [3, 2], 19 : [4, 1], 20 : [5, 0], 21 : [6, 0], 22 : [5, 1], 23 : [4, 2], 24 : [3, 3], 25 : [2, 4], 26 : [1, 5],
    27 : [0, 6], 28 : [0, 7], 29 : [1, 6], 30 : [2, 5], 31 : [3, 4], 32 : [4, 3], 33 : [5, 2], 34 : [6, 1], 35 : [7, 0],
    36 : [7, 1], 37 : [6, 2], 38 : [5, 3], 39 : [4, 4], 40 : [3, 5], 41 : [2, 6], 42 : [1, 7], 43 : [2, 7], 44 : [3, 6],
    45 : [4, 5], 46 : [5, 4], 47 : [6, 3], 48 : [7, 2], 49 : [7, 3], 50 : [6, 4], 51 : [5, 5], 52 : [4, 6], 53 : [3, 7],
    54 : [4, 7], 55 : [5, 6], 56 : [6, 5], 57 : [7, 4], 58 : [7, 5], 59 : [6, 6], 60 : [5, 7], 61 : [6, 7], 62 : [7, 6],
    63 : [7, 7]
}


def generate_key():
    """
    Generates a (symmetric) key for the communicating partners to use in encoding/decoding.
    NB! Exchange this key in a secure and secret manner and do not lose it!

    Returns:
        bytes: The secret key.
    """

    return Fernet.generate_key()


def is_sufficient_dct_space(image, message):
    """
    Checks if the cover image in compressed form (quantized DCT coefficients) is big enough to hide the message. That
    means, there have to be more non-zero DCT coefficients than the bits in the message.

    Args:
        image (numpy.ndarray): The cover image in compressed form where the message will be hidden.
        message (str): The secret message to hide.

    Returns:
        bool: True if there is sufficient space, False if not and throws an IndexError if there is not enough space.
    """

    non_zero_coefficients = numpy.count_nonzero(image)
    if len(message) > non_zero_coefficients:
        IndexError("The message is too long to be embedded in this cover image!")
        return False
    return True


def is_sufficient_image_space(image, message):
    """
    Checks if the cover image in uncompressed form (regular plain image) is big enough to hide the message. That
    means, there have to be more pixels than the bits in the message.

    Args:
        image (numpy.ndarray): The cover image in compressed form where the message will be hidden.
        message (str): The secret message to hide.

    Returns:
        bool: True if there is sufficient space, False if not and throws an IndexError if there is not enough space.
    """

    if len(message) > image.size:
        IndexError("The message is too long to be embedded in this cover image!")
        return False
    return True


def generate_path(image, message):
    """
    Generates a simple randomized path to hide a message in a cover image. Uses  a regular uncompressed image not JPEG
    compressed image (doesn't use quantized DCT coefficients). The path needs to be sent to the receiver in order to
    decode the message (in an encrypted manner using encrypt_path()).

    Args:
        image (numpy.ndarray): The cover image where the message will be hidden.
        message (str): The secret message to hide.

    Returns:
        list: The path (list of coordinates) in which order the message is hidden/recovered.
    """

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


def generate_simple_path(image):
    """
    Generates a simple path in the lexicographic order (from left to right, from up to down). Uses  a regular
    uncompressed image not JPEG compressed image (doesn't use quantized DCT coefficients). The path does not need to be
    sent to the communicating partner, as the same path is always created for the same image.

    Args:
        image (numpy.ndarray): The cover image where the message will be hidden.

    Returns:
        list: The path (list of coordinates) in which order the message is hidden/recovered.
    """

    path = list()

    if image_is_greyscale(image):
        for x in range(image.shape[1]):
            for y in range(image.shape[0]):
                path.append([y, x])
    else:
        for z in range(image.shape[2]):
            for x in range(image.shape[1]):
                for y in range(image.shape[0]):
                    path.append([y, x, z])

    return path


def generate_path_from_key(image, key):
    """
    Generates a randomized path using the shared key to hide a message in a cover image. Uses a regular uncompressed
    image not JPEG compressed image (doesn't use quantized DCT coefficients). The path does not need to be sent to the
    communicating partner, as long as they are using a shared key for encoding and decoding.

    Args:
        image (numpy.ndarray): The cover image where the message will be hidden.
        key (bytes): The key shared between the communicating partners (generated by generate_key()).

    Returns:
        list: The path (list of coordinates) in which order the message is hidden/recovered.
    """

    key_y, key_x, key_z = int.from_bytes(key[0:14], byteorder='little'), int.from_bytes(key[15:29], byteorder='little'), \
                          int.from_bytes(key[30:44], byteorder='little')
    key_y, key_x, key_z = int(key_y / 10.e25), int(key_x / 10.e25), int(key_z / 10.e25)

    path = list()
    y_coordinates = numpy.arange(image.shape[0]).tolist()
    random.seed(key_y)
    random.shuffle(y_coordinates)
    x_coordinates = numpy.arange(image.shape[1]).tolist()
    random.seed(key_x)
    random.shuffle(x_coordinates)
    if not image_is_greyscale(image):
        z_coordinates = numpy.arange(image.shape[2]).tolist()
        random.seed(key_z)
        random.shuffle(z_coordinates)

    if image_is_greyscale(image):
        for x in x_coordinates:
            for y in y_coordinates:
                coordinates = [y, x]
                path.append(coordinates)
    else:
        for z in z_coordinates:
            for x in x_coordinates:
                for y in y_coordinates:
                    coordinates = [y, x, z]
                    path.append(coordinates)

    return path


def generate_dct_path(dct_coefficients_image, message):
    """
    Generates a randomized path to hide a message in a cover image. Uses a JPEG compressed image, that means the
    quantized DCT coefficients. The path is only constructed from non-zero coefficients. The path needs to be sent to
    the receiver in order to decode the message (in an encrypted manner using encrypt_path()).

    Args:
        dct_coefficients_image (numpy.ndarray): Quantized DCT coefficients of the cover image.
        message (str): The secret message to hide.

    Returns:
        list: The path (list of coordinates) in which order the message is hidden/recovered.
    """

    path = list()

    for bit in range(len(message)):
        zero_coefficient = True

        while zero_coefficient:
            coordinates = list()
            y = randbelow(dct_coefficients_image.shape[0])
            coordinates.append(y)
            x = randbelow(dct_coefficients_image.shape[1])
            coordinates.append(x)
            if not image_is_greyscale(dct_coefficients_image):
                z = randbelow(dct_coefficients_image.shape[2])
                coordinates.append(z)

            if image_is_greyscale(dct_coefficients_image):
                if dct_coefficients_image[y, x] != 0 and coordinates not in path:
                    path.append(coordinates)
                    zero_coefficient = False
            else:
                if dct_coefficients_image[y, x, z] != 0 and coordinates not in path:
                    path.append(coordinates)
                    zero_coefficient = False

    return path


def generate_zigzag_dct_path(dct_coefficients_image):
    """
    Generates a path in the zigzag order to hide a message in a cover image. Uses a JPEG compressed image, that means
    the quantized DCT coefficients. The path is only constructed from non-zero coefficients.

    Args:
        dct_coefficients_image (numpy.ndarray): Quantized DCT coefficients of the cover image.

    Returns:
        list: The path (list of coordinates) in which order the message is hidden/recovered.
    """

    non_zero_zigzagged_coordinates = list()

    if image_is_greyscale(dct_coefficients_image):
        for x in r_[:dct_coefficients_image.shape[1]:8]:
            for y in r_[:dct_coefficients_image.shape[0]:8]:
                zigzag_array = zigzag(dct_coefficients_image[y:(y + 8), x:(x + 8)])
                block_non_zero_coordinates = find_non_zero_coordinates_greyscale(y, x, zigzag_array)
                non_zero_zigzagged_coordinates.extend(block_non_zero_coordinates)
    else:
        for z in range(dct_coefficients_image.shape[2]):
            for x in r_[:dct_coefficients_image.shape[1]:8]:
                for y in r_[:dct_coefficients_image.shape[0]:8]:
                    zigzag_array = zigzag(dct_coefficients_image[y:(y + 8), x:(x + 8), 0])
                    block_non_zero_coordinates = find_non_zero_coordinates_colour(y, x, z, zigzag_array)
                    non_zero_zigzagged_coordinates.extend(block_non_zero_coordinates)

    return non_zero_zigzagged_coordinates


def generate_dct_path_from_key(dct_coefficients_image, key):
    """
    Generates a randomized path using the shared key to hide a message in a cover image. Uses a JPEG compressed image,
    that means the quantized DCT coefficients. The path is only constructed from non-zero coefficients, which are found
    using the zigzag path generation algorithm. The path does not need to be sent to the communicating partner,
    as long as they are using a shared key for encoding and decoding.

    Args:
        dct_coefficients_image (numpy.ndarray): The cover image where the message will be hidden.
        key (bytes): The key shared between the communicating partners (generated by generate_key()).

    Returns:
        list: The path (list of coordinates) in which order the message is hidden/recovered.
    """

    key = int.from_bytes(key, byteorder='little')
    key = int(key / 10.e100)

    non_zero_zigzagged_coordinates = generate_zigzag_dct_path(dct_coefficients_image)
    path = list()

    random.seed(key)
    random.shuffle(non_zero_zigzagged_coordinates)

    for coordinate in non_zero_zigzagged_coordinates:
        path.append(coordinate)

    return path


def generate_all_available_coordinate_list(cover_image):
    """
    Method  for generating a permutation of all the available coordinates (for hiding) of a cover image.

    Args:
        cover_image (numpy.ndarray): The cover image where the message could be hidden.

    Returns:
        list: The path (list of coordinates) of all the available coordinates for hiding.
    """

    all_available_coordinates = list()

    if image_is_greyscale(cover_image):
        for x in range(len(cover_image[0, :, 0])):
            for y in range(len(cover_image[:, 0, 0])):
                all_available_coordinates.append([y, x])
    else:
        for z in range(len(cover_image[0, 0, :])):
            for x in range(len(cover_image[0, :, 0])):
                for y in range(len(cover_image[:, 0, 0])):
                    all_available_coordinates.append([y, x, z])

    return all_available_coordinates


def encrypt_path(path, key):
    """
    Method for encrypting a path to send to the communicating partner. Uses the Fernet library. The encryption is done
    with a key generated also using the Fernet library (generate_key() method).

    Args:
        path (list):  The path (list of coordinates) in which order the message is hidden/recovered.
        key (bytes): The key shared between the communicating partners (generated by generate_key()).


    Returns:
        bytes: The token to be sent to the communicating partner for decryption.
    """

    fernet = Fernet(key)
    token = fernet.encrypt(bytes(str(path), 'utf-8'))
    return token


def decrypt_path(token, key):
    """
    Method for encrypting a path to send to the communicating partner. Uses the Fernet library. The encryption is done
    with a key generated also using the Fernet library (generate_key() method).

    Args:
        token (bytes):  The token received from the communicating partner for decryption of a path.
        key (bytes): The key shared between the communicating partners (generated by generate_key()).


    Returns:
        list:  The path (list of coordinates) in which order the message is hidden/recovered.
    """
    fernet = Fernet(key)
    path = fernet.decrypt(token)
    path = path.decode("utf-8")
    path = ast.literal_eval(path)
    return path


def zigzag(block):
    """
    Creates a list of coefficients from a block in the zigzag order. That means, transforms a two dimensional array into
    a one dimensional array by the zigzag order.

    Args:
        block (int): A 8x8 pixel block to be rearranged

    Returns:
        list: The coefficients in a one dimensional list arranged in zigzag order.
    """

    zigzag_array = list()
    for i in range(0, 14):
        if i < 8:
            bound = 0
        else:
            bound = i - 7
        for j in range(bound, i - bound + 1):
            if i % 2 == 1:
                zigzag_array.append(block[j, i-j])
            else:
                zigzag_array.append(block[i-j, j])
    zigzag_array.append(block[7, 7])

    return zigzag_array


def find_non_zero_coordinates_colour(y, x, z, zigzag_array):
    """
    Finds the DCT coefficients with non-zero values from a zigzag array and creates a list of their coordinates. This
    function is used for colour images with 3 dimensions.

    Args:
        y (int): Y-coordinate
        x (int): X-coordinate
        z (int): Z-coordinate
        zigzag_array (list): The zigzag array of an 8x8 block.

    Returns:
        list: The coordinates of non-zero DCT coefficients
    """

    coordinates_array = list()

    for i in range(len(zigzag_array)):
        coefficient = zigzag_array[i]
        if coefficient != 0 :
            coordinates = zigzag_order_to_coordinates_dictionary.get(i)
            coordinates_array.append([y + coordinates[0], x + coordinates[1], z])

    return coordinates_array


def find_non_zero_coordinates_greyscale(y, x, zigzag_array):
    """
    Finds the DCT coefficients with non-zero values from a zigzag array and creates a list of their coordinates. This
    function is used for greyscale images with 2 dimensions.

    Args:
        y (int): Y-coordinate
        x (int): X-coordinate
        zigzag_array (list): The zigzag array of an 8x8 block.

    Returns:
        list: The coordinates of non-zero DCT coefficients
    """

    coordinates_array = list()

    for i in range(len(zigzag_array)):
        coefficient = zigzag_array[i]
        if coefficient != 0 :
            coordinates = zigzag_order_to_coordinates_dictionary.get(i)
            coordinates_array.append([y + coordinates[0], x + coordinates[1]])

    return coordinates_array

