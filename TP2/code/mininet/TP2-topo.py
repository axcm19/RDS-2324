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
        
        #-------------------------------------------------------------------------------
        # LAN 1

        host1 = self.addHost('svr11',
                            ip = "10.0.1.10/24",
                            mac = host_mac_base % (1))

        sw_mac1 = sw_mac_base % (1)
        self.addLink(host1, s1, addr2=sw_mac1)

        host2 = self.addHost('svr12',
                            ip = "10.0.1.20/24",
                            mac = host_mac_base % (2))
        sw_mac2 = sw_mac_base % (2)
        self.addLink(host2, s1, addr2=sw_mac2)

        host3 = self.addHost('h11',
                            ip = "10.0.1.100/24",
                            mac = host_mac_base % (3))
        sw_mac3 = sw_mac_base % (3)
        self.addLink(host3, s1, addr2=sw_mac3)

        #-------------------------------------------------------------------------------      
        # LAN 2

        host4 = self.addHost('svr21',
                            ip = "10.0.2.10/24",
                            mac = host_mac_base % (4))
        sw_mac4 = sw_mac_base % (4)
        self.addLink(host4, s2, addr2=sw_mac4)

        host5 = self.addHost('svr22',
                            ip = "10.0.2.20/24",
                            mac = host_mac_base % (5))
        sw_mac5 = sw_mac_base % (5)
        self.addLink(host5, s2, addr2=sw_mac5)

        host6 = self.addHost('h21',
                            ip = "10.0.2.100/24",
                            mac = host_mac_base % (6))
        sw_mac6 = sw_mac_base % (6)
        self.addLink(host6, s2, addr2=sw_mac6)


        #-------------------------------------------------------------------------------
        # LAN 3

        host7 = self.addHost('svr31',
                            ip = "10.0.3.10/24",
                            mac = host_mac_base % (7))
        sw_mac7 = sw_mac_base % (7)
        self.addLink(host7, s3, addr2=sw_mac7)

        host8 = self.addHost('svr32',
                            ip = "10.0.3.20/24",
                            mac = host_mac_base % (8))
        sw_mac8 = sw_mac_base % (8)
        self.addLink(host8, s3, addr2=sw_mac8)

        host9 = self.addHost('h31',
                            ip = "10.0.3.100/24",
                            mac = host_mac_base % (9))
        sw_mac9 = sw_mac_base % (9)
        self.addLink(host9, s3, addr2=sw_mac9)

        #-------------------------------------------------------------------------------

        #adicionar links entre switchs e routers

        sw_mac10 = "00:aa:bb:00:00:10"
        sw_mac11 = "00:aa:bb:00:00:11"

        sw_mac12 = "00:aa:bb:00:00:12"
        sw_mac13 = "00:aa:bb:00:00:13"

        sw_mac14 = "00:aa:bb:00:00:14"
        sw_mac15 = "00:aa:bb:00:00:15"

        sw_mac16 = "00:aa:bb:00:00:16"
        sw_mac17 = "00:aa:bb:00:00:17"

        sw_mac18 = "00:aa:bb:00:00:18"
        sw_mac19 = "00:aa:bb:00:00:19"

        sw_mac20 = "00:aa:bb:00:00:20"
        sw_mac21 = "00:aa:bb:00:00:21"


        self.addLink(s1, r1, addr1=sw_mac10 ,addr2=sw_mac11)
        self.addLink(s2, r2, addr1=sw_mac12 ,addr2=sw_mac13)
        self.addLink(s3, r3, addr1=sw_mac14 ,addr2=sw_mac15)
        self.addLink(r1, r3, addr1=sw_mac16 ,addr2=sw_mac17)
        self.addLink(r1, r2, addr1=sw_mac18 ,addr2=sw_mac19)
        self.addLink(r2, r3, addr1=sw_mac20 ,addr2=sw_mac21)

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
    
    gateway_mac_r1 = "00:aa:bb:00:00:11"
    gateway_ip_r1 = "10.0.1.254"
    gateway_mac_r2 = "00:aa:bb:00:00:13"
    gateway_ip_r2 = "10.0.2.254"
    gateway_mac_r3 = "00:aa:bb:00:00:15"
    gateway_ip_r3 = "10.0.3.254"




    h11 = net.get('h11')
    h11.setARP(gateway_ip_r1,gateway_mac_r1)
    h11.setDefaultRoute("dev eth0 via %s" % gateway_ip_r1)

    svr11 = net.get('svr11')
    svr11.setARP(gateway_ip_r1,gateway_mac_r1)
    svr11.setDefaultRoute("dev eth0 via %s" % gateway_ip_r1)

    svr12 = net.get('svr12')
    svr12.setARP(gateway_ip_r1,gateway_mac_r1)
    svr12.setDefaultRoute("dev eth0 via %s" % gateway_ip_r1)

    h21 = net.get('h21')
    h21.setARP(gateway_ip_r2,gateway_mac_r2)
    h21.setDefaultRoute("dev eth0 via %s" % gateway_ip_r2)

    svr21 = net.get('svr21')
    svr21.setARP(gateway_ip_r2,gateway_mac_r2)
    svr21.setDefaultRoute("dev eth0 via %s" % gateway_ip_r2)

    svr22 = net.get('svr22')
    svr22.setARP(gateway_ip_r2,gateway_mac_r2)
    svr22.setDefaultRoute("dev eth0 via %s" % gateway_ip_r2)

    h31 = net.get('h31')
    h31.setARP(gateway_ip_r3,gateway_mac_r3)
    h31.setDefaultRoute("dev eth0 via %s" % gateway_ip_r3)

    svr31 = net.get('svr31')
    svr31.setARP(gateway_ip_r3,gateway_mac_r3)
    svr31.setDefaultRoute("dev eth0 via %s" % gateway_ip_r3)

    svr32 = net.get('svr32')
    svr32.setARP(gateway_ip_r3,gateway_mac_r3)
    svr32.setDefaultRoute("dev eth0 via %s" % gateway_ip_r3)


    # adiciona ip's a todas as interfaces do router r1 (eth1 -> 10.0.1.254)
    router = net.get('r1')  
    router.cmd('ip addr add 10.0.1.252/24 dev eth2')    
    router.cmd('ip addr add 10.0.1.253/24 dev eth3')

    # adiciona ip's a todas as interfaces do router r2 (eth1 -> 10.0.2.254)
    router = net.get('r2')  
    router.cmd('ip addr add 10.0.2.252/24 dev eth2')    
    router.cmd('ip addr add 10.0.2.253/24 dev eth3')

    # adiciona ip's a todas as interfaces do router r3 (eth1 -> 10.0.3.254)
    router = net.get('r3')  
    router.cmd('ip addr add 10.0.3.252/24 dev eth2')    
    router.cmd('ip addr add 10.0.3.253/24 dev eth3')


    # Exibe informações sobre os hosts
    for n in hosts:
        hs = net.get(n.__name__)
        hs.describe()

    sleep(1)  # time for the host and switch confs to take effect

    print("Ready !")

    CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    main()
