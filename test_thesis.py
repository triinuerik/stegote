import unittest
import imageio
import jpeg_compression
from jpeg_compression import *
from main import *
from codec import *


class Tests(unittest.TestCase):

    def test_jpeg_zigzag_colour(self):
        message = "testing testing"
        image = imageio.imread("test_data/colour_image.jpg").astype(float)
        secret_message = text_to_bits(message)

        # Hiding data
        compressed_image = compress_colour_image(image)
        hiding_path = generate_zigzag_dct_path(compressed_image)
        encoded_image = lsb_matching_colour_dct_encode(compressed_image, secret_message, hiding_path)

        # Reading data
        reading_path = generate_zigzag_dct_path(encoded_image)
        text_binary = lsb_embedding_colour_decode(compressed_image, reading_path)
        secret_message = bits_to_text(text_binary)

        print("--- JPEG colour image, zigzag encoding, LSB matching ---")
        print(secret_message[0:len(message) + 10])
        self.assertEqual(secret_message[0:len(message)], message)

    def test_jpeg_zigzag_greyscale(self):
        message = "testing testing"
        image = imageio.imread("test_data/greyscale_image.jpg").astype(float)
        secret_message = text_to_bits(message)

        # Hiding data
        compressed_image = compress_greyscale_image(image)
        hiding_path = generate_zigzag_dct_path(compressed_image)
        encoded_image = lsb_matching_greyscale_dct_encode(compressed_image, secret_message, hiding_path)

        # Reading data
        reading_path = generate_zigzag_dct_path(encoded_image)
        text_binary = lsb_embedding_greyscale_decode(encoded_image, reading_path)
        secret_message = bits_to_text(text_binary)

        print("--- JPEG greyscale image, zigzag encoding, LSB matching ---")
        print(secret_message[0:len(message) + 10])
        self.assertEqual(secret_message[0:len(message)], message)

    def test_jpeg_key_colour(self):
        message = "testing testing"
        key = "6u5UduLLCuIGM1oDMoy4A9SFK1NYJpnnF9eFjQiMtPY="
        key = key.encode("utf-8")
        image = imageio.imread("test_data/colour_image.jpg").astype(float)
        secret_message = text_to_bits(message)

        # Hiding data
        compressed_image = compress_colour_image(image)
        hiding_path = generate_dct_path_from_key(compressed_image, key)
        encoded_image = lsb_matching_colour_dct_encode(compressed_image, secret_message, hiding_path)

        # Reading data
        reading_path = generate_dct_path_from_key(encoded_image, key)
        text_binary = lsb_embedding_colour_decode(encoded_image, reading_path)
        secret_message = bits_to_text(text_binary)

        print("--- JPEG colour image, key encoding, LSB matching ---")
        print(secret_message[0:len(message) + 10])
        self.assertEqual(secret_message[0:len(message)], message)

    def test_jpeg_key_greyscale(self):
        message = "testing testing"
        key = "6u5UduLLCuIGM1oDMoy4A9SFK1NYJpnnF9eFjQiMtPY="
        key = key.encode("utf-8")
        image = imageio.imread("test_data/greyscale_image.jpg").astype(float)
        message_length = len(message)
        secret_message = text_to_bits(message)

        # Hiding data
        compressed_image = compress_greyscale_image(image)
        hiding_path = generate_dct_path_from_key(compressed_image, key)
        encoded_image = lsb_matching_greyscale_dct_encode(compressed_image, secret_message, hiding_path)

        # Reading data
        reading_path = generate_dct_path_from_key(encoded_image, key)
        text_binary = lsb_embedding_greyscale_decode(encoded_image, reading_path)
        secret_message = bits_to_text(text_binary)

        print("--- JPEG greyscale image, key encoding, LSB matching ---")
        print(secret_message[0:len(message) + 10])
        self.assertEqual(secret_message[0:message_length], message)

    def test_jpeg_path_colour_matching(self):
        message = "testing testing"
        key = "6u5UduLLCuIGM1oDMoy4A9SFK1NYJpnnF9eFjQiMtPY="
        key = key.encode("utf-8")
        image = imageio.imread("test_data/colour_image.jpg").astype(float)
        secret_message = text_to_bits(message)

        # Hiding data
        compressed_image = compress_colour_image(image)
        hiding_path = generate_dct_path(compressed_image, secret_message)
        encoded_image = lsb_matching_colour_dct_encode(compressed_image, secret_message, hiding_path)
        token = encrypt_path(hiding_path, key)

        # Reading data
        reading_path = decrypt_path(token, key)
        text_binary = lsb_embedding_colour_decode(encoded_image, reading_path)
        secret_message = bits_to_text(text_binary)

        print("--- JPEG colour image, path encoding, LSB matching ---")
        print(secret_message)
        self.assertEqual(secret_message, message)

    def test_jpeg_path_colour_replacement(self):
        message = "testing testing"
        key = "6u5UduLLCuIGM1oDMoy4A9SFK1NYJpnnF9eFjQiMtPY="
        key = key.encode("utf-8")
        image = imageio.imread("test_data/colour_image.jpg").astype(float)
        secret_message = text_to_bits(message)

        # Hiding data
        compressed_image = compress_colour_image(image)
        hiding_path = generate_dct_path(compressed_image, secret_message)
        encoded_image = lsb_replacement_colour_encode(compressed_image, secret_message, hiding_path)
        token = encrypt_path(hiding_path, key)

        # Reading data
        reading_path = decrypt_path(token, key)
        text_binary = lsb_embedding_colour_decode(encoded_image, reading_path)
        secret_message = bits_to_text(text_binary)

        print("--- JPEG colour image, path encoding, LSB replacement ---")
        print(secret_message)
        self.assertEqual(secret_message, message)

    def test_jpeg_path_greyscale_matching(self):
        message = "testing testing"
        key = "6u5UduLLCuIGM1oDMoy4A9SFK1NYJpnnF9eFjQiMtPY="
        key = key.encode("utf-8")
        image = imageio.imread("test_data/greyscale_image.jpg").astype(float)
        secret_message = text_to_bits(message)

        # Hiding data
        compressed_image = compress_greyscale_image(image)
        hiding_path = generate_dct_path(compressed_image, secret_message)
        encoded_image = lsb_matching_greyscale_dct_encode(compressed_image, secret_message, hiding_path)
        token = encrypt_path(hiding_path, key)

        # Reading data
        reading_path = decrypt_path(token, key)
        text_binary = lsb_embedding_greyscale_decode(encoded_image, reading_path)
        secret_message = bits_to_text(text_binary)

        print("--- JPEG greyscale image, path encoding, LSB matching ---")
        print(secret_message)
        self.assertEqual(secret_message, message)

    def test_jpeg_path_greyscale_replacement(self):
        message = "testing testing"
        key = "6u5UduLLCuIGM1oDMoy4A9SFK1NYJpnnF9eFjQiMtPY="
        key = key.encode("utf-8")
        image = imageio.imread("test_data/greyscale_image.jpg").astype(float)
        secret_message = text_to_bits(message)

        # Hiding data
        compressed_image = compress_greyscale_image(image)
        hiding_path = generate_dct_path(compressed_image, secret_message)
        encoded_image = lsb_replacement_greyscale_encode(compressed_image, secret_message, hiding_path)
        token = encrypt_path(hiding_path, key)

        # Reading data
        reading_path = decrypt_path(token, key)
        text_binary = lsb_embedding_greyscale_decode(encoded_image, reading_path)
        secret_message = bits_to_text(text_binary)

        print("--- JPEG greyscale image, path encoding, LSB replacement ---")
        print(secret_message)
        self.assertEqual(secret_message, message)

    def test_plain_simple_colour_matching(self):
        message = "testing testing"
        image = imageio.imread("test_data/colour_image.jpg").astype(float)
        secret_message = text_to_bits(message)

        # Hiding data
        hiding_path = generate_simple_path(image)
        encoded_image = lsb_matching_colour_encode(image, secret_message, hiding_path)

        # Reading data
        reading_path = generate_simple_path(encoded_image)
        text_binary = lsb_embedding_colour_decode(encoded_image, reading_path)
        secret_message = bits_to_text(text_binary)

        print("--- Plain colour image, simple encoding, LSB matching ---")
        print(secret_message[0:len(message) + 10])
        self.assertEqual(secret_message[0:len(message)], message)

    def test_plain_simple_colour_replacement(self):
        message = "testing testing"
        image = imageio.imread("test_data/colour_image.jpg").astype(float)
        secret_message = text_to_bits(message)

        # Hiding data
        hiding_path = generate_simple_path(image)
        encoded_image = lsb_replacement_colour_encode(image, secret_message, hiding_path)

        # Reading data
        reading_path = generate_simple_path(encoded_image)
        text_binary = lsb_embedding_colour_decode(encoded_image, reading_path)
        secret_message = bits_to_text(text_binary)

        print("--- Plain colour image, simple encoding, LSB replacement ---")
        print(secret_message[0:len(message) + 10])
        self.assertEqual(secret_message[0:len(message)], message)

    def test_plain_simple_greyscale_matching(self):
        message = "testing testing"
        image = imageio.imread("test_data/greyscale_image.jpg").astype(float)
        secret_message = text_to_bits(message)

        # Hiding data
        hiding_path = generate_simple_path(image)
        encoded_image = lsb_matching_greyscale_encode(image, secret_message, hiding_path)

        # Reading data
        reading_path = generate_simple_path(encoded_image)
        text_binary = lsb_embedding_greyscale_decode(encoded_image, reading_path)
        secret_message = bits_to_text(text_binary)

        print("--- Plain greyscale image, simple encoding, LSB matching ---")
        print(secret_message[0:len(message) + 10])
        self.assertEqual(secret_message[0:len(message)], message)

    def test_plain_simple_greyscale_replacement(self):
        message = "testing testing"
        image = imageio.imread("test_data/greyscale_image.jpg").astype(float)
        secret_message = text_to_bits(message)

        # Hiding data
        hiding_path = generate_simple_path(image)
        encoded_image = lsb_replacement_greyscale_encode(image, secret_message, hiding_path)

        # Reading data
        reading_path = generate_simple_path(encoded_image)
        text_binary = lsb_embedding_greyscale_decode(encoded_image, reading_path)
        secret_message = bits_to_text(text_binary)

        print("--- Plain greyscale image, simple encoding, LSB replacement ---")
        print(secret_message[0:len(message) + 10])
        self.assertEqual(secret_message[0:len(message)], message)

    def test_plain_key_colour_matching(self):
        message = "testing testing"
        image = imageio.imread("test_data/colour_image.jpg").astype(float)
        key = "6u5UduLLCuIGM1oDMoy4A9SFK1NYJpnnF9eFjQiMtPY="
        key = key.encode("utf-8")
        secret_message = text_to_bits(message)

        # Hiding data
        hiding_path = generate_path_from_key(image, key)
        encoded_image = lsb_matching_colour_encode(image, secret_message, hiding_path)

        # Reading data
        reading_path = generate_path_from_key(encoded_image, key)
        text_binary = lsb_embedding_colour_decode(encoded_image, reading_path)
        secret_message = bits_to_text(text_binary)

        print("--- Plain colour image, key encoding, LSB matching ---")
        print(secret_message[0:len(message) + 10])
        self.assertEqual(secret_message[0:len(message)], message)

    def test_plain_key_colour_replacement(self):
        message = "testing testing"
        image = imageio.imread("test_data/colour_image.jpg").astype(float)
        key = "6u5UduLLCuIGM1oDMoy4A9SFK1NYJpnnF9eFjQiMtPY="
        key = key.encode("utf-8")
        secret_message = text_to_bits(message)

        # Hiding data
        hiding_path = generate_path_from_key(image, key)
        encoded_image = lsb_replacement_colour_encode(image, secret_message, hiding_path)

        # Reading data
        reading_path = generate_path_from_key(encoded_image, key)
        text_binary = lsb_embedding_colour_decode(encoded_image, reading_path)
        secret_message = bits_to_text(text_binary)

        print("--- Plain colour image, key encoding, LSB replacement ---")
        print(secret_message[0:len(message) + 10])
        self.assertEqual(secret_message[0:len(message)], message)

    def test_plain_key_greyscale_matching(self):
        message = "testing testing"
        image = imageio.imread("test_data/greyscale_image.jpg").astype(float)
        key = "6u5UduLLCuIGM1oDMoy4A9SFK1NYJpnnF9eFjQiMtPY="
        key = key.encode("utf-8")
        secret_message = text_to_bits(message)

        # Hiding data
        hiding_path = generate_path_from_key(image, key)
        encoded_image = lsb_matching_greyscale_encode(image, secret_message, hiding_path)

        # Reading data
        reading_path = generate_path_from_key(encoded_image, key)
        text_binary = lsb_embedding_greyscale_decode(encoded_image, reading_path)
        secret_message = bits_to_text(text_binary)

        print("--- Plain greyscale image, key encoding, LSB matching ---")
        print(secret_message[0:len(message) + 10])
        self.assertEqual(secret_message[0:len(message)], message)

    def test_plain_key_greyscale_replacement(self):
        message = "testing testing"
        image = imageio.imread("test_data/greyscale_image.jpg").astype(float)
        key = "6u5UduLLCuIGM1oDMoy4A9SFK1NYJpnnF9eFjQiMtPY="
        key = key.encode("utf-8")
        secret_message = text_to_bits(message)

        # Hiding data
        hiding_path = generate_path_from_key(image, key)
        encoded_image = lsb_replacement_greyscale_encode(image, secret_message, hiding_path)

        # Reading data
        reading_path = generate_path_from_key(encoded_image, key)
        text_binary = lsb_embedding_greyscale_decode(encoded_image, reading_path)
        secret_message = bits_to_text(text_binary)

        print("--- Plain greyscale image, key encoding, LSB replacement ---")
        print(secret_message[0:len(message) + 10])
        self.assertEqual(secret_message[0:len(message)], message)

    def test_plain_path_colour_matching(self):
        message = "testing testing"
        image = imageio.imread("test_data/colour_image.jpg").astype(float)
        key = "6u5UduLLCuIGM1oDMoy4A9SFK1NYJpnnF9eFjQiMtPY="
        key = key.encode("utf-8")
        secret_message = text_to_bits(message)

        # Hiding data
        hiding_path = generate_path_from_key(image, key)
        encoded_image = lsb_matching_colour_encode(image, secret_message, hiding_path)
        token = encrypt_path(hiding_path, key)

        # Reading data
        reading_path = decrypt_path(token, key)
        text_binary = lsb_embedding_colour_decode(encoded_image, reading_path)
        secret_message = bits_to_text(text_binary)

        print("--- Plain colour image, path encoding, LSB matching ---")
        print(secret_message[0:len(message) + 10])
        self.assertEqual(secret_message[0:len(message)], message)

    def test_plain_path_colour_replacement(self):
        message = "testing testing"
        image = imageio.imread("test_data/colour_image.jpg").astype(float)
        key = "6u5UduLLCuIGM1oDMoy4A9SFK1NYJpnnF9eFjQiMtPY="
        key = key.encode("utf-8")
        secret_message = text_to_bits(message)

        # Hiding data
        hiding_path = generate_path_from_key(image, key)
        encoded_image = lsb_replacement_colour_encode(image, secret_message, hiding_path)
        token = encrypt_path(hiding_path, key)

        # Reading data
        reading_path = decrypt_path(token, key)
        text_binary = lsb_embedding_colour_decode(encoded_image, reading_path)
        secret_message = bits_to_text(text_binary)

        print("--- Plain colour image, path encoding, LSB replacement ---")
        print(secret_message[0:len(message) + 10])
        self.assertEqual(secret_message[0:len(message)], message)

    def test_plain_path_greyscale_matching(self):
        message = "testing testing"
        image = imageio.imread("test_data/greyscale_image.jpg").astype(float)
        key = "6u5UduLLCuIGM1oDMoy4A9SFK1NYJpnnF9eFjQiMtPY="
        key = key.encode("utf-8")
        secret_message = text_to_bits(message)

        # Hiding data
        hiding_path = generate_path_from_key(image, key)
        encoded_image = lsb_matching_greyscale_encode(image, secret_message, hiding_path)
        token = encrypt_path(hiding_path, key)

        # Reading data
        reading_path = decrypt_path(token, key)
        text_binary = lsb_embedding_greyscale_decode(encoded_image, reading_path)
        secret_message = bits_to_text(text_binary)

        print("--- Plain greyscale image, path encoding, LSB matching ---")
        print(secret_message[0:len(message) + 10])
        self.assertEqual(secret_message[0:len(message)], message)

    def test_plain_path_greyscale_replacement(self):
        message = "testing testing"
        image = imageio.imread("test_data/greyscale_image.jpg").astype(float)
        key = "6u5UduLLCuIGM1oDMoy4A9SFK1NYJpnnF9eFjQiMtPY="
        key = key.encode("utf-8")
        secret_message = text_to_bits(message)

        # Hiding data
        hiding_path = generate_path_from_key(image, key)
        encoded_image = lsb_replacement_greyscale_encode(image, secret_message, hiding_path)
        token = encrypt_path(hiding_path, key)

        # Reading data
        reading_path = decrypt_path(token, key)
        text_binary = lsb_embedding_greyscale_decode(encoded_image, reading_path)
        secret_message = bits_to_text(text_binary)

        print("--- Plain greyscale image, path encoding, LSB replacement ---")
        print(secret_message[0:len(message) + 10])
        self.assertEqual(secret_message[0:len(message)], message)


if __name__ == '__main__':
    unittest.main()
