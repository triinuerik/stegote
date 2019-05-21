from bitarray import bitarray
from random import randint
import scipy
from scipy import misc
from scipy.ndimage import imread
from scipy.misc import toimage
from scipy.fftpack import dct, idct
from PIL import Image
from numpy import r_
import matplotlib.pyplot as plt
import numpy
import os


quantization_luminance_matrix = numpy.array([
  [16,  11,  10,  16,  24,  40,  51,  61],
  [12,  12,  14,  19,  26,  58,  60,  55],
  [14,  13,  16,  24,  40,  57,  69,  56],
  [14,  17,  22,  29,  51,  87,  80,  62],
  [18,  22,  37,  56,  68, 109, 103,  77],
  [24,  35,  55,  64,  81, 104, 113,  92],
  [49,  64,  78,  87, 103, 121, 120, 101],
  [72,  92,  95,  98, 112, 100, 103,  99]])


quantization_chrominance_matrix = numpy.array([
  [17,  18,  24,  47,  99,  99,  99,  99],
  [18,  21,  26,  66,  99,  99,  99,  99],
  [24,  26,  56,  99,  99,  99,  99,  99],
  [47,  66,  99,  99,  99,  99,  99,  99],
  [99,  99,  99,  99,  99,  99,  99,  99],
  [99,  99,  99,  99,  99,  99,  99,  99],
  [99,  99,  99,  99,  99,  99,  99,  99],
  [99,  99,  99,  99,  99,  99,  99,  99]])


def text_to_bits(text):
    bit_array = bitarray()
    bit_array.frombytes(text.encode("utf-8"))
    return bit_array.to01()


def bits_to_text(bits):
    bit_array = bitarray(bits)
    bits = bit_array.tobytes()
    return ''.join(bits)


def image_is_greyscale():
    return len(image.shape) == 2


def image_is_unconventional_size():
    image_width = image.shape[1]
    image_height = image.shape[0]
    return image_height % 8 != 0 or image_width % 8 != 0


def generate_path():
    path = list()
    for bit in range(len(message)):
        coordinates = list()
        y = randint(0, image.shape[0] - 1)
        coordinates.append(y)
        x = randint(0, image.shape[1] - 1)
        coordinates.append(x)
        if not image_is_greyscale():
            z = randint(0, image.shape[2] - 1)
            coordinates.append(z)
        path.append(coordinates)
    return path


def image_to_rgb():
    r = image[:, :, 2]
    g = image[:, :, 1]
    b = image[:, :, 0]
    return r, g, b


def rgb_to_image(r, g, b):
    result = numpy.ndarray((r.shape[0], r.shape[1], 3))
    result[:, :, 2] = r
    result[:, :, 1] = g
    result[:, :, 0] = b
    return result


def rgb_to_ycbcr(r, g, b):
    y = .299 * r + .587 * g + .114 * b
    cb = 128 - .169 * r - .331 * g + .5 * b
    cr = 128 + .5 * r - .419 * g - .081 * b
    return y, cb, cr


#https://web.archive.org/web/20180421030430/http://www.equasys.de/colorconversion.html
def ycbcr_to_rgb(y, cb, cr):
    cr -= 128
    cb -= 128
    r = y + 1.402 * cr
    g = y - .34414 * cb - .71414 * cr
    b = y + 1.772 * cb
    return r, g, b


# https://inst.eecs.berkeley.edu/~ee123/sp16/Sections/JPEG_DCT_Demo.html
def dct_transformation(block):
    block -= 128
    return dct(dct(block, axis=0, norm='ortho'), axis=1, norm='ortho')


def inverse_dct_transformation(block):
    result = idct(idct(block, axis=0, norm='ortho'), axis=1, norm='ortho')
    result += 128
    return result


def quantize_luminance(block):
    return numpy.around(block / quantization_luminance_matrix)


def quantize_chrominance(block):
    return numpy.around(block / quantization_chrominance_matrix)


def dequantize_luminance(block):
    return block * quantization_luminance_matrix


def dequantize_chrominance(block):
    return block * quantization_chrominance_matrix


def compress_greyscale_image():
    return compress(image, True)


def compress_colour_image():
    r, g, b = image_to_rgb()
    y, cb, cr = rgb_to_ycbcr(r, g, b)
    y, cb, cr = compress(y, True), compress(cb, False), compress(cr, False)
    result = numpy.empty_like(image)
    result[:, :, 0], result[:, :, 1], result[:, :, 2] = y, cb, cr
    return result


def decompress_greyscale_image(compressed_image):
    return decompress(compressed_image, True)


def decompress_colour_image(compressed_image):
    y, cb, cr = compressed_image[:, :, 0], compressed_image[:, :, 1], compressed_image[:, :, 2]
    y, cb, cr = decompress(y, True), decompress(cb, False), decompress(cr, False)
    r, g, b = ycbcr_to_rgb(y, cb, cr)
    return rgb_to_image(r, g, b)


#https://inst.eecs.berkeley.edu/~ee123/sp16/Sections/JPEG_DCT_Demo.html
def compress(channel, is_greyscale):
    channel_dimensions = channel.shape
    compressed_channel = numpy.zeros(channel_dimensions)

    for i in r_[:channel_dimensions[0]:8]:
        for j in r_[:channel_dimensions[1]:8]:
            compressed_channel[i:(i + 8), j:(j + 8)] = dct_transformation(channel[i:(i + 8), j:(j + 8)])
            if is_greyscale:
                compressed_channel[i:(i + 8), j:(j + 8)] = quantize_luminance(compressed_channel[i:(i + 8), j:(j + 8)])
            else:
                compressed_channel[i:(i + 8), j:(j + 8)] = quantize_chrominance(compressed_channel[i:(i + 8), j:(j + 8)])

    return compressed_channel


def decompress(compressed_channel, is_greyscale):
    image_dimensions = compressed_channel.shape
    channel = numpy.zeros(image_dimensions)

    for i in r_[:image_dimensions[0]:8]:
        for j in r_[:image_dimensions[1]:8]:
            if is_greyscale:
                channel[i:(i + 8), j:(j + 8)] = dequantize_luminance(compressed_channel[i:(i + 8), j:(j + 8)])
            else:
                channel[i:(i + 8), j:(j + 8)] = dequantize_chrominance(compressed_channel[i:(i + 8), j:(j + 8)])
            channel[i:(i + 8), j:(j + 8)] = inverse_dct_transformation(channel[i:(i + 8), j:(j + 8)])

    return channel


def crop_image():
    print "Image was cropped (original image's height and/or width was not divisible by 8)"
    image_width = image.shape[1]
    image_height = image.shape[0]
    remainder_width = image_width % 8
    remainder_height = image_height % 8
    return image[0:image_height - remainder_height, 0:image_width - remainder_width, :]


def LSB_replacement_simple_colour_encode(compressed_image, message):
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

def LSB_replacement_simple_greyscale_encode(compressed_image, message):
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


def LSB_replacement_simple_colour_decode(encoded_image):
    message = list()
    try:
        for z in range(len(encoded_image[0, 0, :])):
            for x in range(len(encoded_image[0, :, 0])):
                for y in range(len(encoded_image[:, 0, 0])):
                    message.append(int(encoded_image[y, x, z]) & 1)
    except IndexError:
        pass
    return ''.join(str(char) for char in message)


def LSB_replacement_simple_greyscale_decode(encoded_image):
    message = list()
    try:
        for x in range(len(encoded_image[0, :, 0])):
            for y in range(len(encoded_image[:, 0, 0])):
                message.append(int(encoded_image[y, x]) & 1)
    except IndexError:
        pass
    return ''.join(str(char) for char in message)


def LSB_replacement_random_colour_encode(compressed_image, message, path):
    message = list(message)
    for coordinates in path:
        y, x, z = coordinates[0], coordinates[1], coordinates[2]
        message_bit = message.pop(0)
        if int(message_bit) == 1:
            compressed_image[y, x, z] = int(compressed_image[y, x, z]) | 1  # change the LSB to 1
        else:
            compressed_image[y, x, z] = int(compressed_image[y, x, z]) & ~ 1  # change the LSB to 0
    return compressed_image


def LSB_replacement_random_greyscale_encode(compressed_image, message, path):
    message = list(message)
    for coordinates in path:
        y, x = coordinates[0], coordinates[1]
        message_bit = message.pop(0)
        if int(message_bit) == 1:
            compressed_image[y, x] = int(compressed_image[y, x]) | 1  # change the LSB to 1
        else:
            compressed_image[y, x] = int(compressed_image[y, x]) & ~ 1  # change the LSB to 0
    return compressed_image


def LSB_replacement_random_colour_decode(encoded_image, path):
    message = list()
    for coordinates in path:
        y, x, z = coordinates[0], coordinates[1], coordinates[2]
        message.append(int(encoded_image[y, x, z]) & 1)
    return ''.join(str(char) for char in message)


def LSB_replacement_random_greyscale_decode(encoded_image, path):
    message = list()
    for coordinates in path:
        y, x = coordinates[0], coordinates[1]
        message.append(int(encoded_image[y, x]) & 1)
    return ''.join(str(char) for char in message)


def calculate_quantization_luminance_matrix():
    return numpy.maximum(numpy.floor((50 + quantization_luminance_matrix * (200 - 2 * quality_factor))
                                     / 100), numpy.ones((8, 8)))


def calculate_quantization_chrominance_matrix():
    return numpy.maximum(numpy.floor((50 + quantization_chrominance_matrix * (200 - 2 * quality_factor))
                                     / 100), numpy.ones((8, 8)))


if __name__ == '__main__':
    message = raw_input("Input: ")
    message = text_to_bits(message)

    script_directory = os.path.dirname(__file__) # https://stackoverflow.com/questions/36476659/how-to-add-a-relative-path-in-python-to-find-image-and-other-file-with-a-short-p
    relative_path = "images/i2.jpg"
    absolute_file_path = os.path.join(script_directory, relative_path)

    quality_factor = 100
    quantization_luminance_matrix = calculate_quantization_luminance_matrix()
    quantization_chrominance_matrix = calculate_quantization_chrominance_matrix()

    image = misc.imread(absolute_file_path).astype(float)

    if image_is_unconventional_size():
        image = crop_image()

    encoding_path = generate_path()

    if image_is_greyscale():
        compressed_image = compress_greyscale_image()
        final_result = decompress_greyscale_image(compressed_image)
        LSB_replacement_random_greyscale_encode(final_result, message, encoding_path)
        text_binary = LSB_replacement_random_greyscale_decode(final_result, encoding_path)
    else:
        compressed_image = compress_colour_image()
        final_result = decompress_colour_image(compressed_image)
        LSB_replacement_random_colour_encode(final_result, message, encoding_path)
        text_binary = LSB_replacement_random_colour_decode(final_result, encoding_path)

    text = bits_to_text(text_binary)
    print text
    #toimage(final_result).show()
