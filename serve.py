# -*- coding: utf-8 -*-

import os
import sys
import unicodedata

from flask import Flask, request, jsonify

import numpy as np
import tensorflow as tf

from common import process_sentences, load_ner_model
from common import encode, write_result
from common import argument_parser

from so2html import conll_to_standoff, standoff_to_html, generate_legend
from so2html import sort_types

app = Flask(__name__)


@app.route('/')
def tag():
    format_ = str(request.values.get('format', 'html'))
    text = request.values['text']
    annotated = app.tagger.tag(text)
    annotations = conll_to_standoff(text, annotated)
    print("Format", format_)
    if format_ == 'json':
        anns = [a.to_dict(text) for a in annotations]
        return jsonify(anns)
    else:
        return annotated


class Tagger(object):
    def __init__(self, model, tokenizer, labels, config):
        self.model = model
        self.tokenizer = tokenizer
        self.labels = labels
        self.config = config
        self.session = None
        self.graph = None

    def tag(self, text):
        max_seq_len = self.config['max_seq_length']
        inv_label_map = { i: l for i, l in enumerate(self.labels) }
        words = tokenize(text)
        dummy = ['O'] * len(words)
        data = process_sentences([words], [dummy], self.tokenizer, max_seq_len)
        x = encode(data.combined_tokens, self.tokenizer, max_seq_len)
        if self.session is None or self.graph is None:
            probs = self.model.predict(x, batch_size=8)    # assume singlethreaded
        else:
            with self.session.as_default():
                with self.graph.as_default():
                    probs = self.model.predict(x, batch_size=8)
        preds = np.argmax(probs, axis=-1)
        pred_labels = []
        for i, pred in enumerate(preds):
            pred_labels.append([inv_label_map[t]
                                for t in pred[1:len(data.tokens[i])+1]])
        lines = write_result(
            'output.tsv', data.words, data.lengths,
            data.tokens, data.labels, pred_labels, mode='predict'
        )
        return ''.join(lines)

    @classmethod
    def load(cls, model_dir):
        # session/graph for multithreading, see https://stackoverflow.com/a/54783311
        session = tf.Session()
        graph = tf.get_default_graph()
        with graph.as_default():
            with session.as_default():
                model, tokenizer, labels, config = load_ner_model(model_dir)
                tagger = cls(model, tokenizer, labels, config)
                tagger.session = session
                tagger.graph = graph
        return tagger


punct_chars = set([
    chr(i) for i in range(sys.maxunicode)
    if (unicodedata.category(chr(i)).startswith('P') or
        ((i >= 33 and i <= 47) or (i >= 58 and i <= 64) or
         (i >= 91 and i <= 96) or (i >= 123 and i <= 126)))
])

translation_table = str.maketrans({ c: ' '+c+' ' for c in punct_chars })


def tokenize(text):
    return text.translate(translation_table).split()

def setup(ner_model_dir):
    app.tagger = Tagger.load(ner_model_dir)
    return app

def main(argv):
    print("Load tagger")
    argparser = argument_parser('serve')
    args = argparser.parse_args(argv[1:])
    setup(args.ner_model_dir)
    app.run(port=8080)
    return 0


if __name__ == '__main__':
    print("TESTING")
    sys.exit(main(sys.argv))
