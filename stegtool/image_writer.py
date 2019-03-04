from typing import Optional

import unireedsolomon

from stegtool.image_cursor import ImageCursor


class ImageWriter:
    def __init__(self, cursor: ImageCursor, use_ecc: Optional[bool] = False):
        self.use_ecc = use_ecc
        self.cursor = cursor
        self.ecc = unireedsolomon.RSCoder

    def write(self, data: bytes):
        """DOES NOT WORK"""
        data = [data[i:i+64] for i in range(0, len(data), 64)]
        new_data = b''
        for data_block in data:
            new_data += self.ecc(96, 64).encode(data_block)
        len_data = len(new_data).to_bytes(8, 'little', signed=False)
        temp = bytes(self.ecc(16, 8).encode_fast(len_data, return_string=False))
        self.cursor.write(temp)

        self.cursor.image.save('imageout2.png')

    def read(self):
        header = self.cursor.read(16).bytes
        header_val = int.from_bytes(bytes(self.ecc(16, 8).decode_fast(header, return_string=False)[0]), 'little',
                                    signed=False)
        if header_val % 96 != 0:
            raise ValueError('header must be dividable by block size 96')

        rest_of_data = self.cursor.read(header_val)
        return rest_of_data
