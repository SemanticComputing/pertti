# pertti

Named entity recognition built on top of BERT and keras-bert. This guide is updated version from the original one: https://github.com/jouniluoma/keras-bert-ner

The service is a compilation from [J. Luoma's](https://github.com/jouniluoma/keras-bert-ner) and [S. Pyysalo's](https://github.com/spyysalo/tagdemo) original demos.

## Dependencies:

Notice that this project uses tensorflow 1.11 (also install tensorflow-gpu: pip install tensorflow-gpu==1.14), make sure to downgrade tensorflow to use this project or use it in it's own sandbox. Some of the dependencies are added as a part of the installation.

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

Experiment on Turku NER corpus data (`run-turku-ner.sh` trains, `predict-turku-ner.sh` outputs predictions)

```
./scripts/run-turku-ner.sh
./scripts/predict-turku-ner.sh
python compare.py data/turku-ner/test.tsv turku-ner-predictions.tsv 
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


#### Request where output is given in raw format

Request:
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


#### Request where output is given in JSON format

In this output format the JSON returns in addition to the named entities and their types, also their locations in the given text.

Request:
```
 http://127.0.0.1:8080?text=Presidentti Tarja Halosen elämän ääniraitaan mahtuu muistoja työskentelystä Englannissa, Tapio Rautavaaran Halosen äidille kohdistamista kosiskeluyrityksistä, sekä omista häistään.&format=json
```

Output:

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

## Docker

For building the Docker container image, be sure to have the submodule `bert` fetched:

```
git submodule init
git submodule update
```

### Option 1: self-contained Docker image including language models and NER models trained on `finer-news`, `turku-ner`, and `combined`

Build:
`docker build -f Dockerfile.self-contained -t pertti-self-contained .`

Run:
`docker run -it --rm -p 5000:5000 --name pertti pertti-self-contained [NER_MODEL]`

where NER_MODEL = `combined` (default), `finer-news`, or `turku-ner`

### Option 2: smaller Docker image without pretrained language and NER models

For running the container, you need to have the existing language models and a NER model on the host machine, and pass them to container as a bind mount or on a volume.

E.g. download and unpack the following model distributions and create the following directory structure for them on mount/volume:

* models/multi_cased_L-12_H-768_A-12: https://storage.googleapis.com/bert_models/2018_11_23/multi_cased_L-12_H-768_A-12.zip
* models/multilingual_L-12_H-768_A-12: https://storage.googleapis.com/bert_models/2018_11_03/multilingual_L-12_H-768_A-12.zip
* models/bert-base-finnish-cased-v1: http://dl.turkunlp.org/finbert/bert-base-finnish-cased-v1.zip
* models/bert-base-finnish-uncased-v1: http://dl.turkunlp.org/finbert/bert-base-finnish-uncased-v1.zip
* models/combined-ext-model: http://dl.turkunlp.org/turku-ner-models/combined-ext-model-130220.tar.gz (or one of the models at https://version.aalto.fi/gitlab/seco/finbert-ner-models.git; or use your own NER model trained with the instructions in section `Train NER model`)

You can run the script `./get-models.sh` to download the models (language models and the combined NER model based on FiNER news and Turku NER corpus) into directory `models`.

Build:
`docker build -t pertti .`

Run:
`docker run -it --rm -p 5000:5000 --mount type=bind,source="$(pwd)"/models,target=/app/models -e NER_MODEL_DIR=/app/models/combined-ext-model --name pertti pertti`

The service listens on http://localhost:5000

### Train NER model

To train a NER model:

Build:

`docker build -f Dockerfile.train -t pertti-train .`

Run:

E.g. train a model using FiNER news corpus:

`mkdir finer-ner-model`
`docker run -it --rm --cpus=4 --mount type=bind,source="$(pwd)"/finer-ner-model,target=/app/finer-news-model --name pertti-train pertti-train /bin/bash -c "./scripts/get-models.sh && ./scripts/get-finer.sh && ./scripts/run-finer-news.sh"`

E.g. train a model using Turku NER corpus:

`mkdir ner-models`
`docker run -it --rm --cpus=4 --mount type=bind,source="$(pwd)"/ner-models,target=/app/ner-models --name pertti-train pertti-train /bin/bash -c "./scripts/get-models.sh && ./scripts/get-turku-ner.sh && ./scripts/run-turku-ner.sh"`
`mv ner-models/turku-ner-model .`

E.g. train a model using combined FiNER news and Turku NER corpus:

`mkdir combined-ner-model`
`docker run -it --rm --cpus=4 --mount type=bind,source="$(pwd)"/combined-ner-model,target=/app/combined-model --name pertti-train pertti-train /bin/bash -c "./scripts/get-models.sh && ./scripts/get-combined.sh && ./scripts/run-combined.sh"`

You can also download the language models and NER model training data on your host machine and pass them to container as a bind mount or on a volume. In such case, you only need to run in the container the last command of the above docker run examples, e.g., `./scripts/run-combined.sh`.
