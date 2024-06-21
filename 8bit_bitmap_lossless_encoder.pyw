from tkinter import *
from tkinter import filedialog
from tkinter import ttk

def Kompressor(filename):
    oldbyte=0
    newbyte=0
    repeat=1
    index=1
    tempdata=""
    newdata=""
    words=0
    length=0

    file=open(filename, 'rb')

    data=(file.read())

    width=(int(data[18]))+int(data[19]*256)
    height=(int(data[22]))+int(data[23]*256)
    
    bitdepth=1
    print("image width = ",width," pixels")
    print("image width = ",height," pixels")

    filesize=len(data)
    imagesize=width*height
    print("filesize(bytes) =",filesize)
    print("imagesize(bytes) =",imagesize)


    print("***************************************Pass 1********************************************************** ")

    #                   end of file(TOP) TO beginning of file(BOTTOM), step (- width) 
    for line in range(filesize-width,(filesize-(imagesize+width)),-(width)): # width is the length of each line, we start at the end of the file -120 bytes
           
        for every2bytes in range(line,line+width,bitdepth): #step 1 for 256 color, step 2 for 16 color
            byte=str((data[every2bytes]))+","
            if byte=="8,":
                byte="246," # If we need white, we paint with Grey-green and change it here to 246 white
            tempdata+=byte

    array=list(tempdata.split(","))
    array.remove('')

    array = [int(item) for item in array]


    # #test data
    # array=[0,210,47,255,255,255,255,255,255,255,255,0,153,0,153,0,147,147,0,0,255,255,45,255,255,255,255,255,0,0,0,0,
    #        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
    #        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
    #        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,87,128,128,128,1,2,3,4,5,6,97,97,97,97,6,
    #        7,7,8,9,9,0,0,0,0,0,8,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,210,47,255,255,255,255,255,255,255,255,0,153,0,153,0,147,147,0,0,255,255,45,255,255,255,255,255,0,0,0,0,
    #        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
    #        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
    #        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,87,128,128,128,1,2,3,4,5,6,97,97,97,97,6,
    #        7,7,8,9,9,0,0,0,0,0,8,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #last 2 elements are padding


    length=(len(array))

    print("***************************************Pass 2********************************************************** ")
    same=1
    different=0
    samestring=""
    differentstring=""
    intermediatestring=""
    finalstring=""
    tempstring=""

    intermediatedata=[]
    finaldata=[]
    for index in range(1,length-1,1):
        if array[index-1]==array[index]:
            if same==1:
                samestring=str(array[index-1])+","
            same+=1
            if same==128:
                intermediatestring+=str(255)+","+str(array[index])+","
                same=1
            continue
            
        if array[index-1]!=array[index] and same>1:
            samestring=str(same+128)+","+samestring
            intermediatestring+=samestring
            samestring=""
            same=1

        

        if array[index-1]!=array[index] and same==1:
            
            #if this is so, there are 3 possibilites to check for:
            if array[index]==array[index+1]: #we have a block coming up
                continue
            
            intermediatestring+=str(same)+","+str(array[index])+"," #going solo
    intermediatestring+="0,0" #2 digit padding
    intermediatedata=intermediatestring.split(",")
    #intermediatedata.remove('')
    interdata = [int(i) for i in intermediatedata]

    #print(interdata)

    for i in range(0,len(interdata)-2,2):
        if interdata[i]!=1:
            finalstring+=str(interdata[i])+","+str(interdata[i+1])+","
            continue
        if interdata[i] ==1:
            tempstring+=str(interdata[i+1])+","
            different+=1
            

        if interdata[i+2]>1:
            finalstring+=str(different)+","+tempstring
            different=0
            tempstring=""

    finalstring+=str(interdata[i])+","+str(interdata[i+1])
    
    finalstring="0,0,0,0,"+finalstring #add the header data bytes


    finalarray=finalstring.split(",")
    #finalarray.remove('')
    finalarray= [int(item) for item in finalarray]
    length=len(finalarray)+4
    finalarray[0]=8
    finalarray[1]=width
    finalarray[2]=int(length/256) #MSB
    finalarray[3]=length-((int(length/256))*256) #LSB
    print(finalarray)

    print("incoming file size :",filesize)
    print("incoming data with formatting removed :",len(array))

    print("outgoing file size after compression :",length)
    #data.close
    return finalarray

root = Tk()
root.geometry("480x480")
myLabel = Label(root, text="")
filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select an 8 bit color Bit Map File",
                                          filetypes = (("BMP files",
                                                        "*.bmp*"),
                                                       ))
myLabel.pack()

finalarray=Kompressor(filename)

root.resizable(False, False)
root.title("8 bit color bitmap lossless encoder")

# apply the grid layout
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

# create the text widget
text = Text(root)

text['state'] = 'normal'
text.pack()

text.insert('1.0', finalarray)
text.insert('1.0',"Compressed output, copy and paste it to your editor....    ")


root.mainloop()

    
    
        








             
    




        