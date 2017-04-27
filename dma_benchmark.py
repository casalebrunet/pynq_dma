import argparse
import logging
import time
import numpy as np
from pynq import Overlay
from pynq import PL
from pynq.drivers.dma import DMA
from pynq.drivers.dma import ffi

## Command line parsing
parser = argparse.ArgumentParser(description='Pynq DMA benchmark.')
parser = argparse.ArgumentParser()
parser.add_argument("-d", help="the size in MB of the transmitted/received buffer", type=int, default=1)
parser.add_argument("-n", help="the number of test that should be performed", type=int, default=1000)
parser.add_argument("-v", help="Verbose mode", default=False, action="store_true")
args = parser.parse_args()

MB       = args.d # MB of the arry
NUM_TEST = args.n # Number of benchmark tests
VERBOSE  = args.v # Verbose logging

logging.basicConfig(format='%(levelname)s: %(message)s', level = logging.DEBUG if VERBOSE else  logging.INFO)

logging.debug("Configuration: MB={}, NUM_TEST={}".format(MB, NUM_TEST))

# Load the overlay
logging.info("Loading Overlay...");
start = time.time()
ol = Overlay("dma_benchmark.bit")
ol.download()
end = time.time()

if not ol.is_loaded():
	logging.error("The overlay can not be loaded!")
	exit(-1)

logging.info("Overlay loaded in {0:.4f}s".format(end-start));
logging.debug("Overlay info: [{}, {}]".format(PL.bitfile_name, ol.bitstream.timestamp))


# DMA buffer for Transferring from PS-PL
TXdma = DMA(0x40400000, direction=0)
# DMA buffer for Transferring from PL-PS
RXdma = DMA(0x40400000, direction=1) 

logging.debug("DMA configuration:")
logging.debug(TXdma.Configuration)
logging.debug(RXdma.Configuration)

# Configure overlay
logging.info("Configuring DMA...")
TXdma.configure()
RXdma.configure()

# Compute data and size
elem = int(MB * 1024 * 1024 / np.array([0]).nbytes) # Number of elements stored in the buffer
data = np.array(range(elem))
size = data.nbytes

# Create buffers
TXdma.create_buf(size)
RXdma.create_buf(size)

buf_tx = ffi.buffer(TXdma.buf, size)
view_tx = np.frombuffer(buf_tx, np.int32,-1)
view_tx[:] = data

# Launch a single transfer
logging.info("Sending/Receiving data ({}MB)...".format(MB))
TXdma.transfer(size,direction=0)
RXdma.transfer(size,direction=1) 
TXdma.wait()
RXdma.wait()

# Get RX data
buf_rx = ffi.buffer(RXdma.buf, size)
view_rx = np.frombuffer(buf_rx, np.int32,-1)

# Compare RX with TX data
if (view_tx == view_rx).all() :
	logging.info("Test passed!")
else :
	logging.error("TX and RX values do not match....")
	exit(-1) 

# Launch benchmark
logging.info("Launching benchmark (this could take a while)...")

start = time.time()
for x in range(0, NUM_TEST):
	TXdma.transfer(size,direction=0)
	RXdma.transfer(size,direction=1) 
	TXdma.wait()
	RXdma.wait()
end = time.time()

logging.info("Throughput: {0:.2f}MB/s".format(NUM_TEST * MB / (end - start)))



