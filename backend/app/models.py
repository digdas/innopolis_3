from transformers import AutoTokenizer, AutoModel
import torch
import psycopg2
import random

# Инициализация модели BERT
tokenizer = AutoTokenizer.from_pretrained("DeepPavlov/rubert-base-cased-sentence")
model = AutoModel.from_pretrained("DeepPavlov/rubert-base-cased-sentence")

# Подключение к базе данных PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(
        dbname='qna_db',
        user='postgres',
        password='postgres',
        host='db'
    )
    return conn

# Функция для векторизации вопроса
def embed_question(question):
    inputs = tokenizer(question, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1)

# Функция для поиска похожего вопроса
def search_similar_question(query):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, question, answer FROM qna")
    qna_pairs = cur.fetchall()

    questions = [pair[1] for pair in qna_pairs]
    answers = [pair[2] for pair in qna_pairs]

    query_embedding = embed_question(query)
    question_embeddings = [embed_question(q) for q in questions]

    cosine_scores = [torch.nn.functional.cosine_similarity(query_embedding, q_emb, dim=1).item() for q_emb in question_embeddings]
    best_index = cosine_scores.index(max(cosine_scores))

    return answers[best_index]

# Функция для получения случайного вопроса-ответа
def get_random_qna():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT question, answer FROM qna ORDER BY RANDOM() LIMIT 1")
    return cur.fetchone()
