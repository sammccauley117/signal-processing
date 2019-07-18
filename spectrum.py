import time, uuid, argparse, os
import librosa
import numpy as np
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from moviepy.editor import *

# Set up and parse command line arguments
parser = argparse.ArgumentParser(description='Create a video of a .wav file\'s audio spectrum')
parser.add_argument('filename', type=str, help='filename')
parser.add_argument('-s', '--source', type=str, default='./sounds/', help='The source folder (default: "./sounds/")')
parser.add_argument('-d', '--destination', type=str, default='./videos/', help='The destination folder (default: "./videos/")')
parser.add_argument('-o', '--output', type=str, default='spectrum.mp4', help='The output file (default: "spectrum.mp4")')
parser.add_argument('-l', '--limit', help='Frequency limits. Example: (20, 1000)')
args = parser.parse_args()

# Determine source and destination path
if args.filename.endswith('.wav'):
    source_path = args.source + args.filename
else:
    source_path = args.source + args.filename + '.wav'
if args.output.endswith('.mp4'):
    dest_path = args.destination + args.output
else:
    dest_path = args.destination + args.output + '.mp4'

# Setup variables for calculating each Short Time Fourier Transform (STFT)
window = 50 / 1000 # Size of the STFT in seconds
samples, sr = librosa.load(source_path, sr=None)
duration = len(samples) / sr # Total duration of the .wav file in seconds
num_frames = int(duration / window) # Number of STFTs to take
samples_per_frame = int(window * sr) # How many samples are in each STFT
frames = np.zeros(shape=(num_frames, samples_per_frame//2)) # Array of each STFT
x = np.linspace(0, sr//2, samples_per_frame//2, dtype='int16') # X-axis of the plot

# Execute calculation of each STFT frame
for i in range(num_frames):
    frame_samples = samples[samples_per_frame*i:samples_per_frame*(i+1)]
    fft = np.fft.fft(frame_samples)
    fft = np.absolute(fft)
    fft = fft[:len(fft)//2] # We only want the first half of the fft because the second half is just a mirror
    frames[i] = fft

def parse_limit(s):
    if not s[0].isdigit(): s = s[1:]
    if not s[-1].isdigit(): s = s[:-1]
    s = s.split(',')
    if len(s) > 1:
        return (int(s[0]), int(s[1]))
    if len(s) == 1:
        return (0, int(s[0]))
    return (0, sr // 2)

def get_frame(i):
    '''
    Plots each frame of the animation where `i` is the index of the frame
    '''
    plt.cla()
    plt.xlabel('Frequency')
    plt.ylabel('Amplitude')
    plt.ylim((0, max_value))
    if args.limit:
        plt.xlim(parse_limit(args.limit))
    plt.plot(x, frames[i])

# Create and save the animation
fig = plt.figure()
max_value = np.amax(frames) # For the ylim so that the plot doesn't bounce around
animation = animation.FuncAnimation(fig, get_frame, num_frames)
temp_filename = args.destination + str(uuid.uuid4()) + '.mp4'
animation.save(temp_filename, fps=1/window)

# Add the original audio to the .mp4 file
videoclip = VideoFileClip(temp_filename)
audioclip = AudioFileClip(source_path)
new_audioclip = CompositeAudioClip([audioclip])
videoclip.audio = new_audioclip
videoclip.write_videofile(dest_path)
os.remove(temp_filename)

# print('filename:', filename)
# print('Number of samples:', len(samples))
# print('Sample Rate:', sr)
# print('Duration:', duration)
# print('Number of FTs:', num_frames)
# print('Samples per frame:', samples_per_frame)
# print('Length of frames:', len(frames))
# print(samples)
