import logging

import unireedsolomon
from PIL.Image import Image

from stegtool.image_cursor import ImageCursor

logger = logging.getLogger('stegtool')


class ImageWriter:
    def __init__(self, image: Image):
        self.cursor = ImageCursor(image)
        self.ecc = unireedsolomon.RSCoder

    @property
    def image(self):
        return self.cursor.image

    def write(self, data: bytes):
        logger.info('Starting to encode the message...')
        logger.debug('Encoding data into blocks...')
        data = [data[i:i + 64] for i in range(0, len(data), 64)]
        new_data = b''

        for data_block in data:
            new_data += bytes(self.ecc(96, 64).encode(data_block, return_string=False))

        logger.debug('Finished encoding data')
        logger.debug('Computing data length...')

        len_data = len(new_data).to_bytes(8, 'little', signed=False)

        logger.debug('Computed data length, it is {} bytes'.format(len(new_data)))

        temp = bytes(self.ecc(16, 8).encode_fast(len_data, return_string=False))
        self.cursor.write(temp)
        self.cursor.write(new_data)

    def read(self):
        logger.info('Starting to decode data')
        header = self.cursor.read(16)
        print(repr(header))
        header_val = int.from_bytes(bytes(self.ecc(16, 8).decode_fast(header, return_string=False)[0]), 'little',
                                    signed=False)

        logger.debug('Got data length, it is {} bytes'.format(header_val))

        if header_val % 96 != 0:
            logging.exception('Data length must be dividable by block size 96')
            raise ValueError('Data length must be dividable by block size 96')
        data = self.cursor.read(header_val)
        data = [data[i:i + 96] for i in range(0, len(data), 96)]

        if len(data[len(data) - 1]) != 96:
            logging.exception('Last block is not 96 bytes long')
            raise ValueError('Last block is not 96 bytes long')

        data = b''.join([bytes(self.ecc(96, 64).decode(chunk, return_string=False)[0]) for chunk in data])

        return data

    def reset(self):
        self.cursor.reset()
