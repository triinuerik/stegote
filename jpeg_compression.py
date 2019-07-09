import numpy
from scipy.fftpack import dct, idct
from numpy import r_

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

zigzagged_image = list()


def image_is_greyscale(image):
    """
    Checks if the image is greyscale or colour image.

    Args:
        image (numpy.ndarray): The image to be checked.

    Returns:
        bool: True if image is greyscale, False if image is coloured.
    """

    return len(image.shape) == 2


def image_is_unconventional_size(image):
    """
    Checks if the image has dimensions (width and length) that are a multiple of 8.
    This is needed for JPEG compression, as it works with 8x8 pixel blocks.

    Args:
        image (numpy.ndarray): The image to be checked.

    Returns:
        bool: True if image dimensions need to be modified, False if image already has a good dimensions.
    """

    image_width = image.shape[1]
    image_height = image.shape[0]
    return image_height % 8 != 0 or image_width % 8 != 0


def crop_image(image):
    """
    Crops an image with unconventional dimensions and let's the user know of this activity.

    Args:
        image (numpy.ndarray): The image to be cropped.

    Returns:
        numpy.ndarray: A modified image with appropriate dimensions.
    """

    print("Image was cropped (original image's height and/or width was not divisible by 8)")
    image_width = image.shape[1]
    image_height = image.shape[0]
    remainder_width = image_width % 8
    remainder_height = image_height % 8
    if image_is_greyscale(image):
        return image[0:image_height - remainder_height, 0:image_width - remainder_width]
    return image[0:image_height - remainder_height, 0:image_width - remainder_width, :]


def image_to_rgb(image):
    """
    Splits the image into its red, green and blue channels.

    Args:
        image (numpy.ndarray): The image to be split.

    Returns:
        numpy.ndarray: The red, green and blue channels.
    """

    r = image[:, :, 0]
    g = image[:, :, 1]
    b = image[:, :, 2]
    return r, g, b


def rgb_to_image(r, g, b):
    """
    Gathers the red, green and blue channels and joins them back to a coherent image.

    Args:
        r (numpy.ndarray): The red channel.
        g (numpy.ndarray): The green channel.
        b (numpy.ndarray): The blue channel.

    Returns:
        numpy.ndarray: The image.
    """

    image = numpy.ndarray((r.shape[0], r.shape[1], 3))
    image[:, :, 2] = r
    image[:, :, 1] = g
    image[:, :, 0] = b
    return image


def rgb_to_ycbcr(r, g, b):
    """
    Transforms the RGB colour space to YCbCr colour space.

    Args:
        r (numpy.ndarray): The red channel.
        g (numpy.ndarray): The green channel.
        b (numpy.ndarray): The blue channel.

    Returns:
        numpy.ndarray: The Y, Cb and Cr colour channels.
    """

    y = .299 * r + .587 * g + .114 * b
    cb = 128 - .169 * r - .331 * g + .5 * b
    cr = 128 + .5 * r - .419 * g - .081 * b
    return y, cb, cr


def ycbcr_to_rgb(y, cb, cr):
    """
    Transforms the YCbCr colour space to RGB colour space.

    Args:
        y (numpy.ndarray): The Y channel.
        cb (numpy.ndarray): The Cb channel.
        cr (numpy.ndarray): The Cr channel.

    Returns:
        numpy.ndarray: The red, green and blue channels.
    """

    cr -= 128
    cb -= 128
    r = y + 1.402 * cr
    g = y - .34414 * cb - .71414 * cr
    b = y + 1.772 * cb
    return r, g, b


def dct_transformation(block):
    """
    Performs the DCT-2 transformation on a 8x8 pixel block.
    Because the DCT works on pixel values ranging from -128 to 127 (not 0 to 255) we subtract 128 from the block.
    Reference: https://inst.eecs.berkeley.edu/~ee123/sp16/Sections/JPEG_DCT_Demo.html

    Args:
        block (numpy.ndarray): The 8x8 pixel block to be transformed.

    Returns:
        numpy.ndarray: The transformed block.
    """

    block -= 128
    return dct(dct(block, axis=0, norm='ortho'), axis=1, norm='ortho')


def inverse_dct_transformation(block):
    """
    Performs the inverse DCT-2 transformation on a 8x8 pixel block.
    Because DCT was performed on pixel values ranging from -128 to 127 we add 128 to the block to be in 0...255 space.
    Reference: https://inst.eecs.berkeley.edu/~ee123/sp16/Sections/JPEG_DCT_Demo.html

    Args:
        block (numpy.ndarray): The 8x8 pixel block to be inverse transformed.

    Returns:
        numpy.ndarray: The inverse transformed block.
    """

    result = idct(idct(block, axis=0, norm='ortho'), axis=1, norm='ortho')
    result += 128
    return result


def quantize_luminance(block):
    """
    Performs quantization on a 8x8 pixel luminance (Y channel) block.

    Args:
        block (numpy.ndarray): The 8x8 pixel block to be quantized.

    Returns:
        numpy.ndarray: The quantized block.
    """

    return numpy.around(block / quantization_luminance_matrix)


def quantize_chrominance(block):
    """
    Performs quantization on a 8x8 pixel chrominance (Cb or Cr channel) block.

    Args:
        block (numpy.ndarray): The 8x8 pixel block to be quantized.

    Returns:
        numpy.ndarray: The quantized block.
    """

    return numpy.around(block / quantization_chrominance_matrix)


def dequantize_luminance(block):
    """
    Performs dequantization on a 8x8 pixel luminance (Y channel) block.

    Args:
        block (numpy.ndarray): The 8x8 pixel block to be dequantized.

    Returns:
        numpy.ndarray: The dequantized block.
    """

    return block * quantization_luminance_matrix


def dequantize_chrominance(block):
    """
    Performs dequantization on a 8x8 pixel chrominance (Cb or Cr channel) block.

    Args:
        block (numpy.ndarray): The 8x8 pixel block to be dequantized.

    Returns:
        numpy.ndarray: The dequantized block.
    """

    return block * quantization_chrominance_matrix


def compress_greyscale_image(image):
    """
    Performs JPEG-compression on a greyscale image.

    Args:
        image (numpy.ndarray): The greyscale image to be compressed.

    Returns:
        numpy.ndarray: The compressed image, in other words the quantized DCT coefficients of the image.
    """

    return compress(image, True)


def compress_colour_image(image):
    """
    Performs JPEG-compression on a colour image.
    Splits the image into its RGB channels, transforms the channels to YCbCr colour space, compresses each channel
    separately and then rejoins them into one image.

    Args:
        image (numpy.ndarray): The colour image to be compressed.

    Returns:
        numpy.ndarray: Compressed image, in other words the quantized DCT coefficients of the image's YCbCr channels.
    """

    r, g, b = image_to_rgb(image)
    y, cb, cr = rgb_to_ycbcr(r, g, b)
    y, cb, cr = compress(y, True), compress(cb, False), compress(cr, False)
    compressed_image = numpy.empty_like(image)
    compressed_image[:, :, 0], compressed_image[:, :, 1], compressed_image[:, :, 2] = y, cb, cr
    return compressed_image


def decompress_greyscale_image(compressed_image):
    """
    Performs JPEG-decompression on a greyscale image, in order to display it visually again.

    Args:
        compressed_image (numpy.ndarray): The quantized DCT coefficients of the image.

    Returns:
        numpy.ndarray: The decompressed greyscale image, ready to be displayed as a JPEG image.
    """

    return decompress(compressed_image, True)


def decompress_colour_image(compressed_image):
    """
    Performs JPEG-decompression on a colour image, in order to display it visually again.
    Splits the compressed image to its YCbCr channels, decompresses them separately, transforms them to the RGB colour
    space and joins the RGB channels back together to form a coherent image.

    Args:
        compressed_image (numpy.ndarray): The quantized DCT coefficients of the image.

    Returns:
        numpy.ndarray: The decompressed colour image, ready to be displayed as a JPEG image.
    """

    y, cb, cr = compressed_image[:, :, 0], compressed_image[:, :, 1], compressed_image[:, :, 2]
    y, cb, cr = decompress(y, True), decompress(cb, False), decompress(cr, False)
    r, g, b = ycbcr_to_rgb(y, cb, cr)
    return rgb_to_image(r, g, b)


def compress(channel, is_greyscale):
    """
    JPEG-compresses a channel by 8x8 pixel blocks. First DCT transforms the block and then quantizes it. Also creates
    a list of pixels in a zig-zag order later to be used for encoding/decoding.
    Reference: https://inst.eecs.berkeley.edu/~ee123/sp16/Sections/JPEG_DCT_Demo.html

    Args:
        channel (numpy.ndarray): The channel to be compressed.
        is_greyscale (bool): True if image is greyscale, False if colour image. Used for knowing which quantization
                             matrix to use.

    Returns:
        numpy.ndarray: The compressed channel.
    """

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
    """
    JPEG-decompresses a channel by 8x8 pixel blocks. First dequantizes the block and then performs inverse DCT on it.
    Also creates a list of pixels in a zig-zag order later to be used for encoding/decoding.
    Reference: https://inst.eecs.berkeley.edu/~ee123/sp16/Sections/JPEG_DCT_Demo.html

    Args:
        compressed_channel (numpy.ndarray): The channel to be decompressed.
        is_greyscale (bool): True if image is greyscale, False if colour image. Used for knowing which quantization
                             matrix to use.

    Returns:
        numpy.ndarray: The decompressed channel.
    """

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


def calculate_quantization_luminance_matrix(quality_factor):
    """
    Calculates the luminance matrix that is used for quantization/dequantization based on the quality factor.

    Args:
        quality_factor (int): The compression quality factor. On a scale from 0 to 100.

    Returns:
        numpy.ndarray: The modified luminance matrix.
    """

    return numpy.maximum(numpy.floor((50 + quantization_luminance_matrix * (200 - 2 * quality_factor))
                                     / 100), numpy.ones((8, 8)))


def calculate_quantization_chrominance_matrix(quality_factor):
    """
    Calculates the chrominance matrix that is used for quantization/dequantization based on the quality factor.

    Args:
        quality_factor (int): The compression quality factor. On a scale from 0 to 100.

    Returns:
        numpy.ndarray: The modified chrominance matrix.
    """

    return numpy.maximum(numpy.floor((50 + quantization_chrominance_matrix * (200 - 2 * quality_factor))
                                     / 100), numpy.ones((8, 8)))
