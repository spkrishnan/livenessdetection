#!/usr/bin/env python

# This script is triggered when the event "evpn_core_isolated" is detected. 
#
# This script pings the configured management IP address of the remote peer.
#
# if the management IP address of the remote peer is pingable, all the AE interfaces on this box are disabled. If the management IP address of the remote peer is not pingable, this node will continue forwarding traffic.


"""
Load the script in the following directory on the box
/var/db/scripts/event

Example configuration
show event-options 
policy LIVENESS {
    events evpn_core_isolated;
    then {
        event-script liveness.py {
            arguments {
                host 10.192.34.235;
                count 5;
            }
        }
    }
}
event-script {
    file liveness.py {
        python-script-user suresh;
    }
}

Load the following config on box:
set event-options policy LIVENESS events evpn_core_isolated
set event-options policy LIVENESS then event-script liveness.py arguments host 10.192.34.235
set event-options policy LIVENESS then event-script liveness.py arguments count 5
set event-options event-script file liveness.py python-script-user suresh
commit


"""

import argparse
import jcs
from jnpr.junos import Device
from junos import Junos_Context
from jnpr.junos.utils.config import Config
from lxml import etree

def main():
    parser = argparse.ArgumentParser(description='Pings remote host and prints the rtt details.')
    parser.add_argument('-host', required=True, help='IP address of remote host')
    parser.add_argument('-count', required=True, help='Number of attempts')

    args = parser.parse_args()

    args.host = args.host
    args.count = args.count


    dev = Device()
    dev.open()

    try:
        result = dev.rpc.ping(host=args.host, count=args.count, normalize='True')
        if result.findtext('.//packet-loss') == '0':
                message = "This script was triggered because evpn-core-isolated event was detected." + " Ping to host " + str(args.host) + " at time " + str(Junos_Context['localtime']) + " successful." + " Master ESI-LAG Peer is still reachable. So, this peer is shutting down AE interfaces to avoid split brain state."
                config_set = """deactivate chassis aggregated-devices"""
                cu = Config(dev)
                cu.lock()
                cu.load(config_set, format="set", merge=True)
                cu.commit()
                cu.unlock()
        else:
                message = "This script was triggered because evpn-core-isolated event was detected." + " Ping to host " + str(args.host) + " at time " + str(Junos_Context['localtime']) + " failed." + " Master ESI-LAG peer may be down."
                dev.close()
    except:
        message = "Failed to execute Ping"
        dev.close()

    jcs.syslog("external.info", message)

    # dump the output to a file
    fo = open("/var/tmp/sample.txt", "w+")
    fo.write(message)
    fo.close()

    dev.close()


if __name__ == '__main__':
    main()
