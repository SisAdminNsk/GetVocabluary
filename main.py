from bs4 import BeautifulSoup
import requests
import threading
import json
import re

def get_all_chapters_names(url,parser_type) :
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text,parser_type)
    tag_name = 'a'
    words_chapters = soup.findAll(tag_name, href=True)
    splited_chapters = re.split(r', ', str(words_chapters))
    chapters_list = list()
    for chapter_name in splited_chapters:
        parsed_chapter_name = re.findall(r'en_ru/(.*?)">', chapter_name)
        if len(parsed_chapter_name) > 0:
            chapters_list.append(parsed_chapter_name[0])

    return chapters_list

def get_chapter_intervals(chapter_list) :
    map_chapter_to_interval = dict()
    start_index = end_index = 0
    for i in range(0, len(chapter_list) - 1) :
        if chapter_list[i][0] != chapter_list[i+1][0] :
            map_chapter_to_interval[chapter_list[i][0]] = (start_index, end_index)
            start_index = end_index + 1
        end_index+=1

    return map_chapter_to_interval

def get_all_words_from_chapters(chapters_list, url, parser_type) :
    map_eng_word_to_rus = dict()
    tag_name = 'p'
    for chapter in chapters_list:
        chapter_url = url + chapter
        html_text = requests.get(chapter_url).text
        soup = BeautifulSoup(html_text, parser_type)
        chapter_words = soup.findAll(tag_name)
        splited_chapter_words = re.split(r'</p>,', str(chapter_words))
        for splited_word in splited_chapter_words:
            splited_word += "###"
            parsed_rus_text = re.findall(r'</a>(.*?)###', splited_word)
            parsed_eng_text = re.findall(r'">(.*?)</a>', splited_word)
            map_eng_word_to_rus[parsed_eng_text[0]] = parsed_rus_text[0]

    return map_eng_word_to_rus

def load_to_json(filePath, english_to_russian_dict):
    to_json = list()

    for key,val in english_to_russian_dict.items():
        to_json.append({key : val})

    with open(filePath, 'w', encoding='utf-8') as f:
        f.write(json.dumps(to_json, sort_keys=False, indent=4,
                           ensure_ascii=False, separators=(',', ': ')))

chapters_url = 'https://wooordhunt.ru/dic/content/en_ru'
generalized_url = 'https://wooordhunt.ru/dic/list/en_ru/'
parser_type = 'html.parser'

all_chapters_names = get_all_chapters_names(chapters_url, parser_type)
english_russian_dict = get_all_words_from_chapters(all_chapters_names, generalized_url, parser_type)

json_path = 'parsed_dictionary.json'
load_to_json(json_path, english_russian_dict)