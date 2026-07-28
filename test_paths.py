import os
base = r'D:\Jake\ComfyUI_windows_portable\ComfyUI\output\ComfyUI\annointed-exile\prototype\unit-discs'
for f in os.listdir(base)[:3]:
    full = os.path.join(base, f)
    rel = os.path.relpath(full, r'D:\Jake\ComfyUI_windows_portable\ComfyUI\output\ComfyUI\annointed-exile')
    folder = os.path.dirname(rel).lower()
    print(f'rel={rel!r}')
    print(f'folder={folder!r}')
    print(f'folder.split(os.sep)={folder.split(os.sep)}')
    print(f'prototype in split={("prototype" in folder.split(os.sep))}')
    print()
