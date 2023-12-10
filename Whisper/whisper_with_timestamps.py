import os
import numpy
import pandas as pd
from transformers import WhisperForConditionalGeneration, WhisperTokenizer, WhisperProcessor
from data_collector import DataCollatorSpeechSeq2SeqWithPadding
import torch
import whisper_timestamped
import evaluate

def save_timestamps_to_txt(results, index_audio, model, out_dir):
    seg = results['segments']
    for index in range(len(seg)):
        one_seg = seg[index]
        words = one_seg['words']
        for w in words:
            with open(f"{out_dir}transcriptions_whisper/{model}_{index_audio}.txt", "a+", encoding='utf-8') as myfile:
                myfile.write(
                    f'Word: {w["text"]}, start: {w["start"]}, end: {w["end"]}, confidence: {w["confidence"]}\n')

def tests(dir_path, out_dir):
    wer_metric = evaluate.load("wer")
    bleu_metric = evaluate.load("bleu")
    meteor_metric = evaluate.load("meteor")
    models = ["tiny", "base", "small", "medium", "large-v2"]
    nb_samples = len([entry for entry in os.listdir(f'{dir_path}transcription') if
                      os.path.isfile(os.path.join(f'{dir_path}transcription', entry))])
    tracks = [f'{dir_path}audio/{x}.mp3' for x in range(nb_samples)]
    labels = [open(f'{dir_path}transcription/{x}.txt', encoding='utf-8').read() for x in range(nb_samples)]
    res_models = []
    for model_size in models[2:]:
        model = whisper_timestamped.load_model(model_size, device='cpu')
        transcriptions_whisper = []
        for audio_dir in tracks:
            index_audio=audio_dir.split(".")[0].split("/")[-1]
            audio = whisper_timestamped.load_audio(audio_dir)
            result = whisper_timestamped.transcribe(model, audio, language="fr", plot_word_alignment=False, beam_size=5,
                                                    best_of=5, temperature=(0.0, 0.2, 0.4, 0.6, 0.8, 1.0), vad=False)
            transcriptions_whisper.append(result['text'])
            save_timestamps_to_txt(result, index_audio, model_size, out_dir)

        wer = wer_metric.compute(predictions=transcriptions_whisper, references=labels)
        bleu = bleu_metric.compute(predictions=transcriptions_whisper, references=labels)['bleu']
        meteor = meteor_metric.compute(predictions=transcriptions_whisper, references=labels)['meteor']
        res_models.append((wer, bleu, meteor))
        print("WER: ", wer, " BLEU: ", bleu, " METEOR: ", meteor)
    df = pandas.DataFrame({"Model": models, "wer": [res_models[x][0] for x in range(len(res_models))],
    "bleu": [res_models[x][1] for x in range(len(res_models))], "meteor": [res_models[x][2] for x in range(len(res_models))]})
    df.to_csv(f'{out_dir}performance_whisper_models.csv')

tests("data/test/","results/")
