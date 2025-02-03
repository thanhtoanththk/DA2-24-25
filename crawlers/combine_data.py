import json
import random

def merge_large_json_files(file1, file2, output_file):
    with open(output_file, 'w', encoding='utf-8') as outfile:
        # Đọc từng dòng từ cả hai tệp và ghi trực tiếp vào tệp mới
        with open(file1, 'r', encoding='utf-8') as f1:
            for line in f1:
                outfile.write(line)

        with open(file2, 'r', encoding='utf-8') as f2:
            for line in f2:
                outfile.write(line)

    print(f"Tệp đã được trộn và lưu vào: {output_file}")

def shuffle_large_json_file(input_file, output_file):
    """
    Trộn ngẫu nhiên các dòng trong tệp JSON Lines lớn.

    Args:
        input_file (str): Đường dẫn tới tệp JSON đầu vào.
        output_file (str): Đường dẫn tới tệp JSON đầu ra.
    """
    with open(input_file, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()  # Đọc tất cả các dòng

    random.shuffle(lines)  # Trộn ngẫu nhiên các dòng

    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.writelines(lines)  # Ghi lại các dòng đã trộn

    print(f"Dữ liệu đã được trộn và lưu vào: {output_file}")

def split_large_json_file(input_file, output_files):
    with open(input_file, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

    # Đếm tổng số dòng
    total = len(lines)
    train_size = int(total * 0.7)
    val_size = int(total * 0.2)

    # Trộn ngẫu nhiên các dòng
    random.shuffle(lines)

    # Chia dữ liệu
    train_data = lines[:train_size]
    val_data = lines[train_size:train_size + val_size]
    test_data = lines[train_size + val_size:]

    # Lưu từng phần vào tệp riêng
    for data, output_file in zip([train_data, val_data, test_data], output_files):
        with open(output_file, 'w', encoding='utf-8') as outfile:
            outfile.writelines(data)

    print("Dữ liệu đã được chia thành:")
    print(f"- Train: {output_files[0]} - gồm {train_size} câu.")
    print(f"- Validation: {output_files[1]} - gồm {val_size} câu.")
    print(f"- Test: {output_files[2]} - gồm {len(test_data)} câu.")

# Đường dẫn tệp JSON
file1 = 'data/vietnamese_sentences.json'
file2 = 'data/newsgroups_sentences.json'
merged_file = 'data/merged_large.json'
output_files = ['data/train_large.json', 'data/val_large.json', 'data/test_large.json']

# Bước 1: Trộn tệp
merge_large_json_files(file1, file2, merged_file)

# Bước 2: Trộn ngẫu nhiên dữ liệu
random_file = 'data/random_large.json'
shuffle_large_json_file(merged_file, random_file)

# Bước 3: Chia tệp đã trộn
split_large_json_file(random_file, output_files)
