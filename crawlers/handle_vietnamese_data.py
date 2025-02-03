import json
import random

# Đường dẫn file gốc và các file kết quả
input_file_path = "data/data.json"
vietnamese_sentences_path = "data/vietnamese_sentences.json"

with open(vietnamese_sentences_path, 'w', encoding='utf-8') as output_file:
    with open(input_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            data = json.loads(line.strip())
            output_file.write(json.dumps({"text": data['sentence'], "label": "vietnamese"}, ensure_ascii=False) + '\n')
            output_file.write(json.dumps({"text": data['wrong_sentences'][0], "label": "potential vietnamese"}, ensure_ascii=False) + '\n')
            output_file.write(json.dumps({"text": data['wrong_sentences'][random.randint(1, 14)], "label": "potential vietnamese"}, ensure_ascii=False) + '\n')

