#!/bin/sh

docker run -it --rm -p 5000:5000 --mount type=bind,source="$(pwd)"/ner-model,target=/app/ner-model --name pertti pertti