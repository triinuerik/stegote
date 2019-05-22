import os
import jpeg_compression
from bitarray import bitarray
from jpeg_compression import *
from lsb_embedding import *
from scipy import misc
from scipy.misc import toimage


def compress_and_encode_greyscale_image():
    compressed_image = compress_greyscale_image(image)
    jpeg_image = decompress_greyscale_image(compressed_image)
    return lsb_replacement_random_greyscale_encode(jpeg_image, message, encoding_path)


def compress_and_encode_colour_image():
    compressed_image = compress_colour_image(image)
    jpeg_image = decompress_colour_image(compressed_image)
    return lsb_replacement_random_colour_encode(jpeg_image, message, encoding_path)


def text_to_bits(text):
    bit_array = bitarray()
    bit_array.frombytes(text.encode("utf-8"))
    return bit_array.to01()


def bits_to_text(bits):
    bit_array = bitarray(bits)
    bits = bit_array.tobytes()
    return bits


if __name__ == '__main__':
    message = input("Input: ")
    message = text_to_bits(message)

    file_path = os.path.join(os.path.dirname(__file__), "images/i7.jpg")
    image = misc.imread(file_path).astype(float)

    quality_factor = 100
    jpeg_compression.quantization_luminance_matrix = calculate_quantization_luminance_matrix(quality_factor)
    jpeg_compression.quantization_chrominance_matrix = calculate_quantization_chrominance_matrix(quality_factor)

    if image_is_unconventional_size(image):
        image = crop_image(image)

    key = generate_key()
    encoding_path = generate_path_from_key(image, message, key)
    print(encoding_path)

    if image_is_greyscale(image):
        result = compress_and_encode_greyscale_image()
        text_binary = lsb_replacement_random_greyscale_decode(result, encoding_path)
    else:
        result = compress_and_encode_colour_image()
        text_binary = lsb_replacement_random_colour_decode(result, encoding_path)

    text = bits_to_text(text_binary)
    print(text)
    #toimage(result).show()
