

from mininet.net import Mininet
from mininet.topo import Topo
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.node import OVSKernelSwitch

from p4_mininet import P4Switch, P4Host
from p4runtime_switch import P4RuntimeSwitch

import subprocess
import argparse
from time import sleep

sw_mac_base = "00:aa:bb:00:00:%02x"
host_mac_base = "00:04:00:00:00:%02x"

sw_ip_base = "10.0.%d.254"
host_ip_base =  "10.0.%d.1/24"


class SimpleRouter(Topo):
    def __init__(self, sw_path, thrift_port, grpc_port, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)
        # adding a P4Switch
        
        r1 = self.addSwitch('r1',
                        cls = P4RuntimeSwitch,
                        sw_path = sw_path,
                        #json_path = json_path,
                        thrift_port = thrift_port,
                        grpc_port = grpc_port,
                        device_id = 1,
                        cpu_port = 510)
        r2 = self.addSwitch('r2',
                        cls = P4RuntimeSwitch,
                        sw_path = sw_path,
                        #json_path = json_path,
                        thrift_port = thrift_port+1,
                        grpc_port = grpc_port+1,
                        device_id = 2,
                        cpu_port = 510)


        r3 = self.addSwitch('r3',
                        cls = P4RuntimeSwitch,
                        sw_path = sw_path,
                        #json_path = json_path,
                        thrift_port = thrift_port+2,
                        grpc_port = grpc_port+2,
                        device_id = 3,
                        cpu_port = 510)


         # switchs
        s1 = self.addSwitch('s1', cls = OVSKernelSwitch)
        s2 = self.addSwitch('s2', cls = OVSKernelSwitch)
        s3 = self.addSwitch('s3', cls = OVSKernelSwitch)

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
    parser = argparse.ArgumentParser(description='Mininet demo')
    parser.add_argument('--behavioral-exe', help='Path to behavioral executable',
                        type=str, action="store", default='simple_switch_grpc')
    parser.add_argument('--thrift-port', help='Thrift server port for table updates',
                        type=int, action="store", default=9091)
    parser.add_argument('--grpc-port', help='gRPC server port for controller comm',
                        type=int, action="store", default=50051)
    #parser.add_argument('--json', help='Path to JSON config file',
    #                    type=str, action="store", required=True)

    args = parser.parse_args()



    topo = SimpleRouter(args.behavioral_exe,
                        args.thrift_port,
                        args.grpc_port)
                        #args.json)

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

    num_hosts = 9

    # an array of the mac addrs from the switch
    sw_mac = [sw_mac_base % (n + 1) for n in range(num_hosts)]
    # an array of the ip addrs from the switch 
    # they are only used to define defaultRoutes on hosts 
    sw_addr = [sw_ip_base % (n + 1) for n in range(num_hosts)]

    # h.setARP() populates the arp table of the host
    # h.setDefaultRoute() sets the defaultRoute for the host
    # populating the arp table of the host with the switch ip and switch mac
    # avoids the need for arp request from the host
    

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


    sleep(1)  # time for the host and switch confs to take effect

    subprocess.call("sudo ovs-ofctl add-flow s1 actions=normal", shell=True)
    subprocess.call("sudo ovs-ofctl add-flow s2 actions=normal", shell=True)
    subprocess.call("sudo ovs-ofctl add-flow s3 actions=normal", shell=True)
    

    print("Ready !")

    CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    main()
