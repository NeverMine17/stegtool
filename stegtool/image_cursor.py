import logging

from PIL.Image import Image
from bitstring import *

logger = logging.getLogger('stegtool')


class ImageCursor:
    def __init__(self, image: Image):
        self.channel_num = 2
        self.curr_x = 0
        self.curr_y = 0
        self.image = image
        self.curr_bit = 1
        self.already_wrote = 0

    @property
    def bits_available(self):
        return self.image.size[0] * self.image.size[1] - self.already_wrote

    def iterate(self):
        self.curr_x += 1
        if self.curr_x == self.image.size[0] - 1:
            self.curr_x = 0
            self.curr_y += 1
        self.already_wrote += 1
        if (self.bits_available % 200) == 0:
            logger.debug('Bits available: {0}'.format(self.bits_available))

    def write_at(self, x, y, bit: bool):
        before = self.image.getpixel((x, y))
        blue_value_mod = list(bin(before[2])[2:].zfill(8))
        blue_value_mod[7] = str(int(bit))
        self.image.putpixel((x, y), (before[0], before[1], int(''.join(blue_value_mod), 2)))

    def read_at(self, x, y):
        return bin(
            self.image.getpixel((x, y))[2]
        )[2:].zfill(8)[7] == '1'

    @property
    def size_left(self):
        return self.image.size[0] * self.image.size[1]

    def write(self, bytes_: bytes):
        for bit in BitArray(bytes_):
            self.write_at(self.curr_x, self.curr_y, bit)
            self.iterate()

    def read(self, bytes_: int):
        buffer = BitArray()
        for bit in range(bytes_ * 8):
            buffer.append(BitString([self.read_at(self.curr_x, self.curr_y)]))
            self.iterate()

        return buffer.bytes

    def reset(self):
        self.curr_x = 0
        self.curr_y = 0
