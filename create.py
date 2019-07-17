import argparse, struct
import numpy as np
import wave

def parse_frequency(s):
    '''
    Description: takes a string of frequencies and returns a list of integers of the frequencies.
    Example:
        input:  '100'
        output: [100]

        input:  '[100, 150, 200]'
        output: [100, 150, 200]
    Returns: list of integers of each frequency to be present in the output waveform
    '''
    s = s.replace('[','')
    s = s.replace(']','')
    return [int(f) for f in s.split(',')]

# Set up and parse command line arguments
parser = argparse.ArgumentParser(description='Create an .wav file of sinusoid(s)')
parser.add_argument('frequency', type=str, help='Either a single frequency or a list of frequencies present in the waveform')
parser.add_argument('duration', type=float, help='Length of the waveform in seconds')
parser.add_argument('-f', '--filename', type=str, default='output.wav', help='The filename of the output signal (default: "output.wav")')
parser.add_argument('-s', '--source', type=str, default='./sounds/', help='The source folder (default: "./sounds/")')
args = parser.parse_args()

# Initialize variables
frequencies = parse_frequency(args.frequency) # List of frequencies to be present in output
duration = args.duration # Length of waveform in seconds
sr = 48000 # Sample rate in Hz
A = 4000 # Amplitude
num_samples = int(sr*duration) # Total number of samples that will be in the signal
signal = np.zeros(num_samples) # Output signal
source = args.source # Source file
filename = args.filename # Name of the output audio file
extension = '.wav'

# Check if the '.wav' extension was included in the filename
if filename.endswith('.wav'):
    extension = ''
path = source + filename + extension # Complete (relative) path to the file

# Add each frequency component to the output signal
for frequency in frequencies:
    signal += [A*np.sin(2*np.pi*frequency*x/sr) for x in range(num_samples)]

# Configure wave library
compression_type = "NONE" # We don't want to compress the data at all
compression ="not compressed" # Don't compress the data
num_channels = 1 # Mono audio
sample_width = 2 # Writing as 16b audio, thus our width is 2 Bytes
file = wave.open(path, 'w') # Open the desired file
file.setparams((num_channels, sample_width, int(sr), num_samples, compression_type, compression))

# Write each sample to the .wav file
for sample in signal:
    file.writeframes(struct.pack('h',int(sample))) # Pack the data into 16b
