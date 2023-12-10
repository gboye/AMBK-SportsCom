import evaluate
from transformers import WhisperForConditionalGeneration, WhisperTokenizer, Seq2SeqTrainingArguments, Seq2SeqTrainer, \
    WhisperProcessor
from data_collector import DataCollatorSpeechSeq2SeqWithPadding
from preprocessing import build_dataset, prepare_dataset
import torch


def logs_to_pred_labels():
    f = open(f'C:/Users/Cam/PycharmProjects/whisper/base testing/validation_data.txt', "r", encoding="utf-8").read()
    pred = []
    labels = []

    f = f.split('\n')
    del f[0]
    del f[-1]

    for e in range(len(f)):
        pair = f[e]
        pair = pair.split(" => ")
        pred.append(pair[0])
        labels.append(pair[1])
    return pred, labels

class WhisperWithTrainer:

    def __int__(self, model):
        self.model = model
        self.tokenizer = WhisperTokenizer.from_pretrained(f'openai/whisper-{model}', language="french", task="transcribe")
        self.wer = evaluate.load("wer")
        self.bleu = evaluate.load("bleu")
        self.meteor = evaluate.load("meteor")

    def pred_with_trainer(self, model_dir):
        trainer = self.build_trainer(model_dir, "trainer")
        audio_dataset = build_dataset()
        validation_set = audio_dataset["validation"].map(prepare_dataset, num_proc=3)
        results = trainer.predict(validation_set)
        pred_ids = results.predictions
        transcriptions = self.tokenizer.batch_decode(pred_ids, skip_special_tokens=True)
        return transcriptions


    def save_validation_data(self, pred_str, label_str, metrics):
        with open("base testing/validation_data.txt", "a+", encoding='utf-8') as myfile:
            myfile.write(f"_______ {metrics} ________\n")
            for e in range(len(label_str)):
                try:
                    myfile.write(pred_str[e] + " => " + label_str[e] + '\n')
                except:
                    pred_str1 = pred_str[e].encode('utf-8', 'ignore').decode("utf-8")
                    label_str1 = label_str[e].encode('utf-8', 'ignore').decode("utf-8")
                    myfile.write(pred_str1 + " => " + label_str1 + '\n')

                    print(pred_str1 + " => " + label_str1 + '\n')
            myfile.close()

    def compute_metrics(self, pred):
        pred_ids = pred.predictions
        label_ids = pred.label_ids

        # replace -100 with the pad_token_id
        label_ids[label_ids == -100] = self.tokenizer.pad_token_id

        # we do not want to group tokens when computing the metrics
        pred_str = self.tokenizer.batch_decode(pred_ids, skip_special_tokens=True)
        label_str = self.tokenizer.batch_decode(label_ids, skip_special_tokens=True)

        wer = self.wer.compute(predictions=pred_str, references=label_str)
        # bleu = bleu_metric.compute(predictions=pred_str, references=label_str)
        # meteor = meteor_metric.compute(predictions=pred_str, references=label_str)

        self.save_validation_data(pred_str, label_str, wer)

        return {"wer": wer, "bleu": -1, "meteor": -1}


    def build_trainer(self, root, OUTPUT_DIR):
        BATCH_SIZE = 1
        model = WhisperForConditionalGeneration.from_pretrained(root)
        tokenizer = WhisperTokenizer.from_pretrained(f'openai/whisper-tiny', language="french", task="transcribe")
        processor = WhisperProcessor.from_pretrained(f'openai/whisper-tiny', language="French", task="transcribe")
        processor.tokenizer = tokenizer
        data_collator = DataCollatorSpeechSeq2SeqWithPadding()
        data_collator.processor = processor

        test_args = Seq2SeqTrainingArguments(
            output_dir=OUTPUT_DIR,
            do_train=False,
            do_predict=True,
            per_device_eval_batch_size=BATCH_SIZE,
            dataloader_drop_last=False,
            generation_max_length=225,
            predict_with_generate=True

        )

        trainer = Seq2SeqTrainer(
            model=model,
            args=test_args,
            data_collator=data_collator,
            compute_metrics=self.compute_metrics,
            tokenizer=data_collator.processor.feature_extractor)

        return trainer

    def train_trainer(self):
        print(torch.cuda.is_available(), torch.zeros(1).cuda())
        trainer = self.build_training_trainer()
        trainer.train()
        trainer.save_model("test_timestamps/whisper_model")

    def build_training_trainer(self):
        audio_dataset = build_dataset()
        training_set = audio_dataset["train"].map(prepare_dataset, num_proc=3)
        validation_set = audio_dataset["validation"].map(prepare_dataset, num_proc=3)
        processor = WhisperProcessor.from_pretrained(f'openai/whisper-{self.model}', language="French", task="transcribe")
        tokenizer = WhisperTokenizer.from_pretrained(f'openai/whisper-tiny', language="french", task="transcribe")
        processor.tokenizer = tokenizer
        data_collator = DataCollatorSpeechSeq2SeqWithPadding()
        data_collator.processor = processor

        model = WhisperForConditionalGeneration.from_pretrained(f'openai/whisper-{self.model}', dropout=0.01)
        model.training = True

        model.config.forced_decoder_ids = None
        model.config.suppress_tokens = []

        training_args = Seq2SeqTrainingArguments(
            output_dir="test_timestamps",
            per_device_train_batch_size=16,
            gradient_accumulation_steps=2,
            learning_rate=1e-5,
            warmup_steps=500,
            max_steps=24,
            gradient_checkpointing=True,
            fp16=False,
            evaluation_strategy="steps",
            per_device_eval_batch_size=8,
            predict_with_generate=True,
            generation_max_length=225,
            save_steps=24,
            eval_steps=24,
            logging_steps=24,
            load_best_model_at_end=True,
            metric_for_best_model="wer",
            greater_is_better=False,
        )

        processor.save_pretrained(training_args.output_dir)

        trainer = Seq2SeqTrainer(
            args=training_args,
            model=model,
            train_dataset=training_set,
            eval_dataset=validation_set,
            data_collator=data_collator,
            compute_metrics=self.compute_metrics,
            tokenizer=data_collator.processor.feature_extractor,
        )

        return trainer
