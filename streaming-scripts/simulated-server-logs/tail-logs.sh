#!/bin/bash

filename=$1
portnumber=$2

tail -f $filename | nc -l $portnumber
