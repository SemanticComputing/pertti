# pertti

Named entity recognition built on top of BERT and keras-bert. This guide is updated version from the original one: https://github.com/jouniluoma/keras-bert-ner

The service is a compilation from [J. Luoma's](https://github.com/jouniluoma/keras-bert-ner) and [S. Pyysalo's](https://github.com/spyysalo/tagdemo) original demos.

## Dependencies:

Notice that this project uses tensorflow 1.11, make sure to downgrade tensorflow to use this project or use it in it's own sandbox. Some of the dependencies are added as a part of the installation.

Install the following dependencies preferably in the given order:

* python 3 or higher

* flask

* bert (added as submodule to this project. FullTokenizer is used instead of keras-bert tokenizer)

* keras-bert (https://pypi.org/project/keras-bert/)

Pretrained BERT model, e.g. from:
- https://github.com/TurkuNLP/FinBERT
- https://github.com/google-research/bert

input data e.g. from:
- https://github.com/mpsilfve/finer-data

Input data is expected to be in CONLL:ish format where Token and Tag are tab separated. 
First string on the line corresponds to Token and second string to Tag
  
## Quickstart

Get submodules

```
git submodule init
git submodule update
```

Get pretrained models and data

```
./scripts/get-models.sh
./scripts/get-finer.sh
./scripts/get-turku-ner.sh
```

Run an experiment on FiNER news data

```
./scripts/run-finer-news.sh
```

Start the pertti-service (notice that the --ner\_model\_dir parameter can be changed)
```
python serve.py --ner_model_dir finer-news-model/
```

All options to run the service are:
* -h, --help (help)
* --batch\_size (Batch size for training)
* --output\_file (File to write predicted outputs to)
* --ner\_model\_dir (Trained NER model directory)


(the first job must finish before running the second.)
