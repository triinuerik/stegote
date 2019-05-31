from bitarray import bitarray
from jpeg_compression import *
from lsb_embedding import *
from path_generating import *


def jpeg_zigzag_encode(cover_image, message):
    if is_sufficient_dct_space(cover_image, message):
        if image_is_greyscale(cover_image):
            compressed_image = compress_greyscale_image(cover_image)
            encoding_path = generate_zigzag_dct_path(compressed_image)
            encoded_image = lsb_matching_greyscale_dct_encode(compressed_image, message, encoding_path)
            jpeg_image = decompress_greyscale_image(encoded_image)
        else:
            compressed_image = compress_colour_image(cover_image)
            encoding_path = generate_zigzag_dct_path(compressed_image)
            encoded_image = lsb_matching_colour_dct_encode(compressed_image, message, encoding_path)
            jpeg_image = decompress_colour_image(encoded_image)

        return jpeg_image


def jpeg_zigzag_decode(encoded_image):
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
    if is_sufficient_dct_space(cover_image, message):
        if image_is_greyscale(cover_image):
            compressed_image = compress_greyscale_image(cover_image)
            encoding_path = generate_dct_path_from_key(compressed_image, key)
            encoded_image = lsb_matching_greyscale_dct_encode(compressed_image, message, encoding_path)
            jpeg_image = decompress_greyscale_image(encoded_image)
        else:
            compressed_image = compress_colour_image(cover_image)
            encoding_path = generate_dct_path_from_key(compressed_image, key)
            encoded_image = lsb_matching_colour_dct_encode(compressed_image, message, encoding_path)
            jpeg_image = decompress_colour_image(encoded_image)

        return jpeg_image


def jpeg_key_encode_replacement(cover_image, message, key):
    if is_sufficient_dct_space(cover_image, message):
        if image_is_greyscale(cover_image):
            compressed_image = compress_greyscale_image(cover_image)
            encoding_path = generate_dct_path_from_key(compressed_image, key)
            encoded_image = lsb_replacement_greyscale_encode(compressed_image, message, encoding_path)
            jpeg_image = decompress_greyscale_image(encoded_image)
        else:
            compressed_image = compress_colour_image(cover_image)
            encoding_path = generate_dct_path_from_key(compressed_image, key)
            encoded_image = lsb_replacement_colour_encode(compressed_image, message, encoding_path)
            jpeg_image = decompress_colour_image(encoded_image)

        return jpeg_image


def jpeg_key_decode(encoded_image, key):
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
    if is_sufficient_dct_space(cover_image, message):
        if image_is_greyscale(cover_image):
            compressed_image = compress_greyscale_image(cover_image)
            encoding_path = generate_dct_path(cover_image, message)
            encrypted_path = encrypt_path(encoding_path, key)
            encoded_image = lsb_matching_greyscale_dct_encode(compressed_image, message, encoding_path)
            jpeg_image = decompress_greyscale_image(encoded_image)
        else:
            compressed_image = compress_colour_image(cover_image)
            encoding_path = generate_dct_path(cover_image, message)
            encrypted_path = encrypt_path(encoding_path, key)
            encoded_image = lsb_matching_colour_dct_encode(compressed_image, message, encoding_path)
            jpeg_image = decompress_colour_image(encoded_image)

        return jpeg_image, encrypted_path


def jpeg_path_encode_replacement(cover_image, message, key):
    if is_sufficient_dct_space(cover_image, message):
        if image_is_greyscale(cover_image):
            compressed_image = compress_greyscale_image(cover_image)
            encoding_path = generate_dct_path(cover_image, message)
            path_token = encrypt_path(encoding_path, key)
            encoded_image = lsb_replacement_greyscale_encode(compressed_image, message, encoding_path)
            jpeg_image = decompress_greyscale_image(encoded_image)
        else:
            compressed_image = compress_colour_image(cover_image)
            encoding_path = generate_dct_path(cover_image, message)
            path_token = encrypt_path(encoding_path, key)
            encoded_image = lsb_replacement_colour_encode(compressed_image, message, encoding_path)
            jpeg_image = decompress_colour_image(encoded_image)

        return jpeg_image, path_token


def jpeg_path_decode(encoded_image, key, path_token):
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
    if is_sufficient_image_space(cover_image, message):
        encoding_path = generate_simple_path(cover_image)
        if image_is_greyscale(cover_image):
            encoded_image = lsb_replacement_greyscale_encode(cover_image, message, encoding_path)
        else:
            encoded_image = lsb_replacement_colour_encode(cover_image, message, encoding_path)

        return encoded_image


def image_simple_encode_matching(cover_image, message):
    if is_sufficient_image_space(cover_image, message):
        encoding_path = generate_simple_path(cover_image)
        if image_is_greyscale(cover_image):
            encoded_image = lsb_matching_greyscale_encode(cover_image, message, encoding_path)
        else:
            encoded_image = lsb_matching_colour_encode(cover_image, message, encoding_path)

        return encoded_image


def image_simple_decode(encoded_image):
    encoding_path = generate_simple_path(encoded_image)
    if image_is_greyscale(encoded_image):
        text_binary = lsb_embedding_greyscale_decode(encoded_image, encoding_path)
    else:
        text_binary = lsb_embedding_colour_decode(encoded_image, encoding_path)

    return bits_to_text(text_binary)


def image_key_encode_replacement(cover_image, message, key):
    encoding_path = generate_path_from_key(cover_image, key)
    if is_sufficient_image_space(cover_image, message):
        if image_is_greyscale(cover_image):
            encoded_image = lsb_replacement_greyscale_encode(cover_image, message, encoding_path)
        else:
            encoded_image = lsb_replacement_colour_encode(cover_image, message, encoding_path)

        return encoded_image


def image_key_encode_matching(cover_image, message, key):
    encoding_path = generate_path_from_key(cover_image, key)
    if is_sufficient_image_space(cover_image, message):
        if image_is_greyscale(cover_image):
            encoded_image = lsb_matching_greyscale_encode(cover_image, message, encoding_path)
        else:
            encoded_image = lsb_matching_colour_encode(cover_image, message, encoding_path)

        return encoded_image


def image_key_decode(encoded_image, key):
    encoding_path = generate_path_from_key(encoded_image, key)
    if image_is_greyscale(encoded_image):
        text_binary = lsb_embedding_greyscale_decode(encoded_image, encoding_path)
    else:
        text_binary = lsb_embedding_colour_decode(encoded_image, encoding_path)

    return bits_to_text(text_binary)


def image_path_encode_replacement(cover_image, message, key):
    encoding_path = generate_path(cover_image, message)
    path_token = encrypt_path(encoding_path, key)

    if is_sufficient_image_space(cover_image, message):
        if image_is_greyscale(cover_image):
            encoded_image = lsb_replacement_greyscale_encode(cover_image, message, encoding_path)
        else:
            encoded_image = lsb_replacement_colour_encode(cover_image, message, encoding_path)

        return encoded_image, path_token


def image_path_encode_matching(cover_image, message, key):
    encoding_path = generate_path(cover_image, message)
    path_token = encrypt_path(encoding_path, key)

    if is_sufficient_image_space(cover_image, message):
        if image_is_greyscale(cover_image):
            encoded_image = lsb_matching_greyscale_encode(cover_image, message, encoding_path)
        else:
            encoded_image = lsb_matching_colour_encode(cover_image, message, encoding_path)

        return encoded_image, path_token


def image_path_decode(encoded_image, key, path_token):
    encoding_path = decrypt_path(path_token, key)
    if image_is_greyscale(encoded_image):
        text_binary = lsb_embedding_greyscale_decode(encoded_image, encoding_path)
    else:
        text_binary = lsb_embedding_colour_decode(encoded_image, encoding_path)

    return bits_to_text(text_binary)


def text_to_bits(text):
    bit_array = bitarray()
    bit_array.frombytes(text.encode("utf-8"))
    return bit_array.to01()


def bits_to_text(bits):
    bit_array = bitarray(bits)
    bits = bit_array.tobytes()
    return bits.decode(encoding='UTF-8', errors='ignore')
