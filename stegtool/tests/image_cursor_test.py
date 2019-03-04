import unittest

from PIL.Image import new
from bitstring import BitArray

from stegtool import image_cursor


class ImageCursorTest(unittest.TestCase):
    def test_write_at(self):
        test_img = new('RGB', (1, 1))
        test_img.putpixel((0, 0), (0, 0, 0))
        cur = image_cursor.ImageCursor(test_img, 2)
        cur.write_at(0, 0, True)
        self.assertEqual(test_img.getpixel((0, 0))[2], 1)

    def test_write(self):
        test_img = new('RGB', (8, 1))
        test_img.putpixel((0, 0), (0, 0, 0))
        cur = image_cursor.ImageCursor(test_img, 2)
        cur.write(bytes.fromhex('ff'))
        self.assertEqual(cur.image.getpixel((0, 0))[2], 1)
        self.assertEqual(cur.image.getpixel((1, 0))[2], 1)
        self.assertEqual(cur.image.getpixel((2, 0))[2], 1)
        self.assertEqual(cur.image.getpixel((3, 0))[2], 1)
        self.assertEqual(cur.image.getpixel((4, 0))[2], 1)
        self.assertEqual(cur.image.getpixel((5, 0))[2], 1)
        self.assertEqual(cur.image.getpixel((6, 0))[2], 1)
        self.assertEqual(cur.image.getpixel((7, 0))[2], 1)

    def test_read_at(self):
        test_img = new('RGB', (1, 1))
        test_img.putpixel((0, 0), (0, 0, 1))
        cur = image_cursor.ImageCursor(test_img, 2)
        self.assertEqual(cur.read_at(0, 0), True)

    def test_read(self):
        test_img = new('RGB', (8, 1))
        test_img.putpixel((0, 0), (0, 0, 1))
        test_img.putpixel((1, 0), (0, 0, 0))
        test_img.putpixel((2, 0), (0, 0, 1))
        test_img.putpixel((3, 0), (0, 0, 1))
        test_img.putpixel((4, 0), (0, 0, 1))
        test_img.putpixel((5, 0), (0, 0, 0))
        test_img.putpixel((6, 0), (0, 0, 1))
        test_img.putpixel((7, 0), (0, 0, 1))
        cur = image_cursor.ImageCursor(test_img, 2)
        self.assertEqual(cur.read(1), BitArray([1, 0, 1, 1, 1, 0, 1, 1]))
