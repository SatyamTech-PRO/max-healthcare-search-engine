import faiss, numpy as np, pandas as pd
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
index = faiss.read_index('backend/data/procedures_index.faiss')
df = pd.read_csv('backend/data/procedures_clean.csv')

query = 'blood test'
emb = model.encode([query]).astype('float32')
distances, indices = index.search(emb, 5)

print(f'Top 5 results for: {query}')
for i, idx in enumerate(indices[0]):
    print(f'{i+1}. {df.iloc[idx]["clean_name"]}')