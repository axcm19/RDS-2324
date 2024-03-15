#!/usr/bin/env python3
# Copyright 2013-present Barefoot Networks, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
############################################################################
# RDS-TUT jfpereira - Read all comments from this point on !!!!!!
############################################################################
# This code is given in 
# https://github.com/p4lang/behavioral-model/blob/main/mininet/1sw_demo.py
# with minor adjustments to satisfy the requirements of RDS-TP3. 
# This script works for a topology with one P4Switch connected to 253 P4Hosts. 
# In this TP3, we only need 1 P4Switch and 2 P4Hosts.
# The P4Hosts are regular mininet Hosts with IPv6 suppression.
# The P4Switch it's a very different piece of software from other switches 
# in mininet like OVSSwitch, OVSKernelSwitch, UserSwitch, etc.
# You can see the definition of P4Host and P4Switch in p4_mininet.py
###########################################################################

from mininet.net import Mininet
from mininet.topo import Topo
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.node import OVSSwitch

from p4_mininet import P4Switch, P4Host

import argparse
from time import sleep

# If you look at this parser, it can identify 4 arguments
# --behavioral-exe, with the default value 'simple_switch'
## this indicates that the arch of our software switch is the 'simple_switch'
## and any p4 program made for this arch needs to be compiled against de 'v1model.p4'
# --thrift-port, with the default value of 9090, which is the default server port of
## a thrift server - the P4Switch instantiates a Thrift server that allows us
## to communicate our P4Switch (software switch) at runtime
# --num-hosts, with default value 2 indicates the number of hosts...
# --json, is the path to JSON config file - the output of your p4 program compilation
## this is the only argument that you will need to pass in orther to run the script
parser = argparse.ArgumentParser(description='Mininet demo')
parser.add_argument('--behavioral-exe', help='Path to behavioral executable',
                    type=str, action="store", default='simple_switch')
parser.add_argument('--thrift-port', help='Thrift server port for table updates',
                    type=int, action="store", default=9090)
parser.add_argument('--num-hosts', help='Number of hosts to connect to switch',
                    type=int, action="store", default=9)
parser.add_argument('--json', help='Path to JSON config file',
                    type=str, action="store", required=True)

args = parser.parse_args()

sw_mac_base = "00:aa:bb:00:00:%02x"
host_mac_base = "00:04:00:00:00:%02x"

sw_ip_base = "10.0.%d.254"
host_ip_base =  "10.0.%d.1/24"


class SingleSwitchTopo(Topo):
    def __init__(self, sw_path, json_path, thrift_port, n, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)
        # adding a P4Switch
        """
        switch = self.addSwitch('s1',
                                sw_path = sw_path,
                                json_path = json_path,
                                thrift_port = thrift_port)
        """

        # adicionar os 3 routers(switches)
        r1 = self.addSwitch('r1',
                            cls = P4Switch,
                            sw_path = sw_path,
                            json_path = json_path,
                            thrift_port = thrift_port)

        r2 = self.addSwitch('r2',
                            cls = P4Switch,
                            sw_path = sw_path,
                            json_path = json_path,
                            thrift_port = thrift_port + 1)

        r3 = self.addSwitch('r3',
                            cls = P4Switch,
                            sw_path = sw_path,
                            json_path = json_path,
                            thrift_port = thrift_port + 2)

        # adicionar os 3 switches OVS
        s1 = self.addSwitch('s1',
                            cls = OVSSwitch)

        s2 = self.addSwitch('s2',
                            cls = OVSSwitch)

        s3 = self.addSwitch('s3',
                            cls = OVSSwitch)
        
        # adding host and link with the right mac and ip addrs
        # declaring a link: addr2=sw_mac gives a mac to the switch port
        
        # LAN 1
        for h in range(0,3):
            if h == 0:
                host = self.addHost('svr11',
                                    ip = "10.0.1.10/24",
                                    mac = host_mac_base % (h + 1))


                sw_mac = sw_mac_base % (h + 1)
                self.addLink(host, s1, addr2=sw_mac)
            if h == 1:
                host = self.addHost('svr12',
                                    ip = "10.0.1.20/24",
                                    mac = host_mac_base % (h + 1))
                sw_mac = sw_mac_base % (h + 1)
                self.addLink(host, s1, addr2=sw_mac)
            if h == 2:
                host = self.addHost('h11',
                                    ip = "10.0.1.100/24",
                                    mac = host_mac_base % (h + 1))
                sw_mac = sw_mac_base % (h + 1)
                self.addLink(host, s1, addr2=sw_mac)
                
        # LAN 2
        for h in range(3,6):
            if h == 3:
                host = self.addHost('svr21',
                                    ip = "10.0.2.10/24",
                                    mac = host_mac_base % (h + 1))
                sw_mac = sw_mac_base % (h + 1)
                self.addLink(host, s2, addr2=sw_mac)
            if h == 4:
                host = self.addHost('svr22',
                                    ip = "10.0.2.20/24",
                                    mac = host_mac_base % (h + 1))
                sw_mac = sw_mac_base % (h + 1)
                self.addLink(host, s2, addr2=sw_mac)
            if h == 5:
                host = self.addHost('h21',
                                    ip = "10.0.2.100/24",
                                    mac = host_mac_base % (h + 1))
                sw_mac = sw_mac_base % (h + 1)
                self.addLink(host, s2, addr2=sw_mac)

        # LAN 3
        for h in range(6,9):
            if h == 6:
                host = self.addHost('svr31',
                                    ip = "10.0.3.10/24",
                                    mac = host_mac_base % (h + 1))
                sw_mac = sw_mac_base % (h + 1)
                self.addLink(host, s3, addr2=sw_mac)
            if h == 7:
                host = self.addHost('svr32',
                                    ip = "10.0.3.20/24",
                                    mac = host_mac_base % (h + 1))
                sw_mac = sw_mac_base % (h + 1)
                self.addLink(host, s3, addr2=sw_mac)
            if h == 8:
                host = self.addHost('h31',
                                    ip = "10.0.3.100/24",
                                    mac = host_mac_base % (h + 1))
                sw_mac = sw_mac_base % (h + 1)
                self.addLink(host, s3, addr2=sw_mac)

        #adicionar links entre switchs e routers
        self.addLink(s1, r1, addr2=sw_mac)
        self.addLink(s2, r2, addr2=sw_mac)
        self.addLink(s3, r3, addr2=sw_mac)
        self.addLink(r1, r3, addr2=sw_mac)
        self.addLink(r1, r2, addr2=sw_mac)
        self.addLink(r2, r3, addr2=sw_mac)

def main():
    num_hosts = args.num_hosts

    topo = SingleSwitchTopo(args.behavioral_exe,
                            args.json,
                            args.thrift_port,
                            num_hosts)

    # the host class is the P4Host
    # the switch class is the P4Switch
    net = Mininet(topo = topo,
                  host = P4Host,
                  #switch = P4Switch,
                  controller = None)

    # Here, the mininet will use the constructor (__init__()) of the P4Switch class, 
    # with the arguments passed to the SingleSwitchTopo class in order to create 
    # our software switch.
    net.start()

    # an array of the mac addrs from the switch
    sw_mac = [sw_mac_base % (n + 1) for n in range(num_hosts)]
    # an array of the ip addrs from the switch 
    # they are only used to define defaultRoutes on hosts 
    sw_addr = [sw_ip_base % (n + 1) for n in range(num_hosts)]

    # h.setARP() populates the arp table of the host
    # h.setDefaultRoute() sets the defaultRoute for the host
    # populating the arp table of the host with the switch ip and switch mac
    # avoids the need for arp request from the host
    """
    for n in range(num_hosts):
        h = net.get('h%d' % (n + 1))
        h.setARP(sw_addr[n], sw_mac[n])
        h.setDefaultRoute("dev eth0 via %s" % sw_addr[n])

    for n in range(num_hosts):
        h = net.get('h%d' % (n + 1))
        h.describe()
    """

    hosts = [node for node in net.topo.hosts() if isinstance(node, net.host)]
    for h in hosts:
        hs = net.get(h.__name__)
        hs.setARP(sw_addr[n], sw_mac[n])
        hs.setDefaultRoute("dev eth0 via %s" % sw_addr[n])

    for h in hosts:
        hs = net.get(h.__name__)
        hs.describe()

    sleep(1)  # time for the host and switch confs to take effect

    print("Ready !")

    CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    main()
