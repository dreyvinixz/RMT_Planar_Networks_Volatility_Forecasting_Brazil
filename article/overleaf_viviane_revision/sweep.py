import os, re

d = r'C:\mysystems\projects\b3-econophysics-ai\article\overleaf_viviane_revision\sections'
files = ['introduction.tex', 'related_work.tex', 'data.tex', 'methodology.tex', 
         'results_stylized_correlation.tex', 'results_rmt.tex', 'results_clustering.tex', 
         'results_networks.tex', 'results_subsector_network.tex', 'results_forecasting.tex', 
         'discussion.tex', 'limitations.tex', 'conclusion.tex']

all_text = ""
for f in files:
    with open(os.path.join(d, f), 'r', encoding='utf-8') as file:
        all_text += f"\n--- FILE: {f} ---\n"
        all_text += file.read()

# 1. Acronyms Check (looking at first mention)
acronyms = ['RMT', 'PMFG', 'MST', 'HAR-RV']
print("=== ACRONYMS ===")
for ac in acronyms:
    match = re.search(r'.{0,50}\b' + ac + r'\b.{0,50}', all_text)
    if match:
        print(f"First mention of {ac}: ...{match.group(0).strip()}...")

# 2. Figure and Table Citations Order
print("\n=== FIGURES & TABLES CITATION ORDER ===")
figs_cited = []
tabs_cited = []
for m in re.finditer(r'\\ref\{(fig:[^}]+|tab:[^}]+)\}', all_text):
    ref = m.group(1)
    if ref.startswith('fig:') and ref not in figs_cited:
        figs_cited.append(ref)
    elif ref.startswith('tab:') and ref not in tabs_cited:
        tabs_cited.append(ref)

print("Order of Figure citations in text:", figs_cited)
print("Order of Table citations in text:", tabs_cited)

# Check actual labels defined
labels = re.findall(r'\\label\{(fig:[^}]+|tab:[^}]+)\}', all_text)
print("Labels defined in files:", [l for l in labels if not l.startswith('sec:')])

# 3. Long sentences check (>40 words)
print("\n=== LONG SENTENCES (>40 words) ===")
# Remove LaTeX commands for cleaner word count (very basic heuristic)
clean_text = re.sub(r'\\[a-zA-Z]+\{.*?\}', 'X', all_text)
sentences = re.split(r'(?<=[.!?])\s+', clean_text)
long_sentences = [s.strip() for s in sentences if len(s.split()) > 40 and "--- FILE" not in s]
print(f"Found {len(long_sentences)} sentences with >40 words. Examples:")
for s in long_sentences[:5]:
    print(f" - [{len(s.split())} words]: {s[:100]}...")

