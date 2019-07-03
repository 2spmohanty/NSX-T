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

COMPUTE_MANAGER_IP = "10.172.109.23"
COMPUTE_MANAGER_USER =  "root"
COMPUTE_MANAGER_PASS =  "Admin!23"
COMPUTE_MANAGER_LOCAL_USER = "Administrator@skyscraper.local"
COMPUTE_MANAGER_LOCAL_PASS = "Admin!23"





#Property related to NSX Manager
NSX_MANAGER_IP =  "10.173.203.47"
NSX_MANAGER_USER = "admin"
NSX_MANAGER_PASS = "Admin!23"





#Property related to Control Cluster Deployment

SKIP_CONTROLLER_CREATION = False
CONTROLLER_DATACENTER = "Datacenter3"

CONTROL_CLUSTER = {



    "controller_0" :{

        "CONTROLLER_datastore" :  "Shared-1",
        "CONTROLLER_cluster" : "NSXT-MGMT",
        "CONTROLLER_host" : "sc2-hs1-b2819.eng.vmware.com",
        "CONTROLLER_management_network" : "VM-Traffic",
        "CONTROLLER_audit_password" : 'Admin!23',
        "CONTROLLER_audit_username" : 'admin',
        "CONTROLLER_cli_password" : 'Admin!23',
        "CONTROLLER_cli_username" : 'admin',
        "CONTROLLER_root_password" : 'Admin!23',
        "CONTROLLER_ip_addresses" : "10.173.203.48",
        "CONTROLLER_prefix_length" : 25,
        "CONTROLLER_default_gateway_addresses" : ['10.173.203.125'],
        "CONTROLLER_dns_servers" : ['10.172.40.1','10.172.40.2'],
        "CONTROLLER_hostname" : "sc2hs1-stls-vm18.eng.vmware.com",
        "CONTROLLER_ntp_servers_fqdn" : ["time.eng.vmware.com"],
        "CONTROLLER_form_factor" : 'MEDIUM'
    },
    "controller_1" :{
        "CONTROLLER_datastore" :  "Shared-1",
        "CONTROLLER_cluster" : "NSXT-MGMT",
        "CONTROLLER_host" : "sc2-hs1-b2819.eng.vmware.com",
        "CONTROLLER_management_network" : "VM-Traffic",
        "CONTROLLER_audit_password" : 'Admin!23',
        "CONTROLLER_audit_username" : 'admin',
        "CONTROLLER_cli_password" : 'Admin!23',
        "CONTROLLER_cli_username" : 'admin',
        "CONTROLLER_root_password" : 'Admin!23',
        "CONTROLLER_ip_addresses" : "10.173.203.49",
        "CONTROLLER_prefix_length" : 25,
        "CONTROLLER_default_gateway_addresses" : ['10.173.203.125'],
        "CONTROLLER_dns_servers" : ['10.172.40.1','10.172.40.2'],
        "CONTROLLER_hostname" : "sc2hs1-stls-vm19.eng.vmware.com",
        "CONTROLLER_ntp_servers_fqdn" : ["time.eng.vmware.com"],
        "CONTROLLER_form_factor" : 'MEDIUM'
    },
    "controller_2" :{
        "CONTROLLER_datastore" :  "Shared-1",
        "CONTROLLER_cluster" : "NSXT-MGMT",
        "CONTROLLER_host" : "sc2-hs1-b2819.eng.vmware.com",
        "CONTROLLER_management_network" : "VM-Traffic",
        "CONTROLLER_audit_password" : 'Admin!23',
        "CONTROLLER_audit_username" : 'admin',
        "CONTROLLER_cli_password" : 'Admin!23',
        "CONTROLLER_cli_username" : 'admin',
        "CONTROLLER_root_password" : 'Admin!23',
        "CONTROLLER_ip_addresses" : "10.173.203.50",
        "CONTROLLER_prefix_length" : 25,
        "CONTROLLER_default_gateway_addresses" : ['10.173.203.125'],
        "CONTROLLER_dns_servers" : ['10.172.40.1','10.172.40.2'],
        "CONTROLLER_hostname" : "sc2hs1-stls-vm20.eng.vmware.com",
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

CLUSTER_LIST = ["cloud_cluster_1","cloud_cluster_2"]

#Transport Nodes

TRANSPORT_NODE_NIC = "vmnic2"



# Edge Details

EDGE_SIZE = "MEDIUM"
EDGE_HOSTNAME = "sc2hs1-stls-vm21.eng.vmware.com"
EDGE_IP = "10.173.203.51"
EDGE_NETWORK_PREFIX = 25   #Should be Integer
EDGE_DEFAULT_GW = ["10.173.203.125"]
EDGE_DNS_SERVERS = ["10.172.40.1","10.172.40.2"]
EDGE_NTP_SERVERS = ["10.111.0.101"]  #The format should be IP adress not fqdn

EDGE_DEPLOYMENT_DATACENTER = "Datacenter3"
EDGE_DEPLOYMENT_CLUSTER_NAME=  "NSXT-MGMT"  #The Cluster in which the edge Appliance would be deployed. Not Same as EDGE_CLUSTER_NAME
EDGE_DEPLOYMENT_HOST  = "sc2-hs1-b2819.eng.vmware.com" #The Host on which this edge will be deployed.
EDGE_DATA_NETWORKS = ["VM-Traffic","VM-Traffic","VM-Traffic"]   # Atleast 3. Can be repetitive Foe example ["VM NETWORK","VM NETWORK","VM NETWORK"] . This must be present in EDGE_DEPLOYMENT_HOST
EDGE_DATASTORE = "Shared-1"
EDGE_MGMT_NETWORK = "VM-Traffic" #This must be present in EDGE_DEPLOYMENT_HOST







#DHCP Deployment

DHCP_SERVER_IP = "192.168.191.2/24" #CIDR Formatt Viz.192.168.191.2/24
DHCP_POOL_START_IP = "192.168.191.90"
DHCP_POOL_END_IP = "192.168.191.230"
DHCP_GW_IP = "192.168.191.1"

DHCP_SWITCH = "DHCP-Switch-0"


























