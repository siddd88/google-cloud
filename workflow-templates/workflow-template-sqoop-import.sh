#!/bin/bash

bucket="gs://your-bucket-url"
template_name="mysql-test-import" #Any name for the template
cluster_name = "sqoop-import" # Any name for your cluster
instance_name = "your_cloudsql_instance_name" 

gcloud dataproc workflow-templates delete -q $template_name  &&

gcloud beta dataproc workflow-templates create $template_name &&

gcloud beta dataproc workflow-templates set-managed-cluster $template_name --zone "us-east1-b" \
--cluster-name=$cluster_name \
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
--image-version 1.2 &&

gcloud beta dataproc workflow-templates add-job hadoop \
--step-id=customers_201901 \
--workflow-template=$template_name \
--class=org.apache.sqoop.Sqoop \
--jars=$bucket/sqoop_sqoop-1.4.7.jar,$bucket/sqoop_avro-tools-1.8.2.jar,\
file:///usr/share/java/mysql-connector-java-5.1.42.jar \
-- import -Dmapreduce.job.user.classpath.first=true \
--driver com.mysql.jdbc.Driver \
--connect="jdbc:mysql://localhost:3307" \
--username=[your_username] --password=[your_pwd] \
--query "select * from classicmodels.customers where customerNumber>0 and \$CONDITIONS" \
--target-dir $bucket/customers \
--split-by customerNumber -m 2 && 

gcloud beta dataproc workflow-templates instantiate $template_name
