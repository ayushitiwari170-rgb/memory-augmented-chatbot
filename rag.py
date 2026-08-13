from sentence_transformers import SentenceTransformer
import chromadb
import google.generativeai as genai

genai.configure(api_key="YOUR_GEMINI_API_KEY_HERE")
gen_model = genai.GenerativeModel("gemini-1.5-flash")

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.Client()
collection = client.create_collection("knowledge")

with open("data/knowledge.txt", "r", encoding="utf-8") as f:
    text = f.read()

chunks = [c.strip() for c in text.split("\n\n") if c.strip()]

for i, chunk in enumerate(chunks):
    emb = model.encode(chunk).tolist()
    collection.add(
        documents=[chunk],
        embeddings=[emb],
        ids=[str(i)]
    )

def rag_answer(query):
    q = model.encode(query).tolist()
    result = collection.query(query_embeddings=[q], n_results=1)
    docs = result["documents"][0]
    context = docs[0] if docs else "No relevant information found."

    prompt = f"Answer the question based on this context:\nContext: {context}\nQuestion: {query}\nAnswer:"
    response = gen_model.generate_content(prompt)
    return response.text
