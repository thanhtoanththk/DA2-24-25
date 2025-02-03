from transformers import MT5Tokenizer, MT5ForConditionalGeneration
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
