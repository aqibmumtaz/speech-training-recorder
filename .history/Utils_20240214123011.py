import librosa
import numpy as np
import pickle
import json
import math
import os
from zipfile import ZipFile
from collections import Counter
import shutil


class Utils:

    is_vlc_started = False

    def load_save_dict(file_path, dict=None):

        if dict is None:
            # Read dictionary pkl file
            with open(file_path, "rb") as fp:
                dict = pickle.load(fp)
                print("dictionary loaded successfully from file")
                return dict
        else:
            # save dictionary to person_data.pkl file
            with open(file_path, "wb") as fp:
                pickle.dump(dict, fp)
                print("dictionary saved successfully to file")

    def unique(list):
        return sorted(Counter(list))

    def has_file_ext(file_name, ext="zip"):
        return file_name.endswith(ext)

    def zip_files(file_paths, zip_dest_path, append_name=""):
        zip_name = os.path.splitext(zip_dest_path)[0]
        list1 = zip_name.lower().split("_" + Configs.TRAINING_MODEL.lower())
        list2 = zip_name.lower().split("_v".lower())
        zip_dest_path = list1[0] + append_name + "_v" + list2[1] + ".zip"
        zip_name = zip_dest_path.split("/")[-1]

        with ZipFile(zip_dest_path, "w") as zip_object:
            # Adding files that need to be zipped
            for file_path in file_paths:
                zip_object.write(file_path)

        return zip_name, zip_dest_path

        # Check to see if the zip file is created
        if os.path.exists(zip_dest_path):
            print("ZIP file created")
        else:
            print("ZIP file not created")

    def unzip_files(zip_file_path, unzip_dest_path=None):
        zip_file_path = os.path.splitext(zip_file_path)[0] + ".zip"

        zfile = ZipFile(zip_file_path)
        zfile.extractall(unzip_dest_path)
        return zfile

    def ceil(number, digits) -> float:
        return math.ceil((10.0**digits) * number) / (10.0**digits)

    def get_area(x1, y1, x2, y2):
        return (x2 - x1) * (y2 - y1)

    def is_dir_empty(path):
        dir = os.listdir(path)

        # Checking if the list is empty or not
        if len(dir) == 0:
            return True
        else:
            return False

    def create_dir(path):
        if not Utils.is_path_exists(path):
            os.makedirs(str(path))

    def delete_dir(path):
        if Utils.is_path_exists(path):
            shutil.rmtree(path)

    def delete_file(path):
        try:
            if Utils.is_path_exists(path):
                os.remove(path)
        except Exception as e:
            print("imutil.delete_file : Error", e)

    def delete_all_files(path):
        if Utils.is_path_exists(path):
            for f in os.listdir(path):
                file_path = os.path.join(path, f)
                print("Deleting file", file_path)
                try:
                    if os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                    else:
                        os.remove(file_path)
                except Exception as e:
                    print(
                        "delete_all_files Error",
                        str(e.__class__) + str(e),
                        messageType=-1,
                    )

    def list_files_in_dir(path, dir_only=False, files_only=False):

        # if dir_only:
        #     files = [f for f in os.listdir(path)]
        # elif files_only:
        #     files = [f for f in os.listdir(path) if os.path.isfile(f)]
        # else:
        files = sorted(os.listdir(path))

        return files

    def is_path_exists(path):
        return os.path.exists(path)

    # write list to binary file
    def write_list_to_file(list, file_path):
        print("Started writing list data into a json file")
        with open(file_path, "w") as fp:
            json.dump(list, fp)
            print("Done writing JSON data into .json file")

    # Read list to memory
    def read_list_from_file(file_path):
        # for reading also binary mode is important
        with open(file_path, "rb") as fp:
            list = json.load(fp)
            return list

    def load_wav_file(_wav_file_="test.wav"):
        return librosa.load(_wav_file_, sr=None, mono=True, dtype=np.float32)

    def spectogram_librosa(_wav_file_="test.wav"):
        import pylab

        (sig, rate) = librosa.load(_wav_file_, sr=None, mono=True, dtype=np.float32)
        pylab.specgram(sig, Fs=rate)
        pylab.savefig("./output/spectrogram3.png")

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


Utils.load_wav_file()

# spectogram_librosa(_wav_file_)
# graph_wavfileread(_wav_file_)
# graph_spectrogram_wave(_wav_file_)
