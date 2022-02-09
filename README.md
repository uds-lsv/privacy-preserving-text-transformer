## [Privacy Preserving Text Transformer](https://arxiv.org/abs/2008.03101)

This repository contains the link to our privacy preserving text transformer implementation, an approach to automatically replace sensitive named entities with an alternative of this same named entity type selected randomly from the corpus. 

### Code:
Visit the [official Gitlab](https://gitlab.inria.fr/comprise/text_transformer) of the COMPRISE H2020 project. 

### Data

We also release the humanly annotated VerbMobil NER dataset (in the spoken dialog domain) used in our Interspeech paper to encourage more research in this area. Since the VerbMobil is not freely available, we release a some scripts that can be used to automatically align the tags with words in the original corpus if it is bought.  The [tags](https://github.com/uds-lsv/privacy-preserving-text-transformer/data/verbmobil-tags/) can be found 

* python scripts
  * clean_verbmobil_utt.py : to automatically extract dialog files of VM6.1, VM8.1, VM13.1, VM23.1, VM28.1, VM31.1, VM42.1, VM43.1, VM50.1, and remove unused tags. This generates a directory "data/VerbMobil_cleaned"

  * export_unannotated_texts.py: extract the utterance per dialog into a conll format. This generates a directory "data/VerbMobil_per_dialog" with tokens in each dialog file arranged vertically (CONLL format)

  * extract_annotated_tags.py : automatically compares annotated [tags](https://github.com/uds-lsv/privacy-preserving-text-transformer/data/verbmobil-tags/) and preprocessed words in "data/VerbMobil_per_dialog", and output the annotated corpus in the CoNLL format. 



If you use the code or data, please cite

### BibTeX entry and citation info
```
@inproceedings{adelani:hal-02907939,
  TITLE = {{Privacy guarantees for de-identifying text transformations}},
  AUTHOR = {Adelani, David Ifeoluwa and Davody, Ali and Kleinbauer, Thomas and Klakow, Dietrich},
  URL = {https://hal.inria.fr/hal-02907939},
  BOOKTITLE = {{INTERSPEECH 2020}},
  ADDRESS = {Shanghai, China},
  YEAR = {2020},
  MONTH = Oct,
  KEYWORDS = {Differential privacy ; Spoken language understanding ; Named entity recognition ; Intent detection},
  PDF = {https://hal.inria.fr/hal-02907939/file/adelani_IS20.pdf},
  HAL_ID = {hal-02907939},
  HAL_VERSION = {v1},
}

```
