from transformers import MT5Tokenizer, MT5ForConditionalGeneration, AutoTokenizer, AutoModelForSequenceClassification
import torch

class T5TextCorrector:
    def __init__(self, model_dir="./fine_tuned_t5_vietnamese/checkpoint-44044"):
        self.tokenizer = MT5Tokenizer.from_pretrained(model_dir)
        self.model = MT5ForConditionalGeneration.from_pretrained(model_dir)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    def correct_text(self, input_text):
        input_ids = self.tokenizer(f"fix: {input_text}", return_tensors="pt").input_ids.to(self.device)
        outputs = self.model.generate(input_ids, max_length=128)
        corrected_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return corrected_text

class XRBTextPredictor:
    def __init__(self, model_dir="./my_xrb_model"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_dir)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_dir)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    def predict_language(self, input_text):
        input_ids = self.tokenizer(f"{input_text}", return_tensors="pt").input_ids.to(self.device)
        attention_mask = self.tokenizer(f"{input_text}", return_tensors="pt").attention_mask.to(self.device)
        outputs = self.model(input_ids=input_ids, attention_mask=attention_mask)
        logits = outputs.logits

        # Lấy nhãn dự đoán
        predicted_label = torch.argmax(logits, dim=-1).item()
        return predicted_label
