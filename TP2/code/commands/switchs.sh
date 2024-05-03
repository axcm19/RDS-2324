#!/bin/bash

# Script que configura todos os switchs da topologia deste trabalho

# s1
sudo ovs-ofctl add-flow s1 in_port=1,actions=output:2,3,4 --protocols=OpenFlow10,OpenFlow13
sudo ovs-ofctl add-flow s1 in_port=2,actions=output:1,3,4 --protocols=OpenFlow10,OpenFlow13
sudo ovs-ofctl add-flow s1 in_port=3,actions=output:1,2,4 --protocols=OpenFlow10,OpenFlow13
sudo ovs-ofctl add-flow s1 in_port=4,actions=output:1,2,3 --protocols=OpenFlow10,OpenFlow13

# s2
sudo ovs-ofctl add-flow s2 in_port=1,actions=output:2,3,4 --protocols=OpenFlow10,OpenFlow13
sudo ovs-ofctl add-flow s2 in_port=2,actions=output:1,3,4 --protocols=OpenFlow10,OpenFlow13
sudo ovs-ofctl add-flow s2 in_port=3,actions=output:1,2,4 --protocols=OpenFlow10,OpenFlow13
sudo ovs-ofctl add-flow s2 in_port=4,actions=output:1,2,3 --protocols=OpenFlow10,OpenFlow13

# s3
sudo ovs-ofctl add-flow s3 in_port=1,actions=output:2,3,4 --protocols=OpenFlow10,OpenFlow13
sudo ovs-ofctl add-flow s3 in_port=2,actions=output:1,3,4 --protocols=OpenFlow10,OpenFlow13
sudo ovs-ofctl add-flow s3 in_port=3,actions=output:1,2,4 --protocols=OpenFlow10,OpenFlow13
sudo ovs-ofctl add-flow s3 in_port=4,actions=output:1,2,3 --protocols=OpenFlow10,OpenFlow13

# All switchs configured!
echo "All switchs configured!"

# executar com ./switchs.sh
