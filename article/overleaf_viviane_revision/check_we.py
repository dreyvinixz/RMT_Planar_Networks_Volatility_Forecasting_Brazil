import sys, os, re
sys.stdout.reconfigure(encoding='utf-8')
from PyPDF2 import PdfReader

base = r'C:\mysystems\projects\b3-econophysics-ai\article\literature_review\docs'
files = [f for f in os.listdir(base) if f.endswith('.pdf') and '2302.08208' not in f]

total_we = 0
for fname in files:
    path = os.path.join(base, fname)
    r = PdfReader(path)
    # Read first 8 pages to get a good sample of intro/methodology
    txt = '\n'.join([p.extract_text() or '' for p in r.pages[:8]])
    
    # regex for "we" as a distinct word, case insensitive
    we_matches = re.findall(r'\bwe\b', txt, re.IGNORECASE)
    total_we += len(we_matches)
    
    print(f'\n' + '='*60)
    print(f'Artigo: {fname[:50]}...')
    print(f'Quantidade de "We/we" nas primeiras páginas: {len(we_matches)}')
    
    # Extracting some real examples of usage
    examples = list(re.finditer(r'(?:\w+\W+){0,5}\bwe\b(?:\W+\w+){0,8}', txt, re.IGNORECASE))[:5]
    if examples:
        print(f'Exemplos de uso no texto:')
        for m in examples:
            line = m.group(0).replace('\n', ' ').strip()
            print(f'  -> "... {line} ..."')
    else:
        print(f'Nenhum "we" encontrado.')

print(f'\nTotal de "we" encontrados nestes artigos da revista: {total_we}')
