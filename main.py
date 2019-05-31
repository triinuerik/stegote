import os
import jpeg_compression
from codec import *
from path_generating import *
from scipy import misc
from scipy.misc import toimage


if __name__ == '__main__':
    secret_message = input("Input: ")
    secret_message = text_to_bits(secret_message)

    file_path = os.path.join(os.path.dirname(__file__), "images/i2.jpg")
    image = misc.imread(file_path).astype(float)

    quality_factor = 100
    jpeg_compression.quantization_luminance_matrix = calculate_quantization_luminance_matrix(quality_factor)
    jpeg_compression.quantization_chrominance_matrix = calculate_quantization_chrominance_matrix(quality_factor)

    if image_is_unconventional_size(image):
        image = crop_image(image)

    secret_key = generate_key()

    secret_image, path_token = image_path_encode_replacement(image, secret_message, secret_key)
    #toimage(secret_image).show()
    secret_message = image_path_decode(secret_image, secret_key, path_token)
    print(secret_message)
