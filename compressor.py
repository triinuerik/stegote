from bitarray import bitarray
import scipy
from scipy import misc
from scipy.ndimage import imread
from scipy.misc import toimage
from scipy.fftpack import dct
from PIL import Image
import numpy
import os


def text_to_bits(text):
    bit_array = bitarray()
    bit_array.frombytes(text.encode("utf-8"))
    print bit_array.to01()


def image_to_rgb(image): #https://knowpapa.com/opencv-rgb-split/
    red = image[:, :, 2]
    green = image[:, :, 1]
    blue = image[:, :, 0]
    return red, green, blue


def rgb_to_ycbcr(r, g, b, image):
    cbcr = numpy.empty_like(image)
    # Y
    cbcr[:, :, 0] = .299 * r + .587 * g + .114 * b
    # Cb
    cbcr[:, :, 1] = 128 - .169 * r - .331 * g + .5 * b  # why are these black and white?
    # Cr
    cbcr[:, :, 2] = 128 + .5 * r - .419 * g - .081 * b

    # https://stackoverflow.com/questions/34913005/color-space-mapping-ycbcr-to-rgb
    xform = numpy.array([[.299, .587, .114], [-.1687, -.3313, .5], [.5, -.4187, -.0813]])
    ycbcr = image.dot(xform.T)
    ycbcr[:, :, [1, 2]] += 128

    data = numpy.uint8(ycbcr[:, :, 0])
    # toimage(data).show()
    return numpy.uint8(ycbcr)


def blocksplit(image):
    number_of_blocks = image.size / 64
    blocks = numpy.ndarray([8, 8, number_of_blocks])
    for j in range(0, 8):
        for k in range(0, 8):
            if j != 0 or k != 0:
                blocks[j, k] = image[j::8, k::8].reshape(number_of_blocks)
    return blocks


def transform(block):
    block -= 128 # in these coeficients?
    print dct(block)

if __name__ == '__main__':
    #message = raw_input("Input: ")
    #text_to_bits(message)

    script_dir = os.path.dirname(__file__) # https://stackoverflow.com/questions/36476659/how-to-add-a-relative-path-in-python-to-find-image-and-other-file-with-a-short-p
    rel_path = "images/i1.jpg"
    abs_file_path = os.path.join(script_dir, rel_path)

    face = misc.imread(abs_file_path)

    red, green, blue = image_to_rgb(face)
    ycbcr = rgb_to_ycbcr(red, green, blue, face)

    test_block = blocksplit(ycbcr[:, :, 0])[:, :, 678]
    transform(test_block)
    data = numpy.uint8(test_block)

    for values, color, channel in zip((red, green, blue), ('red', 'green', 'blue'), (2,1,0)):
          img = numpy.zeros((values.shape[0], values.shape[1], 3), dtype = values.dtype)
          img[:,:,channel] = values
          #print "Saving Image: {}.".format("image"+color+".jpg")
          #toimage(img).show()
