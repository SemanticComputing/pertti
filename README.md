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

## Usage

The service will by default use the url: http://127.0.0.1:8080 and accepts currently only get requests.

In order to do Named Entity Recognition with the service, use the following parameters with the request:
* text (required): the text to be annotated with named entities
* format (optional): the format in which the results are returned. The service currently supports only json and raw output formats. To get output in JSON format the user must give this parameter value 'json'. By default without giving this option, the results are returned in raw format. 

### Example requests and their outputs

#### Example request where output is given in raw format

Request
```
 http://127.0.0.1:8080?text=Presidentti Tarja Halosen elämän ääniraitaan mahtuu muistoja työskentelystä Englannissa, Tapio Rautavaaran Halosen äidille kohdistamista kosiskeluyrityksistä, sekä omista häistään.
```

Output:
```
Presidentti	O
Tarja	B-PER
Halosen	I-PER
elämän	O
ääniraitaan	O
mahtuu	O
muistoja	O
työskentelystä	O
Englannissa	B-LOC
,	O
Tapio	B-PER
Rautavaaran	I-PER
Halosen	B-PER
äidille	O
kohdistamista	O
kosiskeluyrityksistä	O
,	O
sekä	O
omista	O
häistään	O
.	O
```


#### Example request where output is given in JSON format

In this output format the JSON returns in addition to the named entities and their types, also their locations in the given text.

Request
```
 http://127.0.0.1:8080?text=Presidentti Tarja Halosen elämän ääniraitaan mahtuu muistoja työskentelystä Englannissa, Tapio Rautavaaran Halosen äidille kohdistamista kosiskeluyrityksistä, sekä omista häistään.&format=json
```

Output

```
[
    {
        "end": 25,
        "start": 12,
        "text": "Tarja Halosen",
        "type": "PER"
    },
    {
        "end": 87,
        "start": 76,
        "text": "Englannissa",
        "type": "LOC"
    },
    {
        "end": 106,
        "start": 89,
        "text": "Tapio Rautavaaran",
        "type": "PER"
    },
    {
        "end": 114,
        "start": 107,
        "text": "Halosen",
        "type": "PER"
    }
]
```

