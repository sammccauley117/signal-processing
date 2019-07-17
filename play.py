import argparse
import librosa
import time
import winsound

# Set up and parse command line arguments
parser = argparse.ArgumentParser(description='Play a .wav file')
parser.add_argument('filename', type=str, help='filename')
parser.add_argument('-s', '--source', type=str, default='./sounds/', help='The source folder (default: "./sounds/")')
args = parser.parse_args()

# Initialize variables
filename = args.filename
source = args.source
extension = '.wav'

# Check if the '.wav' extension was included in the filename
if filename.endswith('.wav'):
    extension = ''
path = source + filename + extension # Complete (relative) path to the file

# Calculate the duration (in seconds) of the file
samples, sr = librosa.load(path, sr=None) # Get the .wav file samples and sample rate
duration = len(samples) / sr

# Play the sound and exit
winsound.PlaySound(path, winsound.SND_ASYNC)
time.sleep(duration)
