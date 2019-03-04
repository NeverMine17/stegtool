import logging

import click
import coloredlogs
from PIL.Image import open as pillow_open

from stegtool.image_writer import ImageWriter


@click.group()
@click.option('--verbose/--not-verbose', default=False)
def cli(verbose):
    coloredlogs.install(level=logging.DEBUG if verbose else logging.INFO)


@click.command()
@click.option('-i', '--infile', help='Path to the source file')
def decode(infile):
    logging.basicConfig(level=logging.DEBUG)
    print(ImageWriter(pillow_open(infile)).read().decode())


@click.command()
@click.option('-i', '--infile', help='Path to the source file')
@click.option('-o', '--outfile', help='Path to the source file')
@click.option('--data', required=True, help='Data to encode')
def encode(infile, outfile, data):
    logging.basicConfig(level=logging.DEBUG)
    imgwrt = ImageWriter(pillow_open(infile))
    imgwrt.write(data.encode())
    imgwrt.image.save(outfile)


if __name__ == "__main__":
    cli.add_command(decode)
    cli.add_command(encode)
    cli()
