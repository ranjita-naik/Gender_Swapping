# Gender Swapping
This repo can be used to perform simple gender swapping on english text. 

## Setup
```
$conda create -n gender_swap python=3.6
$conda activate gender_swap
$pip install spacy==2.2.2 spacy-conll==2.0.0 spacy-stanza==0.2.4 pyconll

```
## Usage
```
$python .\text_to_conllu.py --in_file .\test\test.txt --out_file .\test\test.conll 
$python .\gender_swapping.py --in_file .\test\test.conll  --out_file .\test\test_swapped.conll
$python .\conll_to_text.py --in_file .\test\test_swapped.conll  --out_dir C:\Gender_Swapping\test   

```
