#!/bin/bash

# Script que configura todos os routers da topologia deste trabalho

# r1
simple_switch_CLI --thrift-port 9090 < commands_r1.txt

# r2
simple_switch_CLI --thrift-port 9091 < commands_r2.txt

# r3
simple_switch_CLI --thrift-port 9092 < commands_r3.txt

# All routers configured!
echo "All routers configured!"

# executar com ./routers.sh
