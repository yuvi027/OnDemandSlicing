from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSKernelSwitch, RemoteController
from mininet.cli import CLI
from mininet.link import TCLink


class Topology(Topo):
    def __init__(self):
        # Initialize topology
        Topo.__init__(self)

        # Create template host, switch, and link
        host_config = dict(inNamespace=True)
        switch_link = dict(bw=10)
        host_link = dict(bw=2)

        # Create switch nodes
        for i in range(4):
            sconfig = {"dpid": "%016x" % (i + 1)}
            self.addSwitch("s%d" % (i + 1), **sconfig)

        # Create student nodes
        for i in range(2):
            self.addHost("St%d" % (i + 1), **host_config)
        # Create researcher nodes
        for j in range(2):
            self.addHost("r%d" % (j + 1), **host_config)

        # Add switch links
        self.addLink("s1", "s2", **switch_link)
        self.addLink("s2", "s3", **switch_link)
        self.addLink("s3", "s4", **switch_link)
        self.addLink("s1", "s4", **switch_link)

        # Add host links
        self.addLink("St1", "s1", **host_link)
        self.addLink("r1", "s1", **host_link)
        self.addLink("St2", "s3", **host_link)
        self.addLink("r2", "s3", **host_link)


topos = {"topology": (lambda: Topology())}

if __name__ == "__main__":
    topo = Topology()
    net = Mininet(
        topo=topo,
        switch=OVSKernelSwitch,
        controller=RemoteController("c1", ip="127.0.0.1", port=6633),
        build=False,
        autoSetMacs=True,
        autoStaticArp=True,
        link=TCLink,
    )
    net.build()
    net.start()
    CLI(net)
    net.stop()
