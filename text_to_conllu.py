import argparse
from spacy_conll import init_parser
from spacy_stanza import StanzaLanguage
import stanza
stanza.download('en')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--in_file', required=True,
                        help='Input conllu file')
    parser.add_argument('--out_file', required=True,
                        help='Output conllu file')
    opt = parser.parse_args()

    # Initialise English parser, already including the ConllFormatter as a pipeline component.
    # Indicate that we want to get the CoNLL headers in the string output.
    # `use_gpu` and `verbose` are specific to stanza (and stanfordnlp). These keywords arguments
    # are passed onto their Pipeline() initialisation
    nlp = init_parser("stanza",
                      "en",
                      parser_opts={"use_gpu": True, "verbose": False},
                      # This was to prevent splitting "it's" into "it" and "'s"
                      # But it resulted in incorrect xpos - PRP/PRP$
                      # So I handle the contractions in utils.data get_sentence_text
                      # disable_sbd=True,
                      # is_tokenized=True,
                      include_headers=True)

    in_file = open(opt.in_file, "r", encoding="utf-8")
    out_file = open(opt.out_file, "w", encoding="utf-8")

    for line in in_file:
        # Parse a given sentnece
        doc = nlp(line.strip())

        # Get the CoNLL representation of the whole document, including headers
        conll = doc._.conll_str

        out_file.write(conll + "\n")

    in_file.close()
    out_file.close()
