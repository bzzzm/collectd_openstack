from novaclient import client
from novaclient import exceptions

import collectd
import traceback
import json
import socket

import base

class NovaComputePlugin(base.Base):

    def __init__(self):
        base.Base.__init__(self)
        self.ksession = self.get_keystone()
        self.nova = client.Client(2, session=self.ksession)

        self.hostname = socket.gethostname()

    def get_stats(self):
        for hypervisor in self.nova.hypervisors.list():
            if self.hostname == hypervisor.hypervisor_hostname:
                hv = {
                    'vms': hypervisor.running_vms,
                    'vcpus_used': hypervisor.vcpus_used,
                    'vcpus_total': hypervisor.vcpus,
                    'free_ram': hypervisor.free_ram_mb,
                    'total_ram': hypervisor.memory_mb,
                    'used_ram': hypervisor.memory_mb_used,
                }

        # dispach
        for key, val in hv.iteritems():
            metric = collectd.Values()
            metric.plugin = 'nova_compute'
            metric.type_instance = key
            metric.type = 'gauge'
            metric.values = [val]

            metric.dispatch()



plugin = NovaComputePlugin()
def configure_callback(conf):
    """Received configuration information"""
    plugin.config_callback(conf)

def read_callback():
    """Callback triggerred by collectd on read"""
    plugin.get_stats()
    
collectd.register_config(configure_callback)
collectd.register_read(read_callback, plugin.interval)
