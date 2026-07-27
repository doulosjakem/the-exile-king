with open(r'D:\the-exile-king\review_art_ollama.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = '''"options": {"temperature": 0.1, "num_ctx": 4096, "num_gpu": 0}'''
new = '''"options": {"temperature": 0.1, "num_ctx": 4096, "num_gpu": 1}'''

if old in content:
    content = content.replace(old, new)
    with open(r'D:\the-exile-king\review_art_ollama.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print('Updated review to use GPU (num_gpu=1)')
else:
    print('Could not find options string')
