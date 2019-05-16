from bitarray import bitarray
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


quantization_luminence_matrix = numpy.array([
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


def image_is_grayscale(image):
    print image.shape
    return len(image.shape) == 2


def image_to_rgb(image):
    r = image[:, :, 2]
    g = image[:, :, 1]
    b = image[:, :, 0]
    return r, g, b


def rgb_to_image(r, g, b):
    image = numpy.ndarray((r.shape[0], r.shape[1], 3))
    image[:, :, 0] = r
    image[:, :, 2] = g
    image[:, :, 1] = b
    return image


def rgb_to_ycbcr(r, g, b):
    y = .299 * r + .587 * g + .114 * b
    cb = 128 - .169 * r - .331 * g + .5 * b
    cr = 128 + .5 * r - .419 * g - .081 * b
    return y, cb, cr


#https://web.archive.org/web/20180421030430/http://www.equasys.de/colorconversion.html
def ycrcb_to_rgb(y, cr, cb):
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


def quantizise_luminence(block):
    return numpy.around(block / quantization_luminence_matrix)


def quantizise_chrominance(block):
    return numpy.around(block / quantization_chrominance_matrix)


def test_hiding_row_by_row(block, message):
    print(block)
    data1 = numpy.int8(block)
    print(message)
    for i in range(0, 8):
        for j in range(0, 8):
            if len(message) > 0:
                char = int(message[0])
                block[i, j] += char
                message = message[1:]
            else:
                break
    data2 = numpy.int8(block)
    toimage(data1).show()
    toimage(data2).show()
    print(block)


def compress_grayscale_image(image):
    result = compress(image, True)
    data = numpy.int8(result)
    return result


def compress_colour_image(image):
    r, g, b = image_to_rgb(image)
    y, cb, cr = rgb_to_ycbcr(r, g, b)
    y, cb, cr = compress(y, True), compress(cb, False), compress(cr, False)
    result = numpy.empty_like(image)
    result[:, :, 0] = y
    result[:, :, 1] = cb
    result[:, :, 2] = cr
    return result


#https://inst.eecs.berkeley.edu/~ee123/sp16/Sections/JPEG_DCT_Demo.html
def compress(image, is_grayscale):
    image_size = image.shape
    compressed_image = numpy.zeros(image_size)

    for i in r_[:image_size[0]:8]:
        for j in r_[:image_size[1]:8]:
            compressed_image[i:(i + 8), j:(j + 8)] = dct_transformation(image[i:(i + 8), j:(j + 8)])
            if is_grayscale:
                compressed_image[i:(i + 8), j:(j + 8)] = quantizise_luminence(compressed_image[i:(i + 8), j:(j + 8)])
            else:
                compressed_image[i:(i + 8), j:(j + 8)] = quantizise_chrominance(compressed_image[i:(i + 8), j:(j + 8)])

    return compressed_image


def decompress(compressed_image, is_colour):
    image_size = compressed_image.shape
    image = numpy.zeros(image_size)

    for i in r_[:image_size[0]:8]:
        for j in r_[:image_size[1]:8]:
            image[i:(i + 8), j:(j + 8)] = inverse_dct_transformation(compressed_image[i:(i + 8), j:(j + 8)])

    if is_colour:
        r, b, g = ycrcb_to_rgb(image[:, :, 0], image[:, :, 1], image[:, :, 2])
        image = rgb_to_image(r, g, b)

    return image


def crop_image(image, image_width, image_height):
    print "Image was cropped (original image's height and/or width was not divisible by 8)"
    remainder_width = image_width % 8
    remainder_height = image_height % 8
    image = image[0:image_height - remainder_height, 0:image_width - remainder_width, :]
    return image


if __name__ == '__main__':
    #message = raw_input("Input: ")
    #message = text_to_bits(message)

    script_dir = os.path.dirname(__file__) # https://stackoverflow.com/questions/36476659/how-to-add-a-relative-path-in-python-to-find-image-and-other-file-with-a-short-p
    rel_path = "images/i6.jpg"
    abs_file_path = os.path.join(script_dir, rel_path)

    image = misc.imread(abs_file_path).astype(float)
    image_width = image.shape[1]
    image_height = image.shape[0]
    is_colour = False

    if image_height % 8 != 0 or image_width % 8 != 0:
        image = crop_image(image, image_width, image_height)

    if not image_is_grayscale(image):
        result = compress_colour_image(image)
        is_colour = True
    else:
        result = compress_grayscale_image(image)

    a = decompress(result, is_colour)
    toimage(a).show()


    #test_hiding_row_by_row(quantizised_test_blocks[:, :, 0], message)


    for values, color, channel in zip((r, g, b), ('red', 'green', 'blue'), (2,1,0)):
          img = numpy.zeros((values.shape[0], values.shape[1], 3), dtype = values.dtype)
          img[:,:,channel] = values
          #toimage(img).show()





