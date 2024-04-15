# speech-training-recorder

> Simple GUI application to help record audio dictated from given text
prompts, for use with training speech recognition or speech synthesis.

Given a text file containing prompts, this app will choose a random selection
and ordering of them, display them to be dictated by the user, and record the
dictation audio and metadata to a `.wav` file and `recorder.tsv` file
respectively. You can select a previous recording to play it back, delete it,
and/or re-record it.

![Screenshot](.github/screenshot.png)

**Requirements:**

* Python 3
* See [`requirements.txt`](requirements.txt) for required packages
* Cross platform: Windows, Linux, MacOS

## Getting Started

```
git clone https://github.com/daanzu/speech-training-recorder.git
cd speech-training-recorder
mkdir ../audio_data
pip install -r requirements.txt
python3 recorder.py -p prompts/timit.txt
```

```
usage: recorder.py [-h] [-p PROMPTS_FILENAME] [-d SAVE_DIR] [-c PROMPTS_COUNT]
                   [-l PROMPT_LEN_SOFT_MAX] [-o]

Given a text file containing prompts, this app will choose a random selection
and ordering of them, display them to be dictated by the user, and record the
dictation audio and metadata to a `.wav` file and `recorder.tsv` file
respectively.

optional arguments:
  -h, --help            show this help message and exit
  -p PROMPTS_FILENAME, --prompts_filename PROMPTS_FILENAME
                        file containing prompts to choose from
  -d SAVE_DIR, --save_dir SAVE_DIR
                        where to save .wav & recorder.tsv files (default:
                        ../audio_data)
  -c PROMPTS_COUNT, --prompts_count PROMPTS_COUNT
                        number of prompts to select and display (default: 100)
  -l PROMPT_LEN_SOFT_MAX, --prompt_len_soft_max PROMPT_LEN_SOFT_MAX
  -o, --ordered         present prompts in order, as opposed to random
                        (default: False)
```

## Customization

See `prompts/` directory for acceptable formats for prompt files: the simplest is `rainbow_passage.txt`.

## Related Repositories

* [daanzu/kaldi_ag_training](https://github.com/daanzu/kaldi_ag_training): Docker image and scripts for training finetuned or completely personal Kaldi speech models. Particularly for use with [kaldi-active-grammar](https://github.com/daanzu/kaldi-active-grammar).


## How to run

  * Recording View : `python recorder.py -p prompts/commands.txt`
  * Recording View n samples per prompt : `python recorder.py -p prompts/commands.txt -n 5`  
  * Recording View with Relaod : `python recorder.py -p prompts/commands.txt -r True -n 5`
  * Validation View : `python recorder.py -p prompts/commands.txt -v True`


### Datasets
  * A-Z Medicine Datasets : 
                            https://www.quora.com/Where-can-I-get-a-dataset-of-all-the-medicine-name-and-its-use
                            https://www.kaggle.com/datasets/talhasattar727/pakistan-pharmaceutical-dataset
                            https://www.kaggle.com/datasets/shudhanshusingh/az-medicine-dataset-of-india/code
                            https://www.kaggle.com/code/muhammedtausif/medicine-analytics-eda
                            https://www.kaggle.com/datasets/ahmedshahriarsakib/assorted-medicine-dataset-of-bangladesh


  * Speech Dataset for healthcare:
                            https://www.shaip.com/healthcare-ai/physician-dictation-audio-data-medical-data-catalog/
                            Medical Speech, Transcription, and Intent : https://www.kaggle.com/datasets/paultimothymooney/medical-speech-transcription-and-intent
                            https://zenodo.org/records/4279041


  * Speech Dataset general:
                            https://paperswithcode.com/datasets?task=speech-recognition


  * Audio Datasets :
                            https://paperswithcode.com/datasets?task=audio-classification

  * Pronunciation :
                            https://www.oed.com/dictionary/amoxicillin_n


  * Local Accent Datasets : 
                            indian - https://huggingface.co/datasets/DTU54DL/common-accent
                            indian - https://www.kaggle.com/datasets/polly42rose/indian-accent-dataset
                            indian - https://www.datatang.ai/datasets/940
                            indian - https://github.com/AI4Bharat/NPTEL2020-Indian-English-Speech-Dataset?tab=readme-ov-file
                            High-quality Audio / Speech / Voice Datasets to Train Your Conversational AI Model : https://www.shaip.com/offerings/speech-data-catalog/
                            All Accents - https://www.kaggle.com/datasets/rtatman/speech-accent-archive
                            Urdu (Pakistan) Call Center Speech Dataset for Healthcare - https://www.futurebeeai.com/dataset/speech-dataset/healthcare-call-center-conversation-urdu-pakistan


  * Tools 
                            Text to Speech :
                            Voice cloning / pakistani-accent : https://elevenlabs.io/languages/pakistani-accent
                            https://revoicer.com/
                            https://freetools.textmagic.com/text-to-speech

