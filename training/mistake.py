from datasets import Dataset
import json
import torch
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
from sklearn.preprocessing import LabelEncoder
from tqdm import tqdm
from transformers import T5Tokenizer, T5ForConditionalGeneration, TrainingArguments, Trainer, MT5Tokenizer, MT5ForConditionalGeneration
from torch.utils.data import DataLoader

train_file_path = "./new_data2/train.json"
val_file_path = "./new_data2/val.json"
test_file_path = "./new_data2/test.json"

# Load data from a text file
def load_data(file_path):
    inputs, outputs = [], []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            data = eval(line.strip())
            for i in data['wrong_sentences']:
                inputs.append(i)
                outputs.append(data["sentence"])
    return Dataset.from_dict({"input": inputs, "output": outputs})

train_dataset = load_data(train_file_path)
val_dataset = load_data(val_file_path)
# Load T5 tokenizer
model_name = "google/mt5-small"  # Use a pre-trained T5 model
tokenizer = MT5Tokenizer.from_pretrained(model_name)

# Tokenize the dataset
def preprocess_data(batch):
    inputs = ["fix: " + text for text in batch["input"]]
    model_inputs = tokenizer(inputs, max_length=128, truncation=True, padding="max_length")
    
    with tokenizer.as_target_tokenizer():
        labels = tokenizer(batch["output"], max_length=128, truncation=True, padding="max_length")
    
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

# Apply tokenization
tokenized_train_dataset = train_dataset.map(preprocess_data, batched=True, remove_columns=["input", "output"])
tokenized_val_dataset = val_dataset.map(preprocess_data, batched=True, remove_columns=["input", "output"])

# Load T5 model
model = MT5ForConditionalGeneration.from_pretrained(model_name)

# Define training arguments
training_args = TrainingArguments(
    output_dir="./fine_tuned_t5_vietnamese",
    evaluation_strategy="epoch",  # Evaluate at the end of each epoch
    learning_rate=2e-5,
    per_device_train_batch_size=32,
    per_device_eval_batch_size=64,
    num_train_epochs=2,
    weight_decay=0.01,
    save_strategy="epoch",  # Save the model at the end of each epoch
    logging_dir="./logs",
    logging_steps=10,
    save_total_limit=2,  # Limit the number of saved checkpoints
    fp16=False,
    push_to_hub=False
)

# Initialize Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train_dataset,
    eval_dataset=tokenized_val_dataset,  # Pass the validation dataset
    tokenizer=tokenizer
)

trainer.train()

model.save_pretrained("../fine_tuned_t5_vietnamese")
tokenizer.save_pretrained("../fine_tuned_t5_vietnamese")
