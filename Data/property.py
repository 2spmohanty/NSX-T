__author__ = 'Smruti P Mohanty'
"""
Company : VMWare Inc.
                                Apache License
                               Version 2.0, January 2004
                            http://www.apache.org/licenses/
                        Copyright [2019] [Smruti P Mohanty]

        Licensed under the Apache License, Version 2.0 (the "License");
        you may not use this file except in compliance with the License.
        You may obtain a copy of the License at
        
            http://www.apache.org/licenses/LICENSE-2.0
        
        Unless required by applicable law or agreed to in writing, software
        distributed under the License is distributed on an "AS IS" BASIS,
        WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
        See the License for the specific language governing permissions and
        limitations under the License.



"""

LOG_FILE_NAME = "NSXSetup.log"

# Property Related to vCenter

COMPUTE_MANAGER_IP = None
COMPUTE_MANAGER_USER =  None
COMPUTE_MANAGER_PASS =  None
COMPUTE_MANAGER_LOCAL_USER = None
COMPUTE_MANAGER_LOCAL_PASS = None





#Property related to NSX Manager
NSX_MANAGER_IP =  None
NSX_MANAGER_USER = None,
NSX_MANAGER_PASS = None,





#Property related to Control Cluster Deployment

SKIP_CONTROLLER_CREATION = False
CONTROLLER_DATACENTER = None

CONTROL_CLUSTER = {



    "controller_0" :{

        "CONTROLLER_datastore" :  None,
        "CONTROLLER_cluster" : None,
        "CONTROLLER_host" : None,
        "CONTROLLER_management_network" : None,
        "CONTROLLER_audit_password" : '',
        "CONTROLLER_audit_username" : 'admin',
        "CONTROLLER_cli_password" : '',
        "CONTROLLER_cli_username" : 'admin',
        "CONTROLLER_root_password" : '',
        "CONTROLLER_ip_addresses" : None,
        "CONTROLLER_prefix_length" : None,
        "CONTROLLER_default_gateway_addresses" : ['10.173.203.125'],
        "CONTROLLER_dns_servers" : ['10.172.40.1','10.172.40.2'],
        "CONTROLLER_hostname" : None,
        "CONTROLLER_ntp_servers_fqdn" : ['time.eng.vmware.com'],
        "CONTROLLER_form_factor" : 'MEDIUM'
    },
    "controller_1" :{
        "CONTROLLER_datastore" :  None,
        "CONTROLLER_cluster" : None,
        "CONTROLLER_host" : None,
        "CONTROLLER_management_network" : None,
        "CONTROLLER_audit_password" : '',
        "CONTROLLER_audit_username" : 'admin',
        "CONTROLLER_cli_password" : '',
        "CONTROLLER_cli_username" : 'admin',
        "CONTROLLER_root_password" : '',
        "CONTROLLER_ip_addresses" : None,
        "CONTROLLER_prefix_length" : None,
        "CONTROLLER_default_gateway_addresses" : ['10.173.203.125'],
        "CONTROLLER_dns_servers" : ['10.172.40.1','10.172.40.2'],
        "CONTROLLER_hostname" : None,
        "CONTROLLER_ntp_servers_fqdn" : ['time.eng.vmware.com'],
        "CONTROLLER_form_factor" : 'MEDIUM'
    },
    "controller_2" :{
        "CONTROLLER_datastore" :  None,
        "CONTROLLER_cluster" : None,
        "CONTROLLER_host" : None,
        "CONTROLLER_management_network" : None,
        "CONTROLLER_audit_password" : '',
        "CONTROLLER_audit_username" : 'admin',
        "CONTROLLER_cli_password" : '',
        "CONTROLLER_cli_username" : 'admin',
        "CONTROLLER_root_password" : '',
        "CONTROLLER_ip_addresses" : None,
        "CONTROLLER_prefix_length" : None,
        "CONTROLLER_default_gateway_addresses" : ['10.173.203.125'],
        "CONTROLLER_dns_servers" : ['10.172.40.1','10.172.40.2'],
        "CONTROLLER_hostname" : None,
        "CONTROLLER_ntp_servers_fqdn" : ['time.eng.vmware.com'],
        "CONTROLLER_form_factor" : 'MEDIUM'
    }

}






#VTEP_POOL_TRANSPORT_NODES


VTEP_POOL_NAME =  "vtep-ip-pool"
VTEP_START_IP = "172.168.100.30"
VTEP_END_IP = "172.168.100.100"
VTEP_NETWORK = "172.168.100.0/22"



#Transport Zones

TRANSPORT_ZONES = {
    "OverlaySwitch" : {
        "Type" : "OVERLAY",
        "display_name" : "None",

    }
}

# Compute Collection Datacenter clusters. Clusyters to bE prepped.

CLUSTER_LIST = []

#Transport Nodes

TRANSPORT_NODE_NIC = "vmnic2"



# Edge Details

EDGE_SIZE = "MEDIUM"
EDGE_HOSTNAME = ""
EDGE_IP = ""
EDGE_NETWORK_PREFIX = ""
EDGE_DEFAULT_GW = []
EDGE_DNS_SERVERS = []
EDGE_NTP_SERVERS = []

EDGE_DEPLOYMENT_DATACENTER = ""
EDGE_DEPLOYMENT_CLUSTER_NAME=  ""  #The Cluster in which the edge Appliance would be deployed. Not Same as EDGE_CLUSTER_NAME
EDGE_DEPLOYMENT_HOST  = "" #The Host on which this edge will be deployed.
EDGE_DATA_NETWORKS = []   # Atleast 3. Can be repetitive Foe example ["VM NETWORK","VM NETWORK","VM NETWORK"] . This must be present in EDGE_DEPLOYMENT_HOST
EDGE_DATASTORE = ""
EDGE_MGMT_NETWORK = "" #This must be present in EDGE_DEPLOYMENT_HOST







#DHCP Deployment

DHCP_SERVER_IP = "" #CIDR Formatt Viz.192.168.191.2/24
DHCP_POOL_START_IP = ""
DHCP_POOL_END_IP = ""
DHCP_GW_IP = ""

DHCP_SWITCH = ""


























