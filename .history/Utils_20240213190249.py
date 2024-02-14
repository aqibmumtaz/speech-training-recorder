_wav_file_ = "output/recorder_2024-02-13_18-58-48_526342.wav"


def spectogram_librosa(_wav_file_):
    import librosa
    import pylab
    import numpy as np

    (sig, rate) = librosa.load(_wav_file_, sr=None, mono=True, dtype=np.float32)
    pylab.specgram(sig, Fs=rate)
    pylab.savefig("spectrogram3.png")


def graph_spectrogram_wave(wav_file):
    import wave
    import pylab

    def get_wav_info(wav_file):
        wav = wave.open(wav_file, "r")
        frames = wav.readframes(-1)
        sound_info = pylab.fromstring(frames, "int16")
        frame_rate = wav.getframerate()
        wav.close()
        return sound_info, frame_rate

    sound_info, frame_rate = get_wav_info(wav_file)
    pylab.figure(num=3, figsize=(10, 6))
    pylab.title("spectrogram pylab with wav_file")
    pylab.specgram(sound_info, Fs=frame_rate)
    pylab.savefig("spectrogram2.png")


def graph_wavfileread(_wav_file_):
    import matplotlib.pyplot as plt
    from scipy import signal
    from scipy.io import wavfile
    import numpy as np

    sample_rate, samples = wavfile.read(_wav_file_)
    frequencies, times, spectrogram = signal.spectrogram(
        samples, sample_rate, nfft=1024
    )
    plt.pcolormesh(times, frequencies, 10 * np.log10(spectrogram))
    plt.ylabel("Frequency [Hz]")
    plt.xlabel("Time [sec]")
    plt.savefig("spectogram1.png")


spectogram_librosa(_wav_file_)
# graph_wavfileread(_wav_file_)
# graph_spectrogram_wave(_wav_file_)
