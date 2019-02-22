#!/bin/sh

FUNCTION="bigqueryImport"
PROJECT="streaming-practice-228618"
BUCKET="cloud-funcs-test"

# set the gcloud project
#gcloud config set project ${PROJECT}

gcloud functions deploy gcs_to_bq_csv \
    --runtime python37 \
    --trigger-resource ${BUCKET} \
    --trigger-event google.storage.object.finalize
