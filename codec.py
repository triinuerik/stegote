from jpeg_compression import *
from lsb_embedding import *
from path_generating import *
from bitarray import bitarray


def jpeg_zigzag_encode(cover_image, message):
    """
    Method for hiding a message into a JPEG compressed image using zigzag encoding and LSB matching.

    Args:
        cover_image (numpy.ndarray): Cover image into where to hide the data.
        message (string): Secret message in bits.

    Returns:
        numpy.ndarray: The encoded cover image where the message is hidden.
    """

    if is_sufficient_dct_space(cover_image, message):
        if image_is_greyscale(cover_image):
            compressed_image = compress_greyscale_image(cover_image)
            encoding_path = generate_zigzag_dct_path(compressed_image)
            encoded_image = lsb_matching_greyscale_dct_encode(compressed_image, message, encoding_path)
        else:
            compressed_image = compress_colour_image(cover_image)
            encoding_path = generate_zigzag_dct_path(compressed_image)
            encoded_image = lsb_matching_colour_dct_encode(compressed_image, message, encoding_path)

        return encoded_image


def jpeg_zigzag_decode(encoded_image):
    """
    Method for recovering a message from a JPEG compressed image using zigzag encoding.

    Args:
        encoded_image (numpy.ndarray): Encoded image with the hidden data.

    Returns:
        string: The hidden message in text form.
    """

    if image_is_greyscale(encoded_image):
        compressed_image = compress_greyscale_image(encoded_image)
        encoding_path = generate_zigzag_dct_path(compressed_image)
        text_binary = lsb_embedding_greyscale_decode(compressed_image, encoding_path)
    else:
        compressed_image = compress_colour_image(encoded_image)
        encoding_path = generate_zigzag_dct_path(compressed_image)
        text_binary = lsb_embedding_colour_decode(compressed_image, encoding_path)

    return bits_to_text(text_binary)


def jpeg_key_encode_matching(cover_image, message, key):
    """
    Method for hiding a message into a JPEG compressed image using a shared secret key for encoding and LSB matching.

    Args:
        cover_image (numpy.ndarray): Cover image into where to hide the data.
        message (string): Secret message in bits.
        key (bytes): Shared secret key used for encoding/decoding.

    Returns:
        numpy.ndarray: The encoded cover image where the message is hidden.
    """

    if is_sufficient_dct_space(cover_image, message):
        if image_is_greyscale(cover_image):
            compressed_image = compress_greyscale_image(cover_image)
            encoding_path = generate_dct_path_from_key(compressed_image, key)
            encoded_image = lsb_matching_greyscale_dct_encode(compressed_image, message, encoding_path)
        else:
            compressed_image = compress_colour_image(cover_image)
            encoding_path = generate_dct_path_from_key(compressed_image, key)
            encoded_image = lsb_matching_colour_dct_encode(compressed_image, message, encoding_path)

        return encoded_image


def jpeg_key_encode_replacement(cover_image, message, key):
    """
    TODO: Does not work yet, use the method with LSB matching instead.
    Method for hiding a message into a JPEG compressed image using a shared secret key for encoding and LSB replacement.

    Args:
        cover_image (numpy.ndarray): Cover image into where to hide the data.
        message (string): Secret message in bits.
        key (bytes): Shared secret key used for encoding/decoding.

    Returns:
        numpy.ndarray: The encoded cover image where the message is hidden.
    """

    if is_sufficient_dct_space(cover_image, message):
        if image_is_greyscale(cover_image):
            compressed_image = compress_greyscale_image(cover_image)
            encoding_path = generate_dct_path_from_key(compressed_image, key)
            encoded_image = lsb_replacement_greyscale_encode(compressed_image, message, encoding_path)
        else:
            compressed_image = compress_colour_image(cover_image)
            encoding_path = generate_dct_path_from_key(compressed_image, key)
            encoded_image = lsb_replacement_colour_encode(compressed_image, message, encoding_path)

        return encoded_image


def jpeg_key_decode(encoded_image, key):
    """
    Method for recovering a message from a JPEG compressed image using secret key encoding.

    Args:
        encoded_image (numpy.ndarray): Encoded image with the hidden data.
        key (bytes): Shared secret key used for encoding/decoding.

    Returns:
        string: The hidden message in text form.
    """

    if image_is_greyscale(encoded_image):
        compressed_image = compress_greyscale_image(encoded_image)
        encoding_path = generate_dct_path_from_key(compressed_image, key)
        text_binary = lsb_embedding_greyscale_decode(compressed_image, encoding_path)
    else:
        compressed_image = compress_colour_image(encoded_image)
        encoding_path = generate_dct_path_from_key(compressed_image, key)
        text_binary = lsb_embedding_colour_decode(compressed_image, encoding_path)

    return bits_to_text(text_binary)


def jpeg_path_encode_matching(cover_image, message, key):
    """
    Method for hiding a message into a JPEG compressed image using encrypted path encoding and LSB matching.

    Args:
        cover_image (numpy.ndarray): Cover image into where to hide the data.
        message (string): Secret message in bits.
        key (bytes): Shared secret key used for encoding/decoding.

    Returns:
        numpy.ndarray: The encoded cover image where the message is hidden.
        bytes: The encrypted token of the coordinate path.
    """

    if is_sufficient_dct_space(cover_image, message):
        if image_is_greyscale(cover_image):
            compressed_image = compress_greyscale_image(cover_image)
            encoding_path = generate_dct_path(cover_image, message)
            encrypted_path = encrypt_path(encoding_path, key)
            encoded_image = lsb_matching_greyscale_dct_encode(compressed_image, message, encoding_path)
        else:
            compressed_image = compress_colour_image(cover_image)
            encoding_path = generate_dct_path(cover_image, message)
            encrypted_path = encrypt_path(encoding_path, key)
            encoded_image = lsb_matching_colour_dct_encode(compressed_image, message, encoding_path)

        return encoded_image, encrypted_path


def jpeg_path_encode_replacement(cover_image, message, key):
    """
    Method for hiding a message into a JPEG compressed image using encrypted path encoding and LSB replacement.

    Args:
        cover_image (numpy.ndarray): Cover image into where to hide the data.
        message (string): Secret message in bits.
        key (bytes): Shared secret key used for encoding/decoding.

    Returns:
        numpy.ndarray: The encoded cover image where the message is hidden.
        bytes: The encrypted token of the coordinate path.
    """

    if is_sufficient_dct_space(cover_image, message):
        if image_is_greyscale(cover_image):
            compressed_image = compress_greyscale_image(cover_image)
            encoding_path = generate_dct_path(cover_image, message)
            path_token = encrypt_path(encoding_path, key)
            encoded_image = lsb_replacement_greyscale_encode(compressed_image, message, encoding_path)
        else:
            compressed_image = compress_colour_image(cover_image)
            encoding_path = generate_dct_path(cover_image, message)
            path_token = encrypt_path(encoding_path, key)
            encoded_image = lsb_replacement_colour_encode(compressed_image, message, encoding_path)

        return encoded_image, path_token


def jpeg_path_decode(encoded_image, key, path_token):
    """
    Method for recovering a message from a JPEG compressed image using the encrypted path token.

    Args:
        encoded_image (numpy.ndarray): Encoded image with the hidden data.
        key (bytes): Shared secret key used for encoding/decoding.
        path_token (bytes): The encrypted token of the coordinate path.

    Returns:
        string: The hidden message in text form.
    """

    if image_is_greyscale(encoded_image):
        compressed_image = compress_greyscale_image(encoded_image)
        encoding_path = decrypt_path(path_token, key)
        text_binary = lsb_embedding_greyscale_decode(compressed_image, encoding_path)
    else:
        compressed_image = compress_colour_image(encoded_image)
        encoding_path = decrypt_path(path_token, key)
        text_binary = lsb_embedding_colour_decode(compressed_image, encoding_path)

    return bits_to_text(text_binary)


def image_simple_encode_replacement(cover_image, message):
    """
    Method for hiding a message into a plain image using simple encoding and LSB replacement.

    Args:
        cover_image (numpy.ndarray): Cover image into where to hide the data.
        message (string): Secret message in bits.

    Returns:
        numpy.ndarray: The encoded cover image where the message is hidden.
    """

    if is_sufficient_image_space(cover_image, message):
        encoding_path = generate_simple_path(cover_image)
        if image_is_greyscale(cover_image):
            encoded_image = lsb_replacement_greyscale_encode(cover_image, message, encoding_path)
        else:
            encoded_image = lsb_replacement_colour_encode(cover_image, message, encoding_path)

        return encoded_image


def image_simple_encode_matching(cover_image, message):
    """
    Method for hiding a message into a plain image using simple encoding and LSB matching.

    Args:
        cover_image (numpy.ndarray): Cover image into where to hide the data.
        message (string): Secret message in bits.

    Returns:
        numpy.ndarray: The encoded cover image where the message is hidden.
    """

    if is_sufficient_image_space(cover_image, message):
        encoding_path = generate_simple_path(cover_image)
        if image_is_greyscale(cover_image):
            encoded_image = lsb_matching_greyscale_encode(cover_image, message, encoding_path)
        else:
            encoded_image = lsb_matching_colour_encode(cover_image, message, encoding_path)

        return encoded_image


def image_simple_decode(encoded_image):
    """
    Method for recovering a message from a plain image using simple encoding.

    Args:
        encoded_image (numpy.ndarray): Encoded image with the hidden data.

    Returns:
        string: The hidden message in text form.
    """

    encoding_path = generate_simple_path(encoded_image)
    if image_is_greyscale(encoded_image):
        text_binary = lsb_embedding_greyscale_decode(encoded_image, encoding_path)
    else:
        text_binary = lsb_embedding_colour_decode(encoded_image, encoding_path)

    return bits_to_text(text_binary)


def image_key_encode_replacement(cover_image, message, key):
    """
    Method for hiding a message into a plain image using a shared secret key for encoding and LSB replacement.

    Args:
        cover_image (numpy.ndarray): Cover image into where to hide the data.
        message (string): Secret message in bits.
        key (bytes): Shared secret key used for encoding/decoding.

    Returns:
        numpy.ndarray: The encoded cover image where the message is hidden.
    """

    encoding_path = generate_path_from_key(cover_image, key)
    if is_sufficient_image_space(cover_image, message):
        if image_is_greyscale(cover_image):
            encoded_image = lsb_replacement_greyscale_encode(cover_image, message, encoding_path)
        else:
            encoded_image = lsb_replacement_colour_encode(cover_image, message, encoding_path)

        return encoded_image


def image_key_encode_matching(cover_image, message, key):
    """
    Method for hiding a message into a plain image using a shared secret key for encoding and LSB matching.

    Args:
        cover_image (numpy.ndarray): Cover image into where to hide the data.
        message (string): Secret message in bits.
        key (bytes): Shared secret key used for encoding/decoding.

    Returns:
        numpy.ndarray: The encoded cover image where the message is hidden.
    """

    encoding_path = generate_path_from_key(cover_image, key)
    if is_sufficient_image_space(cover_image, message):
        if image_is_greyscale(cover_image):
            encoded_image = lsb_matching_greyscale_encode(cover_image, message, encoding_path)
        else:
            encoded_image = lsb_matching_colour_encode(cover_image, message, encoding_path)

        return encoded_image


def image_key_decode(encoded_image, key):
    """
    Method for recovering a message from a plain image using secret key encoding.

    Args:
        encoded_image (numpy.ndarray): Encoded image with the hidden data.
        key (bytes): Shared secret key used for encoding/decoding.

    Returns:
        string: The hidden message in text form.
    """

    encoding_path = generate_path_from_key(encoded_image, key)
    if image_is_greyscale(encoded_image):
        text_binary = lsb_embedding_greyscale_decode(encoded_image, encoding_path)
    else:
        text_binary = lsb_embedding_colour_decode(encoded_image, encoding_path)

    return bits_to_text(text_binary)


def image_path_encode_replacement(cover_image, message, key):
    """
    Method for hiding a message into a plain image using encrypted path encoding and LSB replacement.

    Args:
        cover_image (numpy.ndarray): Cover image into where to hide the data.
        message (string): Secret message in bits.
        key (bytes): Shared secret key used for encoding/decoding.

    Returns:
        numpy.ndarray: The encoded cover image where the message is hidden.
        bytes: The encrypted token of the coordinate path.
    """

    encoding_path = generate_path(cover_image, message)
    path_token = encrypt_path(encoding_path, key)

    if is_sufficient_image_space(cover_image, message):
        if image_is_greyscale(cover_image):
            encoded_image = lsb_replacement_greyscale_encode(cover_image, message, encoding_path)
        else:
            encoded_image = lsb_replacement_colour_encode(cover_image, message, encoding_path)

        return encoded_image, path_token


def image_path_encode_matching(cover_image, message, key):
    """
    Method for hiding a message into a plain image using encrypted path encoding and LSB matching.

    Args:
        cover_image (numpy.ndarray): Cover image into where to hide the data.
        message (string): Secret message in bits.
        key (bytes): Shared secret key used for encoding/decoding.

    Returns:
        numpy.ndarray: The encoded cover image where the message is hidden.
        bytes: The encrypted token of the coordinate path.
    """

    encoding_path = generate_path(cover_image, message)
    path_token = encrypt_path(encoding_path, key)

    if is_sufficient_image_space(cover_image, message):
        if image_is_greyscale(cover_image):
            encoded_image = lsb_matching_greyscale_encode(cover_image, message, encoding_path)
        else:
            encoded_image = lsb_matching_colour_encode(cover_image, message, encoding_path)

        return encoded_image, path_token


def image_path_decode(encoded_image, key, path_token):
    """
    Method for recovering a message from a plain image using the encrypted path token.

    Args:
        encoded_image (numpy.ndarray): Encoded image with the hidden data.
        key (bytes): Shared secret key used for encoding/decoding.
        path_token (bytes): The encrypted token of the coordinate path.

    Returns:
        string: The hidden message in text form.
    """

    encoding_path = decrypt_path(path_token, key)
    if image_is_greyscale(encoded_image):
        text_binary = lsb_embedding_greyscale_decode(encoded_image, encoding_path)
    else:
        text_binary = lsb_embedding_colour_decode(encoded_image, encoding_path)

    return bits_to_text(text_binary)


def text_to_bits(text):
    """
    Method to convert a string of text into a string of equivalent bits.

    Args:
        text (string): Text to be converted to bits

    Returns:
        string: Text as an array of bits.
    """

    bit_array = bitarray()
    bit_array.frombytes(text.encode("utf-8"))
    return bit_array.to01()


def bits_to_text(bits):
    """
    Method to convert a string of bits to a string of equivalent characters forming a text.

    Args:
        bits (string): Bits to be converted to text.

    Returns:
        string: Bits as a string of text (bytes).
    """

    bit_array = bitarray(bits)
    bits = bit_array.tobytes()
    return bits.decode("utf-8", errors="ignore")
