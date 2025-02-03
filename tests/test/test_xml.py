from datasets import Dataset
import json
from torch.utils.data import Dataset as dt
import torch
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
from sklearn.preprocessing import LabelEncoder
from tqdm import tqdm
from transformers import AutoModelForSequenceClassification, AutoTokenizer

train_file_path = "../new_data/train_large.json"
val_file_path = "../new_data/val_large.json"
test_file_path = "../new_data/test_large.json"

# Chuyển dữ liệu thành định dạng phù hợp cho Hugging Face Dataset
data_processed = []
# Đọc file JSON
with open(train_file_path, 'r', encoding='utf-8') as file:
    for line in file:
        data = json.loads(line.strip())
        data_processed.append({
            "input": data["text"],
            "output": data["label"]
        })

data_validate = []
# Đọc file JSON
with open(val_file_path, 'r', encoding='utf-8') as file:
    for line in file:
        data = json.loads(line.strip())
        data_validate.append({
            "input": data["text"],
            "output": data["label"]
        })

data_test = []
# Đọc file JSON
with open(test_file_path, 'r', encoding='utf-8') as file:
    for line in file:
        data = json.loads(line.strip())
        data_test.append({
            "input": data["text"],
            "output": data["label"]
        })
# Chuyển đổi dữ liệu thành Dataset của Hugging Face
train_data = Dataset.from_dict({
    'input': [item['input'] for item in data_processed],
    'output': [item['output'] for item in data_processed]
})

val_data = Dataset.from_dict({
    'input': [item['input'] for item in data_validate],
    'output': [item['output'] for item in data_validate]
})

test_data = Dataset.from_dict({
    'input': [item['input'] for item in data_test],
    'output': [item['output'] for item in data_test]
})

# Hàm dự đoán ngôn ngữ
def predict_language(input_text, model, tokenizer, device):
    model.eval()
    with torch.no_grad():
        # Tokenize input text
        inputs = tokenizer(
            input_text,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=128
        )
        input_ids = inputs["input_ids"].to(device)
        attention_mask = inputs["attention_mask"].to(device)

        # Forward pass
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        logits = outputs.logits

        # Lấy nhãn dự đoán
        predicted_label = torch.argmax(logits, dim=-1).item()

    return predicted_label


model_directory = './my_xrb_model'

# Load the tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_directory)

# Load the model
model = AutoModelForSequenceClassification.from_pretrained(model_directory)

device = torch.device("cuda")
model.to(device)
test_label_map = {'english': 0, 'potential vietnamese': 1, 'vietnamese': 2}
texts = []
test_labels = []
pred_labels = []
# Loop qua dữ liệu test
for data in tqdm(test_data, desc="Testing"):
    texts.append(data['input'])
    predicted = predict_language(data['input'], model, tokenizer, device)
    test_labels.append(test_label_map[data['output']])
    pred_labels.append(predicted)
# Lưu ví dụ cho từng case
cases = {
    "Case 1": [],  # Thực tế 0, dự đoán 0
    "Case 2": [],  # Thực tế 0, dự đoán 1
    "Case 3": [],  # thực tế 1, dự đoán 0
    "Case 4": [],  # Thực tế 1, dự đoán 1
    "Case 5": [],  # Thực tế 1, dự đoán 2
    "Case 6": [],  # Thực tế 2, dự đoán 2
    "Case 7": [],  # Thực tế 2, dự đoán 1
     
}
# Lấy ví dụ cho từng case
for idx, (text, true_label, pred_label) in enumerate(zip(texts, test_labels, pred_labels)):
    if true_label == 0 and pred_label == 0 and len(cases["Case 1"]) <= 10:
        cases["Case 1"].append({"text": text, "true_label": true_label, "pred_label": pred_label})
    elif true_label == 0 and pred_label == 1 and len(cases["Case 2"]) <= 10:
        cases["Case 2"].append({"text": text, "true_label": true_label, "pred_label": pred_label})
    elif true_label == 1 and pred_label == 0 and len(cases["Case 3"]) <= 10:
        cases["Case 3"].append({"text": text, "true_label": true_label, "pred_label": pred_label})
    elif true_label == 1 and pred_label == 1 and len(cases["Case 4"]) <= 10:
        cases["Case 4"].append({"text": text, "true_label": true_label, "pred_label": pred_label})
    elif true_label == 1 and pred_label == 2 and len(cases["Case 5"]) <= 10:
        cases["Case 5"].append({"text": text, "true_label": true_label, "pred_label": pred_label})
    elif true_label == 2 and pred_label == 2 and len(cases["Case 6"]) <= 10:
        cases["Case 6"].append({"text": text, "true_label": true_label, "pred_label": pred_label})
    elif true_label == 2 and pred_label == 1 and len(cases["Case 7"]) <= 10:
        cases["Case 7"].append({"text": text, "true_label": true_label, "pred_label": pred_label})

# # In ra từng case
# print("Examples for Each Case:")
# for case, example in cases.items():
#     if example:
#         for ex in example:
#             print(f"\n{case}:")
#             print(f"Text: {ex['text']}")
#             print(f"True Label: {ex['true_label']}")
#             print(f"Predicted Label: {ex['pred_label']}")

# In ra từng case
print("Examples for Each Case:")
for case, example in cases.items():
    if example:
        if case == 'Case 1':
            print(f"\n{case}:")
            print(f"Text: {example[0]['text']}")
            print(f"True Label: {example[0]['true_label']}")
            print(f"Predicted Label: {example[0]['pred_label']}")
        if case == 'Case 2':
            print(f"\n{case}:")
            print(f"Text: {example[0]['text']}")
            print(f"True Label: {example[0]['true_label']}")
            print(f"Predicted Label: {example[0]['pred_label']}")
        if case == 'Case 3':
            print(f"\n{case}:")
            print(f"Text: {example[0]['text']}")
            print(f"True Label: {example[0]['true_label']}")
            print(f"Predicted Label: {example[0]['pred_label']}")
        if case == 'Case 4':
            print(f"\n{case}:")
            print(f"Text: {example[1]['text']}")
            print(f"True Label: {example[1]['true_label']}")
            print(f"Predicted Label: {example[1]['pred_label']}")
        if case == 'Case 5':
            print(f"\n{case}:")
            print(f"Text: {example[2]['text']}")
            print(f"True Label: {example[2]['true_label']}")
            print(f"Predicted Label: {example[2]['pred_label']}")
        if case == 'Case 6':
            print(f"\n{case}:")
            print(f"Text: {example[1]['text']}")
            print(f"True Label: {example[1]['true_label']}")
            print(f"Predicted Label: {example[1]['pred_label']}")
        if case == 'Case 7':
            print(f"\n{case}:")
            print(f"Text: {example[1]['text']}")
            print(f"True Label: {example[1]['true_label']}")
            print(f"Predicted Label: {example[1]['pred_label']}")            
