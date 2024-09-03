#!/bin/bash

perf stat -e instructions,cycles -a sleep 0.1