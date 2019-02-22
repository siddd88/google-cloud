"""Import a json file into BigQuery."""

import logging
import os
import re

from google.cloud import bigquery

GCP_PROJECT = os.environ.get('GCP_PROJECT')

def gcs_to_bq_autodetect(data,context) :   

    client = bigquery.Client()
    bucketname = data['bucket']
    filename = data['name']
    timeCreated = data['timeCreated']
    dataset_id = "test_dataset"

    dataset_ref = client.dataset(dataset_id)
    job_config = bigquery.LoadJobConfig()
    # job_config.schema = [
    #     bigquery.SchemaField('unique_key', 'STRING'),
    #     bigquery.SchemaField('address', 'STRING'),
    #     bigquery.SchemaField('clearance_date', 'STRING'),
    #     bigquery.SchemaField('clearance_status', 'STRING'),
    #     bigquery.SchemaField('description', 'STRING'),
    #     bigquery.SchemaField('district', 'STRING'),
    #     bigquery.SchemaField('primary_type', 'STRING'),
    #     bigquery.SchemaField('timestamp', 'STRING'),
    #     bigquery.SchemaField('year', 'STRING')
    # ]
    #job_config.autodetect = True
    job_config.ignoreUnknownValues = True
    job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
    job_config.maxBadRecords = 10000

    uri = 'gs://%s/%s' % (bucketname, filename)
    

    load_job = client.load_table_from_uri(
        uri,
        dataset_ref.table('crime'),
        job_config=job_config)  # API request
    print('Starting job {}'.format(load_job.job_id))

    load_job.result()  # Waits for table load to complete.
    print('Job finished.')

    destination_table = client.get_table(dataset_ref.table('crime'))
    print('Loaded {} rows.'.format(destination_table.num_rows))

def gcs_to_bq_csv(data,context) :   

    client = bigquery.Client()
    bucketname = data['bucket']
    filename = data['name']
    timeCreated = data['timeCreated']
    dataset_id = "test_dataset"

    dataset_ref = client.dataset(dataset_id)
    job_config = bigquery.LoadJobConfig()
  
    job_config.autodetect = True
    job_config.ignoreUnknownValues = True
    job_config.source_format = bigquery.SourceFormat.CSV
    job_config.maxBadRecords = 10000

    uri = 'gs://%s/%s' % (bucketname, filename)
    

    load_job = client.load_table_from_uri(
        uri,
        dataset_ref.table('cms_codes'),
        job_config=job_config)  # API request
    print('Starting job {}'.format(load_job.job_id))

    load_job.result()
    print('Job finished.')

    destination_table = client.get_table(dataset_ref.table('cms_codes'))
    print('Loaded {} rows.'.format(destination_table.num_rows))

def bigqueryImport(data, context):
    """Import a json file into BigQuery."""
    # get storage update data
    bucketname = data['bucket']
    filename = data['name']
    timeCreated = data['timeCreated']

    # check filename format - dataset_name/table_name.json
    # if not re.search('^[a-z_]+/[a-z_]+.json$', filename):
    #     logging.error('Unrecognized filename format: %s' % (filename))
    #     return

    # parse filename
    #datasetname, tablename = filename.replace('.json', '').split('/')
    datasetname = "test_dataset"
    tablename = "crime"
    table_id = '%s.%s.%s' % (GCP_PROJECT,"test_dataset","crime")

    # log the receipt of the file
    uri = 'gs://%s/%s' % (bucketname, filename)
    print('Received file "%s" at %s.' % (
        uri,
        timeCreated
    ))

    # create bigquery client
    client = bigquery.Client()

    # get dataset reference
    dataset_ref = client.dataset(datasetname)

    # check if dataset exists, otherwise create
    try:
        client.get_dataset(dataset_ref)
    except Exception:
        logging.warn('Creating dataset: %s' % (datasetname))
        client.create_dataset(dataset_ref)

    # create a bigquery load job config
    job_config = bigquery.LoadJobConfig()
    job_config.schema = [
        bigquery.SchemaField('unique_key', 'STRING'),
        bigquery.SchemaField('address', 'STRING'),
        bigquery.SchemaField('clearance_date', 'STRING'),
        bigquery.SchemaField('clearance_status', 'STRING'),
        bigquery.SchemaField('description', 'STRING'),
        bigquery.SchemaField('district', 'STRING'),
        bigquery.SchemaField('primary_type', 'STRING'),
        bigquery.SchemaField('timestamp', 'STRING'),
        bigquery.SchemaField('year', 'STRING')
    ]
    job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
    # job_config.autodetect = True
    # job_config.create_disposition = 'CREATE_IF_NEEDED',
    # job_config.source_format = 'NEWLINE_DELIMITED_JSON',
    # job_config.write_disposition = 'WRITE_TRUNCATE',

    load_job = client.load_table_from_uri(uri,dataset_ref.table('crime'),job_config=job_config)
    print('Starting job {}'.format(load_job.job_id))
    load_job.result()
    destination_table = client.get_table(dataset_ref.table('crime'))
    print('Loaded {} rows.'.format(destination_table.num_rows))

    # try:
    #     load_job = client.load_table_from_uri(
    #         uri,
    #         table_id,
    #         job_config=job_config,
    #     )
    #     print('Load job: %s [%s]' % (
    #         load_job.job_id,
    #         table_id
    #     ))
    # except Exception as e:
    #     logging.error('Failed to create load job: %s' % (e))
