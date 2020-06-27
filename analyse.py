import scipy.io.wavfile
import pydub
import sys
import numpy as np
#from numpy import fft as fft
import scipy.fftpack
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy import signal

if len(sys.argv)>1:
    fname = sys.argv[1]
else:
    print("Need file name")
    quit()


#read wav file
rate,audData=scipy.io.wavfile.read(fname)
print("Sample rate is {0}".format(rate))

#Take the rate, multiply by 8 to get how many samples
#Check shape[0] is larger.

if (audData.shape[0]<rate*8):
    print("Sample is too short to analyze!")
    quit()

#Crop to 8 seconds
audData = audData[:(rate*8)]

#Remove the DC offset
audData = signal.detrend(audData)

#create a time variable in seconds
time = np.arange(0, float(audData.shape[0]), 1) / rate

#Create the plot object
fs=(12,9)
fig = plt.figure(figsize=fs)
plt.rc('figure', titlesize=20)  # fontsize of the figure title
fig.suptitle("Sample rate {0}kHz".format(int(rate/1000)))

#plot amplitude (or loudness) over time
amp_plot = fig.add_subplot(211)
amp_plot.plot(time[::100], audData[::100], linewidth=0.5, alpha=1, color='#000000')
amp_plot.set_ylim([-65000000,65000000])
amp_plot.set_xlabel('Time (s)')
amp_plot.set_ylabel('Amplitude')




# Handle the FFT here
fft_plot = fig.add_subplot(212)
fourier = scipy.fftpack.fft(audData)
# Sample spacing is 1/rate
Tspace = 1.0 / rate
#Number of samples
Nsamp = audData.shape[0]
xf = np.linspace(0.0, 1.0/(2.0*Tspace), int(Nsamp/2))

fft_plot.plot(xf, 2.0/Nsamp * np.abs(audData[0:int(Nsamp/2)]), linewidth = 0.5, color='#ff7f00')
fft_plot.set_ylim([0,100])
fft_plot.set_xlabel('Frequency (Hz)')
fft_plot.set_ylabel('Amplitude')

#fig.tight_layout(pad=0.1)

margins = {
    "left": 0.05,
    "bottom": 0.06,
    "right" : 0.99,
    "top" : 0.95,
    "hspace" : 0.15
}
fig.subplots_adjust(**margins)

fig.savefig('amp+fft_{0}kHz.png'.format(int(rate/1000)))
#plt.show()

