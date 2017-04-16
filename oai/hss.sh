#!/bin/bash

service mysql restart
son-vm-server -c server.conf -v
