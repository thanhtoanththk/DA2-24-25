import json
import random

# Đường dẫn file gốc và các file kết quả
input_file_path = "data.json"
train_file_path = "train.json"
val_file_path = "val.json"
test_file_path = "test.json"

# Đọc file JSON
with open(input_file_path, 'r', encoding='utf-8') as file:
    data = [json.loads(line.strip()) for line in file]

# Xáo trộn dữ liệu để chia ngẫu nhiên
random.shuffle(data)

# Chia dữ liệu theo tỷ lệ 7:2:1
total = len(data)
train_size = int(total * 0.7)
val_size = int(total * 0.2)

train_data = data[:train_size]
val_data = data[train_size:train_size + val_size]
test_data = data[train_size + val_size:]

# Hàm ghi dữ liệu ra file theo định dạng từng dòng
def write_json(file_path, dataset):
    with open(file_path, 'w', encoding='utf-8') as file:
        for item in dataset:
            file.write(json.dumps(item, ensure_ascii=False) + '\n')

# Ghi dữ liệu ra các file
write_json(train_file_path, train_data)
write_json(val_file_path, val_data)
write_json(test_file_path, test_data)
