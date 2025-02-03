import re
import json
import simulate_wrong_data as swd
import numpy as np
import os

file_path = "data.json"
if not os.path.exists(file_path):
    # Tạo tệp JSON trống
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump({}, file)

error_probability = np.arange(0.2, 0.8 + 0.05, 0.05)
raw_data_path = "large_data.txt"
with open(file_path, 'w', encoding='utf-8') as output_file:
    with open(raw_data_path, "r", encoding="utf-8") as file:
        for line in file:
            sen = line.strip()
            wrong_sentences = [swd.remove_vietnamese_accent(sen)]
            for i in error_probability:
                wrong_sentences.append(swd.simulate_typo_vietnamese(sen, i))
            output_file.write(json.dumps({
                "sentence" : sen,
                "wrong_sentences": wrong_sentences
            }, ensure_ascii=False) + '\n')
