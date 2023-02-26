import cv2
from rapidgui import quickGui
import pyaudio
import traceback

import numpy

# chunk = 1024
#  pyaudio.paFloat32
 
WIDTH = 640
HEIGHT = 480
 
pad = pyaudio.PyAudio()
stream = pad.open(
    format = pyaudio.paInt32,
    channels = 2,
    rate = 44100,
    input=True
    )

canvas = numpy.zeros((HEIGHT,WIDTH,3), dtype=numpy.uint8)
fftHist = numpy.zeros((HEIGHT,WIDTH,3), dtype=numpy.uint8)

mmax = 10000

def draw():
    cv2.imshow("output", canvas)
    cv2.waitKey(1)

try:
    while True:
        data = stream.read(4086)

        fdata = numpy.reshape(numpy.frombuffer(data, dtype=numpy.int32), (-1,2) )
        
        
        cfdata = fdata[:,1]
        rfftdata = numpy.fft.fft(cfdata)
        
        fftdata = rfftdata.real / numpy.iinfo(numpy.int32).max * (HEIGHT/2) +(HEIGHT/2)
        
        canvas = numpy.zeros((HEIGHT,WIDTH,3), dtype=numpy.uint8)
        
        # historgam
        fftHist[:,0:WIDTH-1] = fftHist[:,1:WIDTH]
        
        
        pop = (numpy.clip(numpy.abs(
            rfftdata.real[:HEIGHT]/
            # rfftdata.real[:HEIGHT].max()) * 5, 0, 1)
            10000000000) * 5, 0, 1)
            )*255
        
        fftHist[:,WIDTH-1] = cv2.applyColorMap(pop.astype(numpy.uint8), colormap=cv2.COLORMAP_OCEAN)[:,0]
        
        canvas[:] = fftHist[:]
        
        for i in range(len(fftdata)):
            cv2.circle(canvas, (i,int(fftdata.real[i])), 1, (255,255,255))
        draw()
except:
    print(traceback.format_exc()) 

stream.close()