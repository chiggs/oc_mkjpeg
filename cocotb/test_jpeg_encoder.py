"""
Example of using Cocotb to send image files in to the opencores JPEG Encoder
and check that the output is sufficiently similar to the input.

NB Limited to 96x96 images since we're using a static JPEG header.
"""
import os

import logging
from collections import defaultdict
from itertools import izip
from PIL import Image

import cocotb
from cocotb.triggers import RisingEdge, ReadOnly
from cocotb.result import TestFailure
from cocotb.regression import TestFactory
from cocotb.clock import Clock
from cocotb.drivers.opb import OPBMaster
from cocotb.monitors import Monitor


class OutputMonitor(Monitor):

    def __init__(self, dut):
        self.dut = dut
        self.bytes = defaultdict()
        Monitor.__init__(self)


    @cocotb.coroutine
    def _monitor_recv(self):
        while True:
            yield RisingEdge(self.dut.CLK)
            yield ReadOnly()                
            

ENC_START_REG = 0x0
IMAGE_SIZE_REG = 0x4
ENC_STS_REG = 0xC
ENC_LENGTH_REG = 0x14
QUANTIZER_RAM_LUM = 0x100
QUANTIZER_RAM_CHR = 0x200

JPEG_DONE = 0x02
JPEG_RGB = (0x3<<1)
JPEG_ENABLE = 0x1

ROM_LUM = [
   0x10, 0x0B, 0x0C, 0x0E, 0x0C, 0x0A, 0x10, 0x0E, 
   0x0D, 0x0E, 0x12, 0x11, 0x10, 0x13, 0x18, 0x28,
   0x1A, 0x18, 0x16, 0x16, 0x18, 0x31, 0x23, 0x25, 
   0x1D, 0x28, 0x3A, 0x33, 0x3D, 0x3C, 0x39, 0x33,
   0x38, 0x37, 0x40, 0x48, 0x5C, 0x4E, 0x40, 0x44, 
   0x57, 0x45, 0x37, 0x38, 0x50, 0x6D, 0x51, 0x57,
   0x5F, 0x62, 0x67, 0x68, 0x67, 0x3E, 0x4D, 0x71, 
   0x79, 0x70, 0x64, 0x78, 0x5C, 0x65, 0x67, 0x63]


ROM_CHROM = [
  0x11, 0x12, 0x12, 0x18, 0x15, 0x18, 0x2F, 0x1A, 
  0x1A, 0x2F, 0x63, 0x42, 0x38, 0x42, 0x63, 0x63,
  0x63, 0x63, 0x63, 0x63, 0x63, 0x63, 0x63, 0x63, 
  0x63, 0x63, 0x63, 0x63, 0x63, 0x63, 0x63, 0x63,
  0x63, 0x63, 0x63, 0x63, 0x63, 0x63, 0x63, 0x63, 
  0x63, 0x63, 0x63, 0x63, 0x63, 0x63, 0x63, 0x63,
  0x63, 0x63, 0x63, 0x63, 0x63, 0x63, 0x63, 0x63, 
  0x63, 0x63, 0x63, 0x63, 0x63, 0x63, 0x63, 0x63]


class JPEGTestBench(object):

    def __init__(self, dut, debug=True):
        self.dut = dut
        self.master = OPBMaster(dut, "OPB", dut.CLK)
        self.monitor = OutputMonitor(self.dut)

    @cocotb.coroutine
    def initialise(self):
        cocotb.fork(Clock(self.dut.CLK, 100).start())
        self.dut.RST = 1
        for i in range(10):
            yield RisingEdge(self.dut.CLK)
        self.dut.RST = 0
        yield RisingEdge(self.dut.CLK)

        self.dut.log.info("Programming Luminance ROM...")
        for index, value in enumerate(ROM_LUM):
            yield self.master.write(QUANTIZER_RAM_LUM + index*4, value)


        self.dut.log.info("Programming Chrom ROM...")
        for index, value in enumerate(ROM_CHROM):
            yield self.master.write(QUANTIZER_RAM_CHR + index*4, value)

        self.dut.log.info("JPEG Encoder initialised")

    
    @cocotb.coroutine
    def encode(self, image):

        yield self.master.write(ENC_START_REG, JPEG_RGB | JPEG_ENABLE)

        width, height = image.size
        pixels = image.load()

        yield self.master.write(IMAGE_SIZE_REG, (width<<16) | height)

        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                self.dut.iram_wdata = ((b<<16) | (g<<8) | r)
                self.dut.iram_wren = 1
                while True:
                    yield RisingEdge(self.dut.CLK)
                    if not int(self.dut.iram_fifo_afull):
                        break
                self.dut.iram_wren = 0

        self.dut.log.info("Waiting for encoding to complete")
        while True:
            result = yield self.master.read(ENC_STS_REG)
            if int(result) == JPEG_DONE:
                break


def compare(i1, i2):
    """
    Compare the similarity of two images

    From http://rosettacode.org/wiki/Percentage_difference_between_images
    """
    assert i1.mode == i2.mode, "Different kinds of images."
    assert i1.size == i2.size, "Different sizes."

    pairs = izip(i1.getdata(), i2.getdata())
    dif = sum(abs(c1-c2) for p1,p2 in pairs for c1,c2 in zip(p1,p2))
    ncomponents = i1.size[0] * i1.size[1] * 3
    return (dif / 255.0 * 100) / ncomponents


@cocotb.test(skip=True)
def initial_test(dut):
    cocotb.fork(Clock(dut.CLK, 100).start())
    master = OPBMaster(dut, "OPB", dut.CLK)

    dut.RST = 1
    for i in range(10):
        yield RisingEdge(dut.CLK)
    dut.RST = 0
    yield RisingEdge(dut.CLK)
    dut.log.info("Out of reset")
    yield master.read(0)
    yield master.write(0, 0xFFFFFFFF)
    result = yield master.read(0)
    dut.log.info(repr(result))


@cocotb.coroutine
def process_image(dut, filename="", debug=False, threshold=0.22):
    """Run an image file through the jpeg encoder and compare the result"""

    tb = JPEGTestBench(dut, debug=debug)
    yield tb.initialise()

    stimulus = Image.open(filename)
    yield tb.encode(stimulus)

tf = TestFactory(process_image)
tf.add_option("filename", [os.path.join('../test_images', f)
                            for f in os.listdir('../test_images')])
tf.generate_tests()

