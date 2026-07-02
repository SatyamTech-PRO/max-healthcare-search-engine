import faiss, numpy as np, pandas as pd, requests
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
index = faiss.read_index('backend/data/procedures_index.faiss')
df = pd.read_csv('backend/data/procedures_clean.csv')

def search_procedures(query, top_k=5):
    emb = model.encode([query]).astype('float32')
    distances, indices = index.search(emb, top_k)
    return [df.iloc[idx]['clean_name'] for idx in indices[0]]

def ask_llm(query, procedures):
    context = "\n".join(f"- {p}" for p in procedures)
    prompt = f"""You are a Max Healthcare assistant. Based on these procedures:
{context}
Answer this question: {query}"""

    response = requests.post('http://localhost:11434/api/generate', json={
        "model": "tinyllama",
        "prompt": prompt,
        "stream": False
    })
    result = response.json()
    print("Raw:", result)
    return result.get('response', str(result))

query = "What heart procedures are available?"
procedures = search_procedures(query)
answer = ask_llm(query, procedures)

print(f"\nQuery: {query}")
print(f"\nProcedures Found:")
for p in procedures:
    print(f"  - {p}")
print(f"\nAnswer:\n{answer}")