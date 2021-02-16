#!/bin/sh

scripts/get-models.sh

DATADIR=models

wget http://dl.turkunlp.org/turku-ner-models/combined-ext-model-130220.tar.gz -O $DATADIR/combined-ext-model-130220.tar.gz

tar -xzvf $DATADIR/combined-ext-model-130220.tar.gz -C $DATADIR
rm $DATADIR/combined-ext-model-130220.tar.gz