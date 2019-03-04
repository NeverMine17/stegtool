import unittest
from os import path

from PIL.Image import open as pillow_open

from stegtool.image_writer import ImageWriter


class ImageWriterTest(unittest.TestCase):
    def test_normal(self):
        img = pillow_open(path.join('data_examples', 'input.png'))
        imgwrt = ImageWriter(img)
        imgwrt.write(b'123testing123')
        imgwrt.reset()
        self.assertEqual(imgwrt.read(), b'123testing123')
        self.assertEqual(imgwrt.cursor.already_wrote, 1792)


if __name__ == '__main__':
    unittest.main()
