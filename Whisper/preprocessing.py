import os
from datasets import DatasetDict, Audio
from datasets import Dataset
from transformers import WhisperFeatureExtractor
from transformers import WhisperTokenizer
from pydub import AudioSegment
import pandas as pd

model = "tiny"
feature_extractor = WhisperFeatureExtractor.from_pretrained(f'openai/whisper-{model}')
tokenizer = WhisperTokenizer.from_pretrained(f'openai/whisper-{model}', language="French", task="transcribe")


def txt_test_timestamps(list_cuts):
    transcription = "" # f"<Sync time=\"{start_sync_time}\"/>\n"
    for cut_index in range(len(list_cuts)):
        if '<Sync' in list_cuts[cut_index]:
            if cut_index+1 < len(list_cuts) and '<Sync' in list_cuts[cut_index+1]:
                transcription = transcription + "\n" + list_cuts[cut_index] + "\n"
            elif cut_index+1 == len(list_cuts) and '<Sync' in list_cuts[cut_index]:
                transcription = transcription + "\n" + list_cuts[cut_index]
            else:
                transcription = transcription + list_cuts[cut_index] + "\n"
        else:
            transcription = transcription + " " + list_cuts[cut_index]
    return transcription


def save(output_dir, last_test_sample_index, transcription_sample, audio_sample):
    text_file = open(
        f'{output_dir}transcription/{last_test_sample_index}.txt',
        "w", encoding='utf-8')
    text_file.write(transcription_sample)
    text_file.close()
    audio_sample.export(f'{output_dir}audio/{last_test_sample_index}.mp3', format="mp3", codec="libmp3lame")
    audio_sample.export(f'{output_dir}audio wav/{last_test_sample_index}.wav', format="wav")



def find_next_timestamp_line(start_line, transcription):
    line = start_line
    while line < len(transcription):
        if transcription[line][0:5] == '<Sync':
            return line
        line += 1
    return 100000000000


def get_next_sample(start_line, transcription, current_sync_time):
    start_sync_time = float(transcription[start_line].split("\"")[1])
    last_line = start_line
    for line_index in range(start_line, len(transcription)-2):
        if transcription[line_index][0:5] == '<Sync' and line_index+1 < len(transcription):
            if transcription[line_index + 1][0:5] != '<Sync':
                current_line = find_next_timestamp_line(line_index + 2, transcription)
                current_sync_time = float(transcription[current_line].split("\"")[1])
                if current_sync_time - start_sync_time < 30:
                    last_line = current_line
                else:
                    return last_line
    return start_line + 1


def build_30s_samples():
    root = "dataset/raw data/"
    audio_files = ["France_Argentine_Intro_FR.wav", "2007-09-12_Japon-Fidji.mp3", "2015-10-01_France-Canada.wav",
                   "2015-10-17_NouvelleZelande-France.wav", "2015-10-30_AfriqueDuSud-Argentine.mp3"]
    txt_files = ["France_Argentine_Intro_FR.txt", "2007-09-12_Japon-Fidji.txt", "2015-10-01_France-Canada.txt",
                 "2015-10-17_NouvelleZelande-France.txt", "AfriqueDuSud-Argentine_CF.txt"]
    last_training_sample_index = 0
    last_validation_sample_index = 0
    last_test_sample_index = 0
    starts = []
    ends = []
    file_name = []
    transcriptions = []
    transcription_with_timestamps = []
    dataset_part = []
    dataset_id = []
    for file_index in range(len(audio_files)):
        sound = AudioSegment.from_file(f'{root}{audio_files[file_index]}')
        transcription_tailing_space = open(f'{root}{txt_files[file_index]}', "r", encoding='utf-8')
        transcription = [line.rstrip() for line in transcription_tailing_space]
        start_line = 0
        last_line = 0
        while last_line < len(transcription) and start_line < len(transcription):
            if transcription[start_line][0:5] == '<Sync':
                start_sync_time = float(transcription[start_line].split("\"")[1])
                last_line = get_next_sample(start_line, transcription, start_sync_time)
                if last_line > start_line+1:
                    end_sync_time = float(transcription[last_line].split("\"")[1])
                    transcription_sample = " ".join([x for x in transcription[start_line:last_line] if x[0:5] != '<Sync'])
                    audio_sample = sound[start_sync_time * 1000:end_sync_time * 1000]

                    print(end_sync_time - start_sync_time, last_training_sample_index, last_validation_sample_index,
                          last_test_sample_index)
                    if audio_files[file_index] == "2015-10-17_NouvelleZelande-France.wav" or audio_files[file_index] == "France_Argentine_Intro_FR.wav":
                        if end_sync_time < 900:
                            save('C:/Users/Cam/PycharmProjects/whisper/dataset/30s samples/test/',
                                 last_test_sample_index, transcription_sample, audio_sample)
                            starts.append(start_sync_time)
                            ends.append(end_sync_time)
                            file_name.append(audio_files[file_index])
                            transcriptions.append(transcription_sample)
                            dataset_id.append(last_test_sample_index)
                            dataset_part.append("test")
                            last_test_sample_index += 1
                        elif (last_training_sample_index + last_validation_sample_index + last_test_sample_index) % 6 == 0:
                            save('C:/Users/Cam/PycharmProjects/whisper/dataset/30s samples/validation/',
                                 last_validation_sample_index, transcription_sample, audio_sample)
                            starts.append(start_sync_time)
                            ends.append(end_sync_time)
                            file_name.append(audio_files[file_index])
                            transcriptions.append(transcription_sample)
                            dataset_id.append(last_validation_sample_index)
                            dataset_part.append("validation")
                            last_validation_sample_index += 1
                        else:

                            # transcription with all timestamps for testing of the whisper_timestamped library
                            list_transcription_timestamps = [x for x in transcription[start_line+1:last_line + 1]]
                            transcription_sample_timestamps = txt_test_timestamps(list_transcription_timestamps)
                            transcription_with_timestamps.append(transcription_sample_timestamps)

                            text_file_timestamps = open(
                                f'C:/Users/Cam/PycharmProjects/whisper/timestamps testing/timestamps labels/{last_training_sample_index}.txt',
                                "w", encoding='utf-8')
                            text_file_timestamps.write(transcription_sample_timestamps)
                            text_file_timestamps.close()

                            # can be deleted until this line of code

                            save('C:/Users/Cam/PycharmProjects/whisper/dataset/30s samples/training/',
                                 last_training_sample_index, transcription_sample, audio_sample)
                            starts.append(start_sync_time)
                            ends.append(end_sync_time)
                            file_name.append(audio_files[file_index])
                            transcriptions.append(transcription_sample)
                            dataset_id.append(last_training_sample_index)
                            dataset_part.append("training")
                            last_training_sample_index += 1
                    elif (last_training_sample_index + last_validation_sample_index + last_test_sample_index) % 6 == 0:
                        save('C:/Users/Cam/PycharmProjects/whisper/dataset/30s samples/validation/',
                             last_validation_sample_index, transcription_sample, audio_sample)
                        starts.append(start_sync_time)
                        ends.append(end_sync_time)
                        file_name.append(audio_files[file_index])
                        transcriptions.append(transcription_sample)
                        dataset_id.append(last_validation_sample_index)
                        dataset_part.append("validation")
                        last_validation_sample_index += 1
                    else:

                        # transcription with all timestamps for testing of the whisper_timestamped library
                        list_transcription_timestamps = [x for x in transcription[start_line+1:last_line + 1]]
                        transcription_sample_timestamps = txt_test_timestamps(list_transcription_timestamps)
                        transcription_with_timestamps.append(transcription_sample_timestamps)

                        text_file_timestamps = open(
                            f'C:/Users/Cam/PycharmProjects/whisper/timestamps testing/timestamps labels/{last_training_sample_index}.txt',
                            "w", encoding='utf-8')
                        text_file_timestamps.write(transcription_sample_timestamps)
                        text_file_timestamps.close()

                        # can be deleted until this line of code

                        save('C:/Users/Cam/PycharmProjects/whisper/dataset/30s samples/training/',
                             last_training_sample_index, transcription_sample, audio_sample)
                        starts.append(start_sync_time)
                        ends.append(end_sync_time)
                        file_name.append(audio_files[file_index])
                        transcriptions.append(transcription_sample)
                        dataset_id.append(last_training_sample_index)
                        dataset_part.append("training")
                        last_training_sample_index += 1
                start_line = last_line if last_line > start_line else start_line + 1
                print(start_sync_time)
            else:
                print("error")
                start_line += 1

    df = pd.DataFrame(data={"start": starts, "end": ends, "id": dataset_id, "dataset": dataset_part,
                            "file": file_name, "label": transcriptions, "timestamp labels": transcription_with_timestamps})
    df.to_csv("dataset_info.csv")


def build_dataset():
    dir_path = "C:/Users/Cam/PycharmProjects/whisper/dataset/30s samples/training/"
    nb_samples = len([entry for entry in os.listdir(f'{dir_path}transcription') if
                      os.path.isfile(os.path.join(f'{dir_path}transcription', entry))])
    dataset = DatasetDict()

    audio_files = []
    transcription_files = []

    for index_sample in range(nb_samples):
        audio_files.append(f'{dir_path}audio/{index_sample}.mp3')
        f = open(f'{dir_path}transcription/{index_sample}.txt', "r", encoding='utf-8')
        transcription_files.append(f.read())

    dataset["train"] = Dataset.from_dict({"audio": audio_files,
                                          "transcription": transcription_files}).cast_column("audio", Audio(
        sampling_rate=16000))

    dir_path = "C:/Users/Cam/PycharmProjects/whisper/dataset/30s samples/validation/"
    nb_samples = len([entry for entry in os.listdir(f'{dir_path}transcription') if
                      os.path.isfile(os.path.join(f'{dir_path}transcription', entry))])
    audio_files = []
    transcription_files = []

    for index_sample in range(28, nb_samples):
        audio_files.append(f'{dir_path}audio/{index_sample}.mp3')
        f = open(f'{dir_path}transcription/{index_sample}.txt', "r", encoding='utf-8')
        transcription_files.append(f.read())

    dataset["validation"] = Dataset.from_dict({"audio": audio_files,
                                               "transcription": transcription_files}).cast_column("audio", Audio(
        sampling_rate=16000))

    return dataset


def prepare_dataset(batch):
    # load and resample audio data from 48 to 16kHz
    audio = batch["audio"]

    # compute log-Mel input features from input audio array
    batch["input_features"] = feature_extractor(audio["array"], sampling_rate=audio["sampling_rate"]).input_features[0]

    # encode target text to label ids
    batch["labels"] = tokenizer(batch["transcription"]).input_ids
    return batch
