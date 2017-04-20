#!/bin/bash
docker build -t   epc_base:SNAPSHOT  -f Dockerfile.base .
docker build -t   hss:v3  -f Dockerfile.hss .
docker build -t   mme:v3  -f Dockerfile.mme .
docker build -t   sgw:v3  -f Dockerfile.sgw .
docker build -t   pgw:v3  -f Dockerfile.pgw . 
docker build -t   sink:v3  -f Dockerfile.sink . 

