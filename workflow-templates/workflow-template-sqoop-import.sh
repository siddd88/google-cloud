#!/bin/bash

bucket="gs://your-bucket"


gcloud dataproc workflow-templates delete -q mysql-test-import  &&

gcloud beta dataproc workflow-templates create mysql-test-import &&

gcloud beta dataproc workflow-templates set-managed-cluster mysql-test-import --zone "us-east1-b" --cluster-name=sqoop-import \
 --scopes=default,sql-admin --initialization-actions=gs://dataproc-initialization-actions/cloud-sql-proxy/cloud-sql-proxy.sh \
 --properties=hive:hive.metastore.warehouse.dir=gs://staging.streaming-practice-228618.appspot.com/hive-warehouse \
 --metadata=enable-cloud-sql-hive-metastore=false \
 --metadata=additional-cloud-sql-instances=streaming-practice-228618:us-central1:test-instance=tcp:3307 \
 --master-machine-type n1-standard-1 --master-boot-disk-size 20 \
--num-workers 2 \
--worker-machine-type n1-standard-1 --worker-boot-disk-size 20 \
--image-version 1.3 &&

gcloud beta dataproc workflow-templates add-job hadoop --step-id=test_201901 --workflow-template=mysql-test-import \
--class=org.apache.sqoop.Sqoop \
--jars=$bucket/sqoop_sqoop-1.4.7.jar,$bucket/sqoop_avro-tools-1.8.2.jar,\
file:///usr/share/java/mysql-connector-java-5.1.42.jar \
-- import -Dmapreduce.job.user.classpath.first=true \
--driver com.mysql.jdbc.Driver \
--connect="jdbc:mysql://localhost:3307" \
--username=[your_cloudsql_instance_username] --password=[your_cloudsql_instance_pwd] \
--query "select * from classicmodels.customers where customerNumber>0 and \$CONDITIONS" \
--target-dir $bucket/customers \
--split-by customerNumber -m 2 && 

gcloud beta dataproc workflow-templates instantiate mysql-test-import 

#bq load --allow_quoted_newlines --allow_jagged_rows --quote "" -E UTF-8 --field_delimiter \t --source_format=CSV $project_name:$dataset_name.transaction "$bucket/transactions/part-*"

#jdbc:mysql://35.184.232.190/wms