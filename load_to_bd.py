import sqlite3
import sqlite3 as sq
import json


def create_db_if_not_exists(bd_path):
    with sq.connect(bd_path) as connection:
        db = connection.cursor()
        db.execute("""CREATE TABLE IF NOT EXISTS vocabulary (
        word_id INTEGER PRIMARY KEY AUTOINCREMENT,
        word TEXT,
        translation TEXT
        )""")


def read_from_file_json(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        file_content = f.read()
        json_content = json.loads(file_content)

    return json_content


def write_json_content_to_db(json_content, bd_path):
    with sq.connect(bd_path) as connection:
        db = connection.cursor()
        for key, val in json_content.items():
            try:
                db.execute(f"INSERT INTO vocabulary (word, translation) VALUES ('{key}','{val}')")
            except sqlite3.OperationalError:
                pass


json_path = "parsed_dictionary.json"
bd_path = "vocabulary.db"

create_db_if_not_exists(bd_path)
json_content = read_from_file_json(json_path)
write_json_content_to_db(json_content, bd_path)
