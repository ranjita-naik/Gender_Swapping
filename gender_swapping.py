import argparse
from copy import deepcopy
from tqdm import tqdm
from utils.conll import load_sentences, change_line

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--in_file', required=True,
                        help='Input conllu file')
    parser.add_argument('--out_file', required=True,
                        help='Output conllu file')
    opt = parser.parse_args()

    # generalized_swaps.txt and extra_gendered_words.txt
    # are borrowed from https://github.com/uclanlp/corefBias
    swaps = open("swaps/generalized_swaps.txt").readlines()
    swap_dict = {}
    for line in swaps:
        tabs = line.split("\t")
        swap_dict[tabs[-2].strip()] = tabs[-1].strip()

    swaps = open("swaps/extra_gendered_words.txt").readlines()
    for line in swaps:
        tabs = line.split("\t")
        swap_dict[tabs[-2].strip()] = tabs[-1].strip()
        swap_dict[tabs[-1].strip()] = tabs[-2].strip()

    out_file = open(opt.out_file, "w", encoding="utf-8")
    with open(opt.in_file, "r", encoding="utf-8") as in_file:
        # Work in batches of 1000
        not_empty = True
        while not_empty:

            # Load sentences
            print("    Loading partition...")
            conll, not_empty = load_sentences(1000, in_file)

            for sent in tqdm(conll, total=len(conll)):
                lines = []
                # for tok in sent:
                for i in range(len(sent)):
                    token = sent[i]

                    w = token.form
                    q = token.form.lower()
                    swap = None
                    if q in swap_dict:
                        swap = swap_dict[q]

                    # her/PRP him
                    # her/PRP$        his
                    if q == "her":
                        if token.xpos == "PRP":
                            swap = "him"
                        else:
                            swap = "his"

                    if swap is not None and w[0].isupper():
                        swap = swap[0].upper() + swap[1:]

                    if swap is not None:
                        swapped_token = change_line(token, swap)
                        lines.append(swapped_token)
                    else:
                        lines.append(token.conll())

                modified_conll = "\n".join(lines)
                out_file.write(modified_conll + "\n\n")

    in_file.close()
    out_file.close()
