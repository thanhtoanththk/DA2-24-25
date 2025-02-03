from sklearn.datasets import fetch_20newsgroups
import nltk
import string
import json
import re

nltk.download('punkt_tab')  # Ensure NLTK's Punkt tokenizer is downloaded

# Load the 20 Newsgroups dataset
newsgroups_data = fetch_20newsgroups(subset='all', remove=('headers', 'footers', 'quotes'))

all_sentences = []

for document in newsgroups_data.data:
    sentences = nltk.sent_tokenize(document)  # Tokenize document into sentences
    for sentence in sentences:
      if len(sentence) <= 20:
        continue
      text = ''.join(sentence.strip()).replace("\n", "").replace("\t", "").translate(str.maketrans('', '', string.punctuation.replace('.', '').replace(',', '')))
      text = re.sub(r'\s+', ' ', text)
      text = re.sub(r'\.{2,}', '', text)
      all_sentences.append(text)

print('Số lượng câu tiếng anh đã thu thập: ' + str(len(all_sentences)) + ' câu.')
print(f"\nExample:")
# Display the first 5 sentences with labels
for entry in all_sentences[:10]:
    print(entry)

print(f"\n")

# Split the text data into sentences
all_sentences_with_labels = []

for document in newsgroups_data.data:
    sentences = nltk.sent_tokenize(document)  # Tokenize document into sentences
    for sentence in sentences:
      if len(sentence) <= 20:
        continue
      text = ''.join(sentence.strip()).replace("\n", "").replace("\t", "").translate(str.maketrans('', '', string.punctuation.replace('.', '').replace(',', '')))
      text = re.sub(r'\s+', ' ', text)
      text = re.sub(r'\.{2,}', '', text)
      all_sentences_with_labels.append({"text": text, "label": "english"})

print('Số lượng câu tiếng anh đã gắn nhãn: ' + str(len(all_sentences_with_labels)) + ' câu.')
print(f"\nExample:")
# Display the first 5 sentences with labels
for entry in all_sentences_with_labels[:10]:
    print(f"Text: {entry['text']} - Label: {entry['label']}")

# Save to JSON file
with open('newsgroups_sentences.json', 'w', encoding='utf-8') as f:
  for entry in all_sentences_with_labels:
    f.write(json.dumps(entry, ensure_ascii=False)+'\n')
