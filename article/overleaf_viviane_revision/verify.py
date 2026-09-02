import sys, os, re

d = r'C:\mysystems\projects\b3-econophysics-ai\article\overleaf_viviane_revision\sections'
files = [f for f in sorted(os.listdir(d)) if f.endswith('.tex')]
all_text = ""
for f in files:
    with open(os.path.join(d, f), 'r', encoding='utf-8') as file:
        all_text += f"\n--- FILE: {f} ---\n" + file.read()

main_tex = open(r'C:\mysystems\projects\b3-econophysics-ai\article\overleaf_viviane_revision\main.tex', 'r', encoding='utf-8').read()
all_text += "\n--- FILE: main.tex ---\n" + main_tex

print("=== 1. FREQUÊNCIA DE TERMOS ===")
terms = ['empirical', 'topology', 'topological', 'consistent with', 'provide', 'provides', 'interpreted as', 'should be interpreted', 'rather than', 'incremental', 'therefore', 'diagnostic', 'informative', 'complementary', 'mesoscopic', 'pipeline']
for t in terms:
    count = len(re.findall(r'\b' + t + r'\b', all_text, re.IGNORECASE))
    print(f"{t:25s} => {count}")

we_count = len(re.findall(r'\bwe\b', all_text, re.IGNORECASE))
print(f"{'we / We':25s} => {we_count}")

print("\n=== 2. TABELAS ÓRFÃS ===")
tabs_defined = re.findall(r'\\label\{(tab:[^}]+)\}', all_text)
tabs_cited = re.findall(r'\\ref\{(tab:[^}]+)\}', all_text)
orphans = [t for t in set(tabs_defined) if t not in tabs_cited]
print(f"Tabelas definidas: {len(set(tabs_defined))}")
print(f"Tabelas órfãs: {orphans if orphans else 'Nenhuma!'}")

print("\n=== 3. ORDEM DAS FIGURAS ===")
figs_cited = []
for m in re.finditer(r'\\ref\{(fig:[^}]+)\}', all_text):
    if m.group(1) not in figs_cited:
        figs_cited.append(m.group(1))
figs_defined = re.findall(r'\\label\{(fig:[^}]+)\}', all_text)
print("Primeiras 5 citadas:  ", figs_cited[:5])
print("Primeiras 5 definidas:", [f for f in figs_defined if not f.startswith('sec:')][:5])

print("\n=== 4. COMPRIMENTO DOS HIGHLIGHTS ===")
highlights = re.search(r'\\begin\{highlights\}(.*?)\\end\{highlights\}', main_tex, re.DOTALL)
if highlights:
    items = re.findall(r'\\item\s+(.*)', highlights.group(1))
    for i, item in enumerate(items, 1):
        print(f"H{i}: {len(item)} chars -> {item[:50]}...")
else:
    print("Highlights não encontrados no main.tex.")

print("\n=== 5. ESTILO DA BIBLIOGRAFIA ===")
bib_style = re.search(r'\\bibliographystyle\{(.*?)\}', main_tex)
print(f"Estilo atual: {bib_style.group(1) if bib_style else 'Não encontrado'}")

print("\n=== 6. TÍTULO DECLARAÇÃO IA ===")
declarations = open(r'C:\mysystems\projects\b3-econophysics-ai\article\overleaf_viviane_revision\sections\declarations.tex', 'r', encoding='utf-8').read()
ai_sec = re.search(r'\\section\*?\{([^}]*generative AI[^}]*)\}', declarations, re.IGNORECASE)
print(f"Título IA: {ai_sec.group(1) if ai_sec else 'Não encontrado'}")
