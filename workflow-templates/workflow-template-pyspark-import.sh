#!/bin/bash

bucket="gs://sids-bucket"
template_name="spark-mysql-import"
cluster_name="spark-cluster"
instance_name="streaming-practice-228618:us-central1:test-instance"
table_name="customers"
spark_file_path="spark-cloudsql/export_tables.py"

# gsutil rm -r $bucket/$table_name/

# gcloud dataproc workflow-templates delete -q $template_name  && 

gcloud beta dataproc workflow-templates create $template_name &&

gcloud beta dataproc workflow-templates set-managed-cluster $template_name \
 --zone "us-east1-b" --cluster-name=$cluster_name \
 --scopes=default,sql-admin \
 --initialization-actions=gs://dataproc-initialization-actions/cloud-sql-proxy/cloud-sql-proxy.sh \
 --properties=hive:hive.metastore.warehouse.dir=$bucket/hive-warehouse \
 --metadata=enable-cloud-sql-hive-metastore=false \
 --metadata=additional-cloud-sql-instances=$instance_name=tcp:3307 \
 --master-machine-type n1-standard-1 \
 --master-boot-disk-size 20 \
 --num-workers 2 \
 --worker-machine-type n1-standard-2 \
 --worker-boot-disk-size 20 \
 --image-version 1.3 &&

gcloud beta dataproc workflow-templates \
add-job pyspark $bucket/$spark_file_path \
--step-id=test123 \
--workflow-template=$template_name && 

gcloud beta dataproc workflow-templates instantiate $template_name
