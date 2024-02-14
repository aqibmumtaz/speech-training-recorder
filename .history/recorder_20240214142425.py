#!/usr/bin/env python3

import argparse, datetime, logging, math, os, os.path, random, re, sys

import struct
import numpy as np
from scipy.ndimage import binary_dilation
import webrtcvad
import soundfile

from Utils import *

try:
    import winsound
except Exception as e:
    logging.warning("sound output only supported on Windows")

from PySide2.QtGui import QGuiApplication, QFontDatabase
from PySide2.QtQml import QQmlApplicationEngine, qmlRegisterType
from PySide2.QtCore import Qt, QUrl, QObject, Property, Signal, Slot

import audio

# For silence trimming
vad_moving_average_width = 8
int16_max = (2**15) - 1
vad_window_length = 30
sample_rate = 16000
vad_max_silence_length = 6


# Source: CorentinJ - Real Time Voice Cloning - Thanks for this one!
def trim_long_silences(wav):

    # Compute the voice detection window size
    samples_per_window = (vad_window_length * sample_rate) // 1000

    # Trim the end of the audio to have a multiple of the window size
    wav = wav[: len(wav) - (len(wav) % samples_per_window)]

    # Convert the float waveform to 16-bit mono PCM
    pcm_wave = struct.pack(
        "%dh" % len(wav), *(np.round(wav * int16_max)).astype(np.int16)
    )

    # Perform voice activation detection
    voice_flags = []
    vad = webrtcvad.Vad(mode=3)
    for window_start in range(0, len(wav), samples_per_window):
        window_end = window_start + samples_per_window
        voice_flags.append(
            vad.is_speech(
                pcm_wave[window_start * 2 : window_end * 2], sample_rate=sample_rate
            )
        )
    voice_flags = np.array(voice_flags)

    # Smooth the voice detection with a moving average
    def moving_average(array, width):
        array_padded = np.concatenate(
            (np.zeros((width - 1) // 2), array, np.zeros(width // 2))
        )
        ret = np.cumsum(array_padded, dtype=float)
        ret[width:] = ret[width:] - ret[:-width]
        return ret[width - 1 :] / width

    audio_mask = moving_average(voice_flags, vad_moving_average_width)
    audio_mask = np.round(audio_mask).astype(np.bool)

    # Dilate the voiced regions
    audio_mask = binary_dilation(audio_mask, np.ones(vad_max_silence_length + 1))
    audio_mask = np.repeat(audio_mask, samples_per_window)

    return wav[audio_mask == True]


class Recorder(QObject):
    """docstring for Recorder"""

    def __init__(
        self,
        save_dir,
        prompts_filename,
        ordered=False,
        prompts_count=100,
        prompt_len_soft_max=None,
    ):
        super(Recorder, self).__init__()
        if not os.path.isdir(save_dir):
            raise Exception("save_dir '%s' is not a directory" % save_dir)
        self.save_dir = save_dir
        if not os.path.isfile(prompts_filename):
            raise Exception("prompts_filename '%s' is not a file" % prompts_filename)
        self.prompts_filename = prompts_filename
        self.prompts_count = prompts_count
        self.prompt_len_soft_max = prompt_len_soft_max
        self.ordered = ordered
        self.audio = audio.Audio()

    @Slot(QObject)
    def init(self, scriptModel):
        logging.debug("init: %s", scriptModel)
        self.window.setProperty("saveDir", self.save_dir)
        self.scriptModel = scriptModel
        self.window.setProperty(
            "promptsName", os.path.splitext(os.path.basename(self.prompts_filename))[0]
        )
        for script in self.get_scripts_from_file(
            self.prompts_count,
            self.prompts_filename,
            self.ordered,
            split_len=self.prompt_len_soft_max,
        ):
            self.window.appendScript({"script": script, "filename": ""})

    @Slot(bool)
    def toggleRecording(self, recording):
        logging.debug("toggleRecording: recording is now %s", recording)

    @Slot()
    def startRecording(self):
        size = self.flush()
        logging.debug("flushed %s", size)
        self.audio.stream.start_stream()

    @Slot()
    def finishRecording(self):
        self.audio.stream.stop_stream()
        data = self.read_audio(drop_last=3)
        if self.window.property("scriptFilename"):
            self.deleteFile(self.window.property("scriptFilename"))

        _filename = "recorder_" + datetime.datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S_%f"
        )
        prompt_name = (self.prompts_filename.split("/")[1]).split(".")[0]
        dirname = os.path.normpath(
            os.path.join(self.window.property("saveDir"), prompt_name)
        )
        Utils.create_dir(dirname)

        filename = os.path.normpath(
            os.path.join(
                dirname,
                _filename + ".wav",
            )
        )

        self.window.setProperty("scriptFilename", filename)
        self.audio.write_wav(filename, data)
        scriptText = self.window.property("scriptText")
        with open(
            os.path.join(self.window.property("saveDir"), "recorder.tsv"), "a"
        ) as xsvfile:
            xsvfile.write(
                "\t".join(
                    [
                        filename,
                        "0",
                        self.window.property("promptsName"),
                        "",
                        self.sanitize_script(scriptText),
                    ]
                )
                + "\n"
            )
        with open(os.path.join(dirname, "recorder.tsv"), "a") as xsvfile:
            xsvfile.write(
                "\t".join(
                    [
                        filename,
                        "0",
                        self.window.property("promptsName"),
                        "",
                        self.sanitize_script(scriptText),
                    ]
                )
                + "\n"
            )
        logging.debug("wrote %s to %s", len(data), filename)

        trimmed_filename = os.path.normpath(
            os.path.join(
                self.window.property("saveDir"),
                _filename + "_trimmed" + ".wav",
            )
        )

        # trim silence?
        try:
            wav, source_sr = Utils.load_wav_file(_wav_file_=filename)
            wav = trim_long_silences(wav)
            soundfile.write(str(filename), wav, source_sr)
        except Exception as e:
            print(f"Error : {e}")

    @Slot(str)
    def playFile(self, filename):
        winsound.PlaySound(filename, winsound.SND_FILENAME)

    @Slot(str)
    def deleteFile(self, filename):
        os.remove(filename)
        xsvfile_in_path = os.path.join(self.window.property("saveDir"), "recorder.tsv")
        xsvfile_out_path = os.path.join(
            self.window.property("saveDir"), "recorder_delete_temp.tsv"
        )
        with open(xsvfile_in_path, "r") as xsvfile_in:
            with open(xsvfile_out_path, "w") as xsvfile_out:
                for line in xsvfile_in:
                    if filename not in line:
                        xsvfile_out.write(line)
        os.replace(xsvfile_out_path, xsvfile_in_path)
        self.window.setProperty("scriptFilename", "")

    def read_audio(self, drop_last=None):
        blocks = []
        while not self.audio.buffer_queue.empty():
            block = self.audio.buffer_queue.get_nowait()
            # logging.debug('read %s', len(block) if block else None)
            if block:
                blocks.append(block)
        # logging.debug('read total %s', len(b''.join(blocks)))
        if drop_last:
            blocks = blocks[:-drop_last]
        return b"".join(blocks)

    def flush(self):
        size = self.audio.buffer_queue.qsize()
        while not self.audio.buffer_queue.empty():
            self.audio.buffer_queue.get_nowait()
        return size

    def get_scripts_from_file(self, n, filename, ordered=False, split_len=None):
        def filter(script):
            # match = re.fullmatch(r'\w+ "(.*)"', script)
            patterns = [
                r'^\w+ "(.*)"$',  # arctic
                r"^(.*) \(s.\d+\)$",  # timit
            ]
            for pat in patterns:
                script = re.sub(pat, r"\1", script, count=1)
            return script

        with open(filename, "r") as file:
            scripts = [line.strip() for line in file if not line.startswith(";")]
        if n is None:
            n = len(scripts)
        if not ordered:
            # random.shuffle(scripts)
            scripts = [random.choice(scripts) for _ in range(n)]
        scripts = scripts[:n]
        scripts = [filter(script) for script in scripts]
        if split_len is not None:
            scripts = [self.split_script(script, split_len) for script in scripts]
            scripts = sum(scripts, [])
        return scripts[:n]

    @classmethod
    def sanitize_script(cls, script):
        return script.strip()
        script = re.sub(r"[\-]", " ", script)
        script = re.sub(r'[,.?!:;"]', "", script)

    @classmethod
    def split_script(cls, script, split_len):
        scripts = []
        n = math.ceil(len(script) / split_len)
        startpos = 0
        # print(script)
        regex = re.compile(r"\s+")
        for i in range(n):
            match = regex.search(script, pos=startpos + split_len)
            endpos = match.start() if match else None
            scripts.append(script[startpos:endpos].strip())
            # print(startpos, endpos, scripts)
            if endpos is None:
                break
            startpos = endpos
        return scripts


def main():
    current_path = os.path.abspath(os.path.dirname(__file__))
    qml_file = os.path.join(current_path, os.path.splitext(__file__)[0] + ".qml")

    parser = argparse.ArgumentParser(
        description="""
        Given a text file containing prompts, this app will choose a random selection
        and ordering of them, display them to be dictated by the user, and record the
        dictation audio and metadata to a `.wav` file and `recorder.tsv` file
        respectively.
    """
    )
    parser.add_argument(
        "-p", "--prompts_filename", help="file containing prompts to choose from"
    )
    parser.add_argument(
        "-d",
        "--save_dir",
        default="./output",
        help="where to save .wav & recorder.tsv files (default: %(default)s)",
    )
    parser.add_argument(
        "-c",
        "--prompts_count",
        type=int,
        default=100,
        help="number of prompts to select and display (default: %(default)s)",
    )
    parser.add_argument("-l", "--prompt_len_soft_max", type=int)
    parser.add_argument(
        "-o",
        "--ordered",
        action="store_true",
        default=False,
        help="present prompts in order, as opposed to random (default: %(default)s)",
    )
    args = parser.parse_args()
    assert args.prompts_filename

    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    engine.addImportPath(current_path)
    kwargs = {
        k: v
        for k, v in vars(args).items()
        if v is not None and k in "prompts_count prompt_len_soft_max".split()
    }
    recorder = Recorder(args.save_dir, args.prompts_filename, args.ordered, **kwargs)
    engine.rootContext().setContextProperty("recorder", recorder)
    engine.load(qml_file)
    recorder.window = engine.rootObjects()[0]

    res = app.exec_()
    sys.exit(res)


if __name__ == "__main__":
    logging.basicConfig(level=10)
    main()
