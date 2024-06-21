Encoder is written in Python. Just run it, selected a BMP file(8 bit only) and then copy the output text and paste it into your text editor or IDE. 
This reads in the data from the BMP, reformats it so it is in a top-down format and then simply checks for blocks of pixels of the same color or blocks of different color pixels until a same-color block is encountered and encodes them as such.

Compression ratio varies, but typically between 25-50%, which is good enough for the use case of encoding icons and small graphical items.
Companion decompressor is written in CCS C for PIC MCUs and lookup RGB table.

