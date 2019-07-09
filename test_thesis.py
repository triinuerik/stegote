import unittest
from main import *
import codec


class Tests(unittest.TestCase):
    """
    Unit tests for testing all the different hiding combinations: JPEG or plain image, simple or key or path encoding,
    LSB matching or LSB replacement embedding and greyscale or colour image.

    Each test is composed of the data hiding and data reading part.
    """

    def test_jpeg_zigzag_colour(self):
        message = "testing testing"
        image = imageio.imread("test_data/colour_image.jpg").astype(float)
        secret_message = text_to_bits(message)

        # Hiding data
        encoded_image = codec.jpeg_zigzag_encode(image, secret_message)

        # Reading data
        reading_path = generate_zigzag_dct_path(encoded_image)
        text_binary = lsb_embedding_colour_decode(encoded_image, reading_path)
        secret_message = bits_to_text(text_binary)

        print("--- JPEG colour image, zigzag encoding, LSB matching ---")
        print(secret_message[0:len(message) + 10])
        self.assertEqual(secret_message[0:len(message)], message)

    def test_jpeg_zigzag_greyscale(self):
        message = "testing testing"
        image = imageio.imread("test_data/greyscale_image.jpg").astype(float)
        secret_message = text_to_bits(message)

        # Hiding data
        encoded_image = codec.jpeg_zigzag_encode(image, secret_message)

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
        encoded_image = codec.jpeg_key_encode_matching(image, secret_message, key)

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
        encoded_image = codec.jpeg_key_encode_matching(image, secret_message, key)

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
        encoded_image, token = codec.jpeg_path_encode_matching(image, secret_message, key)

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
        encoded_image, token = codec.jpeg_path_encode_replacement(image, secret_message, key)

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
        encoded_image, token = codec.jpeg_path_encode_matching(image, secret_message, key)

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
        encoded_image, token = codec.jpeg_path_encode_replacement(image, secret_message, key)

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
        encoded_image = codec.image_simple_encode_matching(image, secret_message)

        # Reading data
        secret_message = codec.image_simple_decode(encoded_image)

        print("--- Plain colour image, simple encoding, LSB matching ---")
        print(secret_message[0:len(message) + 10])
        self.assertEqual(secret_message[0:len(message)], message)

    def test_plain_simple_colour_replacement(self):
        message = "testing testing"
        image = imageio.imread("test_data/colour_image.jpg").astype(float)
        secret_message = text_to_bits(message)

        # Hiding data
        encoded_image = codec.image_simple_encode_replacement(image, secret_message)

        # Reading data
        secret_message = codec.image_simple_decode(encoded_image)

        print("--- Plain colour image, simple encoding, LSB replacement ---")
        print(secret_message[0:len(message) + 10])
        self.assertEqual(secret_message[0:len(message)], message)

    def test_plain_simple_greyscale_matching(self):
        message = "testing testing"
        image = imageio.imread("test_data/greyscale_image.jpg").astype(float)
        secret_message = text_to_bits(message)

        # Hiding data
        encoded_image = codec.image_simple_encode_matching(image, secret_message)

        # Reading data
        secret_message = codec.image_simple_decode(encoded_image)

        print("--- Plain greyscale image, simple encoding, LSB matching ---")
        print(secret_message[0:len(message) + 10])
        self.assertEqual(secret_message[0:len(message)], message)

    def test_plain_simple_greyscale_replacement(self):
        message = "testing testing"
        image = imageio.imread("test_data/greyscale_image.jpg").astype(float)
        secret_message = text_to_bits(message)

        # Hiding data
        encoded_image = codec.image_simple_encode_replacement(image, secret_message)

        # Reading data
        secret_message = codec.image_simple_decode(encoded_image)

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
        encoded_image = codec.image_key_encode_matching(image, secret_message, key)

        # Reading data
        secret_message = codec.image_key_decode(encoded_image, key)

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
        encoded_image = codec.image_key_encode_replacement(image, secret_message, key)

        # Reading data
        secret_message = codec.image_key_decode(encoded_image, key)

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
        encoded_image = codec.image_key_encode_matching(image, secret_message, key)

        # Reading data
        secret_message = codec.image_key_decode(encoded_image, key)

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
        encoded_image = codec.image_key_encode_replacement(image, secret_message, key)

        # Reading data
        secret_message = codec.image_key_decode(encoded_image, key)

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
        encoded_image, token = codec.image_path_encode_matching(image, secret_message, key)

        # Reading data
        secret_message = codec.image_path_decode(encoded_image, key, token)

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
        encoded_image, token = codec.image_path_encode_replacement(image, secret_message, key)

        # Reading data
        secret_message = codec.image_path_decode(encoded_image, key, token)

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
        # Hiding data
        encoded_image, token = codec.image_path_encode_matching(image, secret_message, key)

        # Reading data
        secret_message = codec.image_path_decode(encoded_image, key, token)

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
        encoded_image, token = codec.image_path_encode_replacement(image, secret_message, key)

        # Reading data
        secret_message = codec.image_path_decode(encoded_image, key, token)

        print("--- Plain greyscale image, path encoding, LSB replacement ---")
        print(secret_message[0:len(message) + 10])
        self.assertEqual(secret_message[0:len(message)], message)


if __name__ == '__main__':
    unittest.main()
