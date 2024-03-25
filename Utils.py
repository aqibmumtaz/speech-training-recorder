import librosa
import numpy as np
import pickle
import json
import math
import os
from zipfile import ZipFile
from collections import Counter
import shutil
import nltk
from nltk.corpus import wordnet
from nltk.probability import FreqDist
import random
from nltk.corpus import wordnet
import csv


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

    def download_dataset():

        # Download the WordNet database if not already downloaded
        nltk.download("wordnet")

        # Load the dataset of medicine names
        medicine_names = nltk.corpus.names.words("medicine.txt")

        # Calculate the frequency distribution of the medicine names
        freq_dist = FreqDist(medicine_names)

        # Get the top 100 medicine names
        top_100_medicine_names = freq_dist.most_common(100)

        # Print the top 100 medicine names
        for medicine_name, frequency in top_100_medicine_names:
            print(medicine_name)

    # def generate_medicine_names():

    #     def generate_medicine_names_list(num_names):
    #         prefixes = [
    #             "Pro",
    #             "Zenith",
    #             "Medi",
    #             "Tranqui",
    #             "Cardio",
    #             "Dermacare",
    #             "Osteo",
    #             "Neuro",
    #             "Pulmo",
    #             "Gastro",
    #             "Aller",
    #             "Renova",
    #             "Diabeti",
    #             "Vision",
    #             "Musculo",
    #             "Immuno",
    #             "Pedia",
    #             "Asthma",
    #             "Cardio",
    #             "Pain",
    #         ]

    #         # Get synsets from WordNet for potential suffixes
    #         synsets = list(wordnet.all_synsets(pos=wordnet.NOUN))
    #         suffixes = [synset.lemmas()[0].name() for synset in synsets]

    #         medicine_names = []
    #         for _ in range(num_names):
    #             prefix = random.choice(prefixes)
    #             suffix = random.choice(suffixes).capitalize()
    #             name = f"{prefix}{suffix}"
    #             medicine_names.append(name)

    #         return medicine_names

    # # Generate a list of 10 medicine names
    # medicine_list = generate_medicine_names_list(10)

    # # Print the generated medicine names
    # for i, medicine in enumerate(medicine_list, start=1):
    #     print(f"{i}. {medicine}")

    def generate_medicine_names(
        filename="./datasets/Pakistan_Pharmaceutical_Products_Pricing_and_Availability_Data.csv",
    ):

        # Open the CSV file and read the data
        with open(filename, "r") as file:
            reader = csv.DictReader(file)
            data = list(reader)

            medicine_names = []
            for medicine in data:
                medicine_name = medicine["Name"]
                medicine_name = medicine_name.strip()
                if medicine_name != "":
                    medicine_name = medicine_name[0].upper() + medicine_name[1:]
                    medicine_names.append(medicine_name)

            medicine_names = Utils.unique(medicine_names)

            file = open("prompts/medicine_names.txt", "w")
            for medicine_names in medicine_names:
                file.write(medicine_names + "\n")
            file.close()


Utils.load_wav_file()
# Utils.download_dataset()
# Utils.generate_medicine_names()

# spectogram_librosa(_wav_file_)
# graph_wavfileread(_wav_file_)
# graph_spectrogram_wave(_wav_file_)


# Medicine

# commonly used medicines


# Diagontics

# tests
