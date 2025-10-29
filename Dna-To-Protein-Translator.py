# Single-file script: demonstrates translation, mutation simulation, codon usage table and plot. 
# # This cell will run a demo using a sample DNA sequence.

import random
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt

CODON_TABLE = {
    'TTT':'F','TTC':'F','TTA':'L','TTG':'L','CTT':'L','CTC':'L','CTA':'L','CTG':'L',
    'ATT':'I','ATC':'I','ATA':'I','ATG':'M','GTT':'V','GTC':'V','GTA':'V','GTG':'V',
    'TCT':'S','TCC':'S','TCA':'S','TCG':'S','CCT':'P','CCC':'P','CCA':'P','CCG':'P',
    'ACT':'T','ACC':'T','ACA':'T','ACG':'T','GCT':'A','GCC':'A','GCA':'A','GCG':'A',
    'TAT':'Y','TAC':'Y','TAA':'*','TAG':'*','CAT':'H','CAC':'H','CAA':'Q','CAG':'Q',
    'AAT':'N','AAC':'N','AAA':'K','AAG':'K','GAT':'D','GAC':'D','GAA':'E','GAG':'E',
    'TGT':'C','TGC':'C','TGA':'*','TGG':'W','CGT':'R','CGC':'R','CGA':'R','CGG':'R',
    'AGT':'S','AGC':'S','AGA':'R','AGG':'R','GGT':'G','GGC':'G','GGA':'G','GGG':'G'
}

def clean_dna(seq: str) -> str:
    seq = seq.upper().replace('U', 'T')
    return ''.join([c for c in seq if c in 'ACGT'])

def chunker(seq: str, size: int):
    for i in range(0, len(seq), size):
        yield seq[i:i+size]

def translate_dna(seq: str, frame: int = 0, to_stop: bool = False) -> str:
    seq = clean_dna(seq)
    prot = []
    for codon in chunker(seq[frame:], 3):
        if len(codon) < 3:
            break
        aa = CODON_TABLE.get(codon, 'X')
        if aa == '*':
            if to_stop: break
            else: prot.append('*')
        else:
            prot.append(aa)
    return ''.join(prot)

def find_orfs(seq: str, min_aa_len: int = 20):
    seq = clean_dna(seq)
    orfs = []
    for frame in (0,1,2):
        i = 0
        while i < len(seq[frame:])//3:
            codon = seq[frame + i*3: frame + i*3 + 3]
            aa = CODON_TABLE.get(codon, 'X')
            if aa == 'M':
                j = i
                prot = []
                stopped = False
                while j < len(seq[frame:])//3:
                    c = seq[frame + j*3: frame + j*3 + 3]
                    a = CODON_TABLE.get(c, 'X')
                    if a == '*':
                        stopped = True
                        end = frame + j*3 + 3
                        break
                    prot.append(a)
                    j += 1
                if not stopped:
                    end = frame + j*3 + 3
                aa_seq = ''.join(prot)
                if len(aa_seq) >= min_aa_len:
                    orfs.append((frame, frame + i*3, end, aa_seq))
                i = j+1
            else:
                i += 1
    return orfs

def simulate_point_mutations(seq: str, rate: float = 0.01, seed: int = None):
    if seed is not None: random.seed(seed)
    seq = list(clean_dna(seq))
    n = len(seq)
    mcount = max(1, int(round(n * rate))) if n>0 else 0
    positions = random.sample(range(n), mcount) if mcount <= n else list(range(n))
    mutations = []
    for pos in positions:
        orig = seq[pos]
        choices = [b for b in 'ACGT' if b != orig]
        new = random.choice(choices)
        seq[pos] = new
        mutations.append((pos, orig, new))
    return ''.join(seq), mutations

def codon_usage_table(seq: str, frame: int = 0):
    seq = clean_dna(seq)
    codons = [c for c in chunker(seq[frame:], 3) if len(c) == 3]
    counts = Counter(codons)
    all_codons = sorted(CODON_TABLE.keys())
    data = []
    total = sum(counts.values()) or 1
    for codon in all_codons:
        aa = CODON_TABLE[codon]
        cnt = counts.get(codon, 0)
        data.append((codon, aa, cnt, cnt/total))
    df = pd.DataFrame(data, columns=['codon','aa','count','freq']).sort_values('count', ascending=False).reset_index(drop=True)
    return df

def plot_codon_usage(df, top_n=20, title='Codon usage (top N)'):
    top = df.head(top_n)
    fig, ax = plt.subplots(figsize=(10,4))
    ax.bar(top['codon'], top['count'])
    ax.set_xlabel('Codon')
    ax.set_ylabel('Count')
    ax.set_title(title)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

sample_seq = "ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG"
print("Sample DNA:", sample_seq)
print("Cleaned DNA:", clean_dna(sample_seq))

for f in (0,1,2):
    print(f"Frame {f} translation:", translate_dna(sample_seq, frame=f, to_stop=False))

print("Frame 0 (to_stop=True):", translate_dna(sample_seq, frame=0, to_stop=True))

mut_seq, muts = simulate_point_mutations(sample_seq, rate=0.08, seed=42)
print("\nSimulated mutations (sample):", muts)
print("Mutated DNA:", mut_seq)
print("Translation original:", translate_dna(sample_seq))
print("Translation mutated :", translate_dna(mut_seq))

df_usage = codon_usage_table(sample_seq, frame=0)
print("\nTop codons in sample (table):")
print(df_usage.head(12))

plot_codon_usage(df_usage, top_n=12, title='Sample codon usage (top 12)')
