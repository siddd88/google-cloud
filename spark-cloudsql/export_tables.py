from pyspark import SparkContext, SparkConf, SQLContext
from pyspark.sql.types import StructType, StructField, StringType, FloatType

bucket_name = "gs://[your-bucket]"

bucket_path = bucket_name+"/classicmodels"

CLOUDSQL_INSTANCE_IP = 'localhost'
CLOUDSQL_DB_NAME = 'classicmodels'
CLOUDSQL_USER = '[your-username]'
CLOUDSQL_PWD  = '[your-cloudsql-instance-pwd]'

conf = SparkConf().setAppName("ETL-MYSQL")
sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)

jdbcDriver = 'com.mysql.jdbc.Driver'
jdbcUrl    = 'jdbc:mysql://%s:3307/%s?user=%s&password=%s' % (CLOUDSQL_INSTANCE_IP, CLOUDSQL_DB_NAME, CLOUDSQL_USER, CLOUDSQL_PWD)

# Read data from Cloud SQL

tables = list()

#import customers table 
customers = ('(select * from customers ) as t','customers')
tables.append(customers)


for table_qry in tables : 
	
	df_name = "df_"+table_qry[1]

	df_name = sqlContext.read.format('jdbc').options(driver=jdbcDriver,url=jdbcUrl, dbtable=table_qry[0], useSSL='false').load()

	df_name.coalesce(1).write.format('json').save(bucket_path+"/"+table_qry[1])
