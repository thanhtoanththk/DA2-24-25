from datasets import Dataset
import json
from torch.utils.data import Dataset as dt
import torch
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
from sklearn.preprocessing import LabelEncoder
from tqdm import tqdm
from transformers import T5ForConditionalGeneration, T5Tokenizer

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

        # Lấy nhãn dự đoán
        predict = model.generate(input_ids)
        result = tokenizer.decode(predict[0], skip_special_tokens=True)

    return result


model = T5ForConditionalGeneration.from_pretrained("./my_t5_model")
tokenizer = T5Tokenizer.from_pretrained("./my_t5_model")

device = torch.device("cuda")
model.to(device)
texts = []
test_labels = []
pred_labels = []
# Loop qua dữ liệu test
for data in tqdm(test_data, desc="Testing"):
    texts.append(data['input'])
    predicted = predict_language(data['input'], model, tokenizer, device)
    test_labels.append(data['output'])
    pred_labels.append(predicted)
# Lưu ví dụ cho từng case
cases = {
    "Case 1": [],  # Thực tế 0, dự đoán 0
    "Case 2": [],  # Thực tế 0, dự đoán 1
    "Case 3": [],  # Thực tế 1, dự đoán 0
    "Case 3": [],  # Thực tế 1, dự đoán 1
    "Case 4": [],  # Thực tế 1, dự đoán 2
    "Case 5": [],  # Thực tế 2, dự đoán 0
    "Case 6": [],   # Thực tế 2, dự đoán 1
    "Case 7": []   # Thực tế 2, dự đoán 2
}

# Lấy ví dụ cho từng case
for idx, (text, true_label, pred_label) in enumerate(zip(texts, test_labels, pred_labels)):
    if true_label == 'english' and pred_label == 'english' and len(cases["Case 1"]) <= 10:
        cases["Case 1"].append({"text": text, "true_label": true_label, "pred_label": pred_label})
    elif true_label == 'english' and pred_label == 'potential vietnamese' and len(cases["Case 2"]) <= 10:
        cases["Case 2"].append({"text": text, "true_label": true_label, "pred_label": pred_label})
    elif true_label == 'potential vietnamese' and pred_label == 'english':
        cases["Case 3"].append({"text": text, "true_label": true_label, "pred_label": pred_label})
    elif true_label == 'potential vietnamese' and pred_label == 'potential vietnamese' and len(cases["Case 4"]) <= 10:
        cases["Case 4"].append({"text": text, "true_label": true_label, "pred_label": pred_label})
    elif true_label == 'vietnamese' and pred_label == 'english':
        cases["Case 5"].append({"text": text, "true_label": true_label, "pred_label": pred_label})
    elif true_label == 'vietnamese' and pred_label == 'potential vietnamese' and len(cases["Case 6"]) <= 10:
        cases["Case 6"].append({"text": text, "true_label": true_label, "pred_label": pred_label})
    elif true_label == 'vietnamese' and pred_label == 'potential vietnamese' and len(cases["Case 7"]) <= 10:
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
            print(f"Text: {example[3]['text']}")
            print(f"True Label: {example[3]['true_label']}")
            print(f"Predicted Label: {example[3]['pred_label']}")
        if case == 'Case 3':
            print(f"\n{case}:")
            print(f"Text: {example[49]['text']}")
            print(f"True Label: {example[49]['true_label']}")
            print(f"Predicted Label: {example[49]['pred_label']}")
        if case == 'Case 4':
            print(f"\n{case}:")
            print(f"Text: {example[4]['text']}")
            print(f"True Label: {example[4]['true_label']}")
            print(f"Predicted Label: {example[4]['pred_label']}")
        if case == 'Case 5':
            print(f"\n{case}:")
            print(f"Text: {example[0]['text']}")
            print(f"True Label: {example[0]['true_label']}")
            print(f"Predicted Label: {example[0]['pred_label']}")
        if case == 'Case 6':
            print(f"\n{case}:")
            print(f"Text: {example[2]['text']}")
            print(f"True Label: {example[2]['true_label']}")
            print(f"Predicted Label: {example[2]['pred_label']}")
        if case == 'Case 7':
            print(f"\n{case}:")
            print(f"Text: {example[5]['text']}")
            print(f"True Label: {example[5]['true_label']}")
            print(f"Predicted Label: {example[5]['pred_label']}")
            
