from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

sentence = "How can I learn Python?"

embedding = model.encode(sentence)

print(embedding)
print(len(embedding))