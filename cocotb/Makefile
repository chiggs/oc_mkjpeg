TOPLEVEL=JpegEnc
MODULE=test_jpeg_encoder


SIM?=aldec
TOLEVEL_LANG=vhdl
GPI_IMPL=vhpi

PWD=$(shell pwd)

VERILOG_SOURCES = $(PWD)/../design/mdct/FinitePrecRndNrst.v \
                  $(PWD)/../design/JFIFGen/HeaderRAM.v

VHDL_SOURCES = $(PWD)/../design/common/JPEG_PKG.vhd \
               $(PWD)/../design/common/RAMZ.VHD \
               $(PWD)/../design/common/FIFO.vhd \
               $(PWD)/../design/common/SingleSM.vhd \
               $(PWD)/../design/BufFifo/multiplier.vhd \
               $(PWD)/../design/BufFifo/SUB_RAMZ_LUT.vhd \
               $(PWD)/../design/BufFifo/SUB_RAMZ.VHD \
               $(PWD)/../design/BufFifo/BUF_FIFO.vhd \
               $(PWD)/../design/mdct/MDCT_PKG.vhd \
               $(PWD)/../design/mdct/ROMO.VHD \
               $(PWD)/../design/mdct/ROME.VHD \
               $(PWD)/../design/mdct/RAM.VHD \
               $(PWD)/../design/mdct/DBUFCTL.VHD \
               $(PWD)/../design/mdct/DCT1D.vhd \
               $(PWD)/../design/mdct/DCT2D.VHD \
               $(PWD)/../design/mdct/MDCT.VHD \
               $(PWD)/../design/mdct/FDCT.vhd \
               $(PWD)/../tb/vhdl/DCT_TROM.vhd \
               $(PWD)/../design/quantizer/ROMQ.vhd \
               $(PWD)/../design/quantizer/s_divider.vhd \
               $(PWD)/../design/quantizer/ROMR.vhd \
               $(PWD)/../design/quantizer/r_divider.vhd \
               $(PWD)/../design/quantizer/QUANTIZER.vhd \
               $(PWD)/../design/quantizer/QUANT_TOP.VHD \
               $(PWD)/../design/zigzag/ZIGZAG.VHD \
               $(PWD)/../design/zigzag/ZZ_TOP.VHD \
               $(PWD)/../design/rle/RleDoubleFifo.vhd \
               $(PWD)/../design/rle/RLE.VHD \
               $(PWD)/../design/rle/RLE_TOP.VHD \
               $(PWD)/../design/huffman/DoubleFifo.vhd \
               $(PWD)/../design/huffman/DC_ROM.vhd \
               $(PWD)/../design/huffman/AC_ROM.vhd \
               $(PWD)/../design/huffman/DC_CR_ROM.vhd \
               $(PWD)/../design/huffman/AC_CR_ROM.vhd \
               $(PWD)/../design/huffman/Huffman.vhd \
               $(PWD)/../design/bytestuffer/ByteStuffer.vhd \
               $(PWD)/../design/control/CtrlSM.vhd \
               $(PWD)/../design/hostif/HostIF.vhd \
               $(PWD)/../design/iramif/IRAMIF.vhd \
               $(PWD)/../design/JFIFGen/JFIFGen.vhd \
               $(PWD)/../design/outmux/OutMux.vhd \
               $(PWD)/../design/top/JpegEnc.vhd

ASIM_ARGS += -ieee_nowarn

include $(COCOTB)/makefiles/Makefile.inc
include $(COCOTB)/makefiles/Makefile.sim

