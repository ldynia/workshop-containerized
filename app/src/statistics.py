"""
author: Lukasz Dynowski
email: ludd@cbs.dtu.dk
licence: MIT
"""

class Statistic():
    """
    Example: fsa-analyzer data/dna.fsa | python -m json.tool
    """
    CODONS = [
        'ATT', 'ATC', 'ATA', 'CTT',
        'CTC', 'CTA', 'CTG', 'TTA',
        'TTG', 'GTT', 'GTC', 'GTA',
        'GTG', 'TTT', 'TTC', 'ATG',
        'TGT', 'TGC', 'GCT', 'GCC',
        'GCA', 'GCG', 'GGT', 'GGC',
        'GGA', 'GGG', 'CCT', 'CCC',
        'CCA', 'CCG', 'ACT', 'ACC',
        'ACA', 'ACG', 'TCT', 'TCC',
        'TCA', 'TCG', 'AGT', 'AGC',
        'TAT', 'TAC', 'TGG', 'CAA',
        'CAG', 'AAT', 'AAC', 'CAT',
        'CAC', 'GAA', 'GAG', 'GAT',
        'GAC', 'AAA', 'AAG', 'CGT',
        'CGC', 'CGA', 'CGG', 'AGA',
        'AGG', 'TAA', 'TAG', 'TGA',
    ]

    def __init__(self, data_file):
        self.data_file = data_file

    def __del__(self):
        self.data_file.close()

    def count_nucleotides(self):
        results = {}
        self.data_file.seek(0)
        for line in self.data_file:
            line = line.strip('\n')
            if not line.startswith('>'):
                for letter in line.strip('\n'):
                    if letter not in results:
                        results[letter] = 0
                    results[letter] += 1
        return results

    def count_codons(self):
        results = dict.fromkeys(Statistic.CODONS, 0)
        self.data_file.seek(0)
        for line in self.data_file:
            line = line.strip('\n')
            if not line.startswith('>'):
                for start_index in range(0, len(line), 3):
                    stop_index = start_index + 3
                    codon = line[start_index:stop_index]
                    if codon in Statistic.CODONS:
                        results[codon] += 1
        return results
