import psycopg2
import os
from datasets import load_dataset

def load_data():
    # Подключение к базе данных PostgreSQL
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT")
    )
    cur = conn.cursor()

    # Создание таблицы вопросов-ответов
    cur.execute("""
    CREATE TABLE IF NOT EXISTS questions_answers (
        id SERIAL PRIMARY KEY,
        question TEXT,
        answer TEXT
    );
    """)

    # Загрузка русского датасета вопросов-ответов
    dataset = load_dataset("IlyaGusev/russian_super_glue", "russian_rubq", split="train")

    # Проход по датасету и вставка данных в БД
    for entry in dataset:
        question = entry['question']
        answer = entry['answers'][0]['text'] if entry['answers'] else None  # Берем первый ответ из списка
        if answer:
            cur.execute("""
            INSERT INTO questions_answers (question, answer) VALUES (%s, %s);
            """, (question, answer))

    # Сохранение изменений и закрытие соединения
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    load_data()
