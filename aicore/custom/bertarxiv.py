import os
import glob
import logging
import evaluate
import numpy as np
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    DataCollatorWithPadding,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
    pipeline,
)


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('bertarxiv.log')
formatter = logging.Formatter(
    '[%(asctime)s] -- "%(filename)s" : "%(lineno)d" [-] "%(levelname)s" -- "%(message)s"'
    )
fh.setFormatter(formatter)
logger.addHandler(fh)

# https://learnopencv.com/fine-tuning-bert/

logger.debug("Reset Log File")
cmd = ">bertarxiv.log"
os.system(cmd)

logger.debug("Set Hyperparams")

BATCH_SIZE = 32
NUM_PROCS = 32
LR = 0.00005
EPOCHS = 5
MODEL = 'bert-base-uncased'
OUT_DIR = 'arxiv_bert'

logger.debug("Download and Prepare the Dataset")

train_dataset = load_dataset("ccdv/arxiv-classification", split='train')
# logger.debug(str(train_dataset))

valid_dataset = load_dataset("ccdv/arxiv-classification", split='validation')
# logger.debug(str(valid_dataset))

test_dataset = load_dataset("ccdv/arxiv-classification", split='test')
# logger.debug(str(test_dataset))

logger.debug("Visualize a sample: " + str(train_dataset[0]['label']))

logger.debug("Dataset Label Information")

id2label = {
    0: "math.AC",
    1: "cs.CV",
    2: "cs.AI",
    3: "cs.SY",
    4: "math.GR",
    5: "cs.CE",
    6: "cs.PL",
    7: "cs.IT",
    8: "cs.DS",
    9: "cs.NE",
    10: "math.ST"
}
label2id = {
    "math.AC": 0,
    "cs.CV": 1,
    "cs.AI": 2,
    "cs.SY": 3,
    "math.GR": 4,
    "cs.CE": 5,
    "cs.PL": 6,
    "cs.IT": 7,
    "cs.DS": 8,
    "cs.NE": 9,
    "math.ST": 10
}

logger.debug("Tokenizing the Dataset")
tokenizer = AutoTokenizer.from_pretrained(MODEL)

logger.debug("Func to Tokenize batch textual data")
def preprocess_function(examples):
    return tokenizer(
        examples["text"],
        truncation=True,
    )

"""
logger.debug("Map to batch processing")
tokenized_train = train_dataset.map(
    preprocess_function,
    batched=True,
    batch_size=BATCH_SIZE,
    num_proc=NUM_PROCS
)
 
tokenized_valid = valid_dataset.map(
    preprocess_function,
    batched=True,
    batch_size=BATCH_SIZE,
    num_proc=NUM_PROCS
)

tokenized_test = test_dataset.map(
    preprocess_function,
    batched=True,
    batch_size=BATCH_SIZE,
    num_proc=NUM_PROCS
)
# """

logger.debug("Data Collator")
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

logger.debug("Sample Tokenization Example")
tokenized_sample = preprocess_function(train_dataset[0])

logger.debug(str(tokenized_sample))
logger.debug(f"Length of tokenized IDs: {len(tokenized_sample.input_ids)}")
logger.debug(f"Length of attention mask: {len(tokenized_sample.attention_mask)}")

logger.debug("Evaluation Metrics")
accuracy = evaluate.load('accuracy')
def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)
    return accuracy.compute(predictions=predictions, references=labels)

logger.debug("Preparing the BERT Model")

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL,
    num_labels=11,
    id2label=id2label,
    label2id=label2id,
)

logger.debug("Training Arguments")

training_args = TrainingArguments(
    output_dir=OUT_DIR,
    learning_rate=LR,
    per_device_train_batch_size=BATCH_SIZE,
    per_device_eval_batch_size=BATCH_SIZE,
    num_train_epochs=EPOCHS,
    weight_decay=0.01,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
    save_total_limit=3,
    report_to='tensorboard',
    fp16=True
)

logger.debug("Initializing the Trainer")
"""
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train,
    eval_dataset=tokenized_valid,
    tokenizer=tokenizer,
    data_collator=data_collator,
    compute_metrics=compute_metrics,
)
 
history = trainer.train()


logger.debug("Evaluation")
trainer.evaluate(tokenized_test)

logger.debug("Inference on Unseen Data")

AutoModelForSequenceClassification.from_pretrained(f"arxiv_bert/checkpoint-4440")
 
tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
classify = pipeline(task='text-classification', model=model, tokenizer=tokenizer)
 
all_files = glob.glob('inference_data/*')
for file_name in all_files:
    file = open(file_name)
    content = file.read()
    print(content)
    result = classify(content)
    print('PRED: ', result)
    print('GT: ', file_name.split('_')[-1].split('.txt')[0])
    print('\n')
"""
