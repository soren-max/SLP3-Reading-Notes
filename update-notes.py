import json, urllib.request, sys, os

os.chdir('/home/hoot/project1/note/SLP3-Reading-Notes')

def patch_note(note_id, title, content, tags):
    body = json.dumps({'title': title, 'content': content, 'tags': tags}).encode('utf-8')
    req = urllib.request.Request(
        f'http://localhost:8000/api/notes/{note_id}',
        data=body,
        headers={'Content-Type': 'application/json'},
        method='PATCH'
    )
    resp = urllib.request.urlopen(req)
    return json.loads(resp.read())

# Ch 2: Words and Tokens
with open('Part-I-Large-Language-Models/02-Words-and-Tokens.md') as f:
    content = f.read().split('---', 2)[2].strip()

patch_note(1, "Words and Tokens：LLM 与 KG-RAG 的输入层基础", content, "LLM,Tokenization,RAG,KG,IE,NER,EntityLinking,Reasoning")
print('Note 1 done')

# Ch 3: Embeddings
with open('Part-I-Large-Language-Models/03-Embeddings.md') as f:
    content = f.read().split('---', 2)[2].strip()

r = patch_note(2, "Embeddings：RAG、实体链接与语义检索的向量基础", content, "LLM,Embedding,VectorSemantics,RAG,KG,IE,EntityLinking,Reasoning")
print(f'Note 2 done: {len(r["content"])} chars')
