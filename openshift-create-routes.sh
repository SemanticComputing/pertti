#!/bin/sh

oc create route edge --hostname 'finbert-ner.nlp.ldf.fi' --insecure-policy 'Allow' --service 'production-finbert-ner' finbert-ner.nlp.ldf.fi
oc label route --overwrite 'finbert-ner.nlp.ldf.fi' 'app=finbert-ner' 'environment=production'
oc annotate route 'finbert-ner.nlp.ldf.fi' --overwrite haproxy.router.openshift.io/timeout=300s