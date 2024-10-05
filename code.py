import numpy as np
from scipy.signal import butter, lfilter

# Band-pass filter to remove high-frequency noise
def butter_bandpass(lowcut, highcut, fs, order=5):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return b, a

def bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

# Function to calculate the signal-to-noise ratio (SNR)
def calculate_snr(signal, noise_level=1e-5):
    signal_power = np.sum(signal ** 2)
    noise_power = noise_level ** 2 * len(signal)
    return 10 * np.log10(signal_power / noise_power)

# Example seismic data (this should be replaced with real seismic data from Apollo or InSight)
seismic_data = np.random.randn(10000)  # Simulated data, replace with actual data

# Apply bandpass filter to remove noise (frequencies between 0.1 Hz and 10 Hz)
filtered_data = bandpass_filter(seismic_data, lowcut=0.1, highcut=10.0, fs=100)

# Sliding window approach to analyze seismic data
window_size = 1000  # Window size in samples (e.g., 10-second window at 100 Hz)
snr_threshold = 5  # Threshold to detect an event
events = []

for start in range(0, len(filtered_data) - window_size, window_size):
    window = filtered_data[start:start + window_size]
    snr = calculate_snr(window)
   
    if snr > snr_threshold:
        print(f"Seismic event detected at sample {start} with SNR: {snr}")
        events.append((start, start + window_size))  # Store the event start and end indices

# Output the seismic events
if events:
    print("Seismic events detected:", events)
else:
    print("No seismic events detected.")
