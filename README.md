Written in Python, just run it, selected a BMP file(8 bit only) and then copy the output text and paste it into your IDE. 
This reads in the data from the BMP, reformats it so it is in a top-down format and then simply checks for consecutive pixels of the same color and encodes them as a block.

Compression ratio varies, but typically between 25-50%, which is good enough for the use case of encoding icons and small graphical items.
Companion decompressor is written in CCS C for PIC MCUs and lookup RGB table.
These will be uploaded shortly.
