#!/bin/bash

bucket="gs://your-bucket"


gcloud dataproc workflow-templates delete -q pyspark-import  && 

gcloud beta dataproc workflow-templates create pyspark-import &&

gcloud beta dataproc workflow-templates set-managed-cluster pyspark-import --zone "us-east1-b" --cluster-name=spark-cloudsql \
 --scopes=default,sql-admin --initialization-actions=gs://dataproc-initialization-actions/cloud-sql-proxy/cloud-sql-proxy.sh \
 --properties=hive:hive.metastore.warehouse.dir=gs://staging.streaming-practice-228618.appspot.com/hive-warehouse \
 --metadata=enable-cloud-sql-hive-metastore=false \
 --metadata=additional-cloud-sql-instances=streaming-practice-228618:us-central1:test-instance=tcp:3307 \
 --master-machine-type n1-standard-1 --master-boot-disk-size 20 \
--num-workers 2 \
--worker-machine-type n1-standard-2 --worker-boot-disk-size 20 \
--image-version 1.3 &&

gcloud beta dataproc workflow-templates add-job pyspark $bucket/spark-cloudsql/export_all_tables.py --step-id=test123 --workflow-template=pyspark-import && 

gcloud beta dataproc workflow-templates instantiate pyspark-import