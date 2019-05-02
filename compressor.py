from bitarray import bitarray
import scipy
from scipy import misc
from scipy.ndimage import imread
from scipy.misc import toimage
from scipy.fftpack import dct
from PIL import Image
from numpy import r_
import matplotlib.pyplot as plt
import numpy
import os


quantization_matrix = numpy.array([
  [16,  11,  10,  16,  24,  40,  51,  61],
  [12,  12,  14,  19,  26,  58,  60,  55],
  [14,  13,  16,  24,  40,  57,  69,  56],
  [14,  17,  22,  29,  51,  87,  80,  62],
  [18,  22,  37,  56,  68, 109, 103,  77],
  [24,  35,  55,  64,  81, 104, 113,  92],
  [49,  64,  78,  87, 103, 121, 120, 101],
  [72,  92,  95,  98, 112, 100, 103,  99]])


def text_to_bits(text):
    bit_array = bitarray()
    bit_array.frombytes(text.encode("utf-8"))
    print bit_array.to01()


def image_to_rgb(image):
    r = image[:, :, 2]
    g = image[:, :, 1]
    b = image[:, :, 0]
    return r, g, b


def rgb_to_ycbcr(r, g, b, image):
    ycbcr = numpy.empty_like(image)
    ycbcr[:, :, 0] = .299 * r + .587 * g + .114 * b
    ycbcr[:, :, 1] = 128 - .169 * r - .331 * g + .5 * b
    ycbcr[:, :, 2] = 128 + .5 * r - .419 * g - .081 * b
    y = ycbcr[:, :, 0]
    cb = ycbcr[:, :, 1]
    cr = ycbcr[:, :, 2]
    return y, cb, cr


def blocksplit(image):
    number_of_blocks = image.size / 64
    blocks = numpy.ndarray([8, 8, number_of_blocks])
    for j in range(0, 8):
        for k in range(0, 8):
            if j != 0 or k != 0:
                blocks[j, k] = image[j::8, k::8].reshape(number_of_blocks)
    return blocks


# https://inst.eecs.berkeley.edu/~ee123/sp16/Sections/JPEG_DCT_Demo.html
def dct_transformation(block):
    block -= 128
    return dct(dct(block, axis=0, norm='ortho'), axis=1, norm='ortho')


def transform_blocks(blocks):
    number_of_blocks = blocks.shape[2]
    transformed_blocks = numpy.zeros([8, 8, number_of_blocks])
    for i in range(number_of_blocks):
        transformed_blocks[:, :, i] = dct_transformation(blocks[:, :, i])
    return transformed_blocks


def quantizise(blocks):
    number_of_blocks = blocks.shape[2]
    quantizised_blocks = numpy.zeros([8, 8, number_of_blocks])
    for i in range(number_of_blocks):
        quantizised_blocks[:, :, i] = numpy.around(blocks[:, :, i] / quantization_matrix)
    return quantizised_blocks


# https://github.com/wzq94qzw/naive-jpeg
def zigzag(block):
    zigzag_array = numpy.zeros([64])
    index = -1
    for i in range(0, 14):
        if i < 8:
            bound = 0
        else:
            bound = i - 7
        for j in range(bound, i - bound + 1):
            index += 1
            if i % 2 == 1:
                zigzag_array[index] = block[j, i-j]
            else:
                zigzag_array[index] = block[i-j, j]
    return zigzag_array



if __name__ == '__main__':
    #message = raw_input("Input: ")
    #text_to_bits(message)

    script_dir = os.path.dirname(__file__) # https://stackoverflow.com/questions/36476659/how-to-add-a-relative-path-in-python-to-find-image-and-other-file-with-a-short-p
    rel_path = "images/i1.jpg"
    abs_file_path = os.path.join(script_dir, rel_path)

    image = misc.imread(abs_file_path)
    r, g, b = image_to_rgb(image)
    y, cb, cr = rgb_to_ycbcr(r, g, b, image)
    test_blocks = blocksplit(y)
    transformed_test_blocks = transform_blocks(test_blocks)
    quantizised_test_blocks = quantizise(transformed_test_blocks)
    print quantizised_test_blocks[:, :, 0]
    print zigzag(quantizised_test_blocks[:, :, 0])


