#!/bin/bash

# Get combined FiNER news and Turku NER data (https://github.com/TurkuNLP/turku-ner-corpus/tree/development)

# https://stackoverflow.com/a/246128
SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

set -euo pipefail

DATADIR="$SCRIPTDIR/../data"

mkdir -p "$DATADIR"

combineddir="$DATADIR/combined-data"
if [ -e "$DATADIR/combined-data" ]; then
    echo "$combineddir exists, not cloning again"
else
    cd "$DATADIR"
    git clone -b development "https://github.com/TurkuNLP/turku-ner-corpus.git" combined-data
    cd "$combineddir"
    git checkout 34f921b 2>/dev/null    # Make sure we have the right version
fi