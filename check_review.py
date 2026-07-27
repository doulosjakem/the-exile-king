import json, os

p = r'D:\the-exile-king\art_review_report.json'
if os.path.exists(p):
    with open(p, 'r') as f:
        r = json.load(f)
    total = r.get('total_reviewed')
    errors = r.get('errors')
    keeps = r.get('keep')
    trash = r.get('trash')
    print(f'Total reviewed: {total}')
    print(f'Errors: {errors}')
    print(f'Keep: {keeps}')
    print(f'Trash: {trash}')
    if r.get('images'):
        last = r['images'][-1]
        print(f'Last: {last["filename"]} -> {last["decision"]}')
else:
    print('Report not created yet')
