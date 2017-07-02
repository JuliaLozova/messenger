#!/bin/bash
echo $1 | netcat -lk 127.0.0.1 50007
