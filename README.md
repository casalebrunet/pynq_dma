# PYNQ DMA

This repository contains a PYNQ DMA benchmark project. The Vivado design contains only the PS, the DMA and an AXI4-Stream Data FIFO. 
The FIFO is used to make a feedback loop between the MM2S and S2MM of the DMA.

![Vivado Block Design](https://raw.githubusercontent.com/casalebrunet/pynq_dma/master/vivado/img/block_design.png)

## Launch the program

Upload the files on the PYNQ and use the launch.sh script


```
$./launch.sh [-d] [-n] 
```

where ```-d``` is the size in MB of the transmitted/received buffer and ```n``` is the number of tests that should be performed.


Please note that the script should be launched from the console of your PYNQ. I have no made any Jupyter Notebook. If you like that you can use the content of ```dma_benchmark.py```. 

## Vivado Project

In the folder vivado of this repository there is a tcl script that can be used to rebuild the overlay with Vivado 2016.1. Please note that is a simplified version of the base overlay provided by Avnet.

```
vivado -mode batch -source build.tcl
```
