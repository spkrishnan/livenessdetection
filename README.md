### livenessdetection

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
set system scripts language python
set event-options policy LIVENESS events evpn_core_isolated
set event-options policy LIVENESS then event-script liveness.py arguments host 10.192.34.235
set event-options policy LIVENESS then event-script liveness.py arguments count 5
set event-options event-script file liveness.py python-script-user suresh
commit
"""
