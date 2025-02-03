import requests
from bs4 import BeautifulSoup
import time
import re
import os
import json

def is_valid_url(url):
    pattern = re.compile(
        r'^(https?://)'  # Giao thức: http hoặc https
        r'([a-zA-Z0-9.-]+)'  # Tên miền
        r'(\.[a-zA-Z]{2,})'  # Phần mở rộng tên miền (e.g., .com, .vn)
        r'(:[0-9]{1,5})?'  # Cổng (tùy chọn)
        r'(/.*)?$'  # Đường dẫn (tùy chọn)
    )
    return bool(pattern.match(url))
def split_sentences(text):
    # Regular Expression để tách câu
    sentence_pattern = r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|!)(\s|$)'
    sentences = re.split(sentence_pattern, text)

    # Loại bỏ các phần tử rỗng và xóa khoảng trắng thừa
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]

    return sentences

response = requests.get("https://thanhnien.vn/api/list-mega-menu.htm")
soup = BeautifulSoup(response.content, "html.parser")
links = []
titles = soup.findAll('div', class_='box')
total_titles = []
title_list = {}
pattern = r"http"
for lists in titles:
    main_title = lists.find('a', class_='title').get_text()
    title_list[main_title] = []
    list = lists.findAll('a', class_='item')
    for link in list:
        if re.search(pattern, link.attrs["href"]):
            continue
        title_list[main_title].append(link.get_text())
        total_titles.append(link.get_text())
        links.append(link.attrs["href"])
print('Tổng số chủ đề: ', len(total_titles))

title_file_path = "title.json"
if not os.path.exists(title_file_path):
    with open(title_file_path, 'a', encoding='utf-8') as file:
        json.dump({key: value for key, value in title_list.items() if value}, file, ensure_ascii=False, indent=4)

total_post = 0
link_posts = []
for link in links:
    response = requests.get("https://thanhnien.vn" + link)
    soup = BeautifulSoup(response.content, "html.parser")
    posts = soup.findAll('div', class_='box-category-item')
    total_post += len(posts)
    for post in posts:
        post_link = post.find('a', class_='box-category-link-with-avatar')
        if post_link:
            link_posts.append(post_link.attrs["href"])
    time.sleep(1)
print('Tổng số bài viết: ', total_post)
raw_data_path = "large_data.txt"
if os.path.exists(raw_data_path):
    with open(raw_data_path, "a", encoding="utf-8") as file:
        for link in link_posts:
            if is_valid_url("https://thanhnien.vn" + link):
                try:
                    response_post = requests.get("https://thanhnien.vn" + link)
                    soup_post = BeautifulSoup(response_post.content, "html.parser")
                    contents = soup_post.find('div', class_='detail-content')
                    if contents:
                        raw_data = [paragragh.get_text() for paragragh in contents.findAll('p')]
                        for data in raw_data:
                            sentences = split_sentences(data)
                            for sen in sentences:
                                if re.search(r".*?:.*", sen) :
                                    continue
                                if re.search(r"(.*https?://[^\s]+.*)", sen):
                                    continue
                                if re.search(r".+\.$", sen):
                                    file.write(sen + '\n')
                except Exception as e:
                    print("Đã xảy ra lỗi: ", e)
