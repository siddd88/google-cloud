import time
import datetime
import pytz
import numpy
import random
import gzip
import zipfile
import sys
import argparse
from faker import Faker
from random import randrange
from tzlocal import get_localzone
local = get_localzone()
import csv
import sys 
import time 

faker = Faker()

from google.cloud import storage


response=["200","404","500","301"]

verb=["GET","POST","DELETE","PUT"]

resources=["/list","/wp-content","/wp-admin","/explore","/search/tag/list","/app/main/posts","/posts/posts/explore","/apps/cart.jsp?appID="]

ualist = [faker.firefox, faker.chrome, faker.safari, faker.internet_explorer, faker.opera]


def upload_to_bucket(blob_name, path_to_file, bucket_name):
    
    storage_client = storage.Client.from_service_account_json('creds.json')

    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(path_to_file)
    return blob.public_url


flag= True 
while flag : 
    timestr = time.strftime("%Y%m%d-%H%M%S")
    data = list() 
    for i in range(100) : 
        otime = datetime.datetime.now()
        increment = datetime.timedelta(seconds=random.randint(30, 300))
        otime += increment
        ip = faker.ipv4()
        dt = otime.strftime('%d/%b/%Y:%H:%M:%S')
        tz = datetime.datetime.now(local).strftime('%z')
        vrb = numpy.random.choice(verb,p=[0.6,0.1,0.1,0.2])
        uri = random.choice(resources)
        if uri.find("apps")>0:
            uri += str(random.randint(1000,10000))

        resp = numpy.random.choice(response,p=[0.9,0.04,0.02,0.04])
        byt = int(random.gauss(5000,50))
        referer = faker.uri()
        useragent = numpy.random.choice(ualist,p=[0.5,0.3,0.1,0.05,0.05] )()
        tup =(ip,dt,tz,vrb,uri,resp,byt,referer,useragent)
        data.append(tup)
        if i == 99:
            break


    kwargs = {'newline': ''}
    mode = 'w'
    if sys.version_info < (3, 0):
        kwargs.pop('newline', None)
        mode = 'wb'
    
    with open('csvs/server-logs-'+timestr+'.csv', mode, **kwargs) as fp:
        writer = csv.writer(fp, delimiter=',')
        writer.writerows(data)

    filename = 'server-logs-'+timestr+'.csv'
    blob_name = "streaming-files/"+filename
    bucket = "sid-data"

    upload_to_bucket(blob_name,"csvs/"+filename,bucket)

    time.sleep(5)
