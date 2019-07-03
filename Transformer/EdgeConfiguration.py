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

from com.vmware import nsx_client
import com.vmware.nsx.model_client as model_client
from com.vmware.nsx import fabric_client
import com.vmware.nsx.fabric.nodes_client as nodes_client
import com.vmware.nsx.transport_nodes_client as transport_nodes_client
import time
import com.vmware.nsx.dhcp_client as dhcp_client
import com.vmware.nsx.dhcp.servers_client as dhcp_servers_client



class Edge():
    def __init__(self,stub_config,edge_size,edge_hostname,edge_ip,network_prefix,default_gateway_addresses,
                 dns_servers,cluster_mob_id,data_network_mob_ids,host_mob_id,
                 management_network_mob_id,ntp_servers,datastore_mob_id,compute_manager_id):
        self.stub_config = stub_config
        self.edge_size = edge_size
        self.edge_ip = edge_ip
        self.edge_hostname = edge_hostname
        self.network_prefix = network_prefix
        self.default_gateway_addresses = default_gateway_addresses
        self.dns_servers = dns_servers
        self.cluster_mob_id = cluster_mob_id
        self.data_network_mob_ids = data_network_mob_ids
        self.host_mob_id = host_mob_id
        self.management_network_mob_id = management_network_mob_id
        self.ntp_servers = ntp_servers
        self.datastore_mob_id = datastore_mob_id
        self.compute_manager_id = compute_manager_id



    def create(self):

        nodeUserSpec = model_client.NodeUserSettings(audit_password='Admin!23', audit_username='audit',
                                                     cli_password='Admin!23', cli_username='admin',
                                                     root_password='Admin!23')
        data_network_ids = ["network-33018", "network-33018", "network-33018"]
        management_port_subnets = model_client.IPSubnet(ip_addresses=[self.edge_ip], prefix_length=self.network_prefix)

        vm_deployment_config = model_client.VsphereDeploymentConfig(allow_ssh_root_login=True,
                                                                    compute_id=self.cluster_mob_id,
                                                                    data_network_ids=data_network_ids,
                                                                    default_gateway_addresses=self.default_gateway_addresses,
                                                                    dns_servers=self.dns_servers,
                                                                    enable_ssh=True,
                                                                    host_id=self.host_mob_id,
                                                                    hostname=self.edge_hostname,
                                                                    management_network_id=self.management_network_mob_id,
                                                                    management_port_subnets=[management_port_subnets],
                                                                    ntp_servers=["10.111.0.101"],
                                                                    search_domains=["eng.vmware.com"],
                                                                    storage_id=self.datastore_mob_id,
                                                                    vc_id=self.compute_manager_id,
                                                                    placement_type='VsphereDeploymentConfig')

        deployment_config = model_client.EdgeNodeDeploymentConfig(form_factor=self.edge_size, node_user_settings=nodeUserSpec,
                                                                  vm_deployment_config=vm_deployment_config)

        edgeNodeSpec = model_client.EdgeNode(deployment_config=deployment_config, display_name=self.edge_hostname,
                                             resource_type='EdgeNode')

        EdgeNodesClient = fabric_client.Nodes(self.stub_config)

        edge_id = None
        final_edge = False


        try:


            edge = EdgeNodesClient.create(edgeNodeSpec)

            print ( "Edge - Deployed edge with Edge Config Spec")

            edge_id = edge.convert_to(model_client.Node).external_id

            edge_status_client =  nodes_client.State(self.stub_config)

            edge_failure = ["EDGE_CONFIG_ERROR", "INSTALL_FAILED", 'REGISTRATION_FAILED', 'VM_DEPLOYMENT_FAILED',
                            "VM_POWER_ON_FAILED"]
            loop = True


            print ("Edge - Initiating Edge Deployment Status Check for edge %s"%edge_id)

            while (loop):
                edge_status = edge_status_client.get(edge_id).state
                if edge_status == 'NODE_READY':
                    print "Edge Successfully deployed."
                    loop = False
                    final_edge = True
                elif edge_status in edge_failure:
                    print "Edge Deployment Failed."
                    loop = False

                else:
                    print "Edge - Edge Deployment %s"%edge_status
                    print("Edge - Sleep for 60 seconds beofre next polling")
                    time.sleep(60)
        except Exception,e:
            print ("Edge - Error while deplying edge %s"%e)
            return edge_id, final_edge


        return edge_id , final_edge









"""
for enode in enodes.results:
    node_type = enode.convert_to(model_client.Node).resource_type
    if node_type == "EdgeNode":
        print enode.convert_to(model_client.Node).external_id


"""


def CreateEdgeUplinkProfile(stub_config):
    profiles_client = nsx_client.HostSwitchProfiles(stub_config)

    uplink_spec = model_client.Uplink(uplink_name="uplink-1", uplink_type="PNIC")

    teaming_spec = model_client.TeamingPolicy(active_list=[uplink_spec], policy="FAILOVER_ORDER")

    uplink_hostswitch_profile = model_client.UplinkHostSwitchProfile(mtu=1500, teaming=teaming_spec,
                                                                     display_name="edge-uplink",
                                                                     description="Edge Uplink Profile")

    edge_uplink = profiles_client.create(uplink_hostswitch_profile)

    time.sleep(5)
    
    return edge_uplink.convert_to(model_client.BaseHostSwitchProfile).id





def MarkEdgeAsTransportNode(logger, stub_config,vtep_pool_id,edge_profile_id,transport_zone_id,edge_id):
    tn_result_id = None

    try:
        tn_client = nsx_client.TransportNodes(stub_config)

        ip_assignment_spec = model_client.StaticIpPoolSpec(ip_pool_id=vtep_pool_id,
                                                           resource_type='StaticIpPoolSpec')

        pnic = model_client.Pnic(device_name="fp-eth1", uplink_name="uplink-1")



        host_switch_profile_id = model_client.HostSwitchProfileTypeIdEntry(key="UplinkHostSwitchProfile",
                                                                           value=edge_profile_id)

        host_switch = model_client.StandardHostSwitch(host_switch_name="OverlaySwitch",
                                                      host_switch_profile_ids=[host_switch_profile_id],
                                                      ip_assignment_spec=ip_assignment_spec, pnics=[pnic])

        host_switch_spec = model_client.StandardHostSwitchSpec(host_switches=[host_switch],
                                                               resource_type='StandardHostSwitchSpec')

        tz_endpoint = model_client.TransportZoneEndPoint(transport_zone_id=transport_zone_id)

        transport_node_spec = model_client.TransportNode(description="Edge Transport Node", display_name="Edge-TN-Node-Auto-1",
                                                         host_switch_spec=host_switch_spec,
                                                         node_id=edge_id,
                                                         transport_zone_endpoints=[tz_endpoint])

        tn_result = tn_client.create(transport_node_spec)

        tn_result_id = tn_result.id



        edge_tn_client = transport_nodes_client.State(stub_config)

        loop = True

        while (loop):
            edge_tn_state = edge_tn_client.get(tn_result_id).state
            if edge_tn_state == 'success' or edge_tn_state == 'SUCCESS':
                logger.info ("Edge Node %s deployment is sucess"%edge_tn_state)
                loop = False
            elif edge_tn_state in ['failed' ,'orphaned' ]:
                logger.info ("Edge Node %s deployment failed" % edge_tn_state)
                loop = False
            else:
                logger.info ("Edge Node %s deployment " % edge_tn_state)
                print("Sleep for 30 seconds before next poll")
                time.sleep(30)


        return tn_result_id,True

    except Exception,e:
        logger.error("Error while making the Edge as Transport Node %s"%e)
        return tn_result_id,False



def CreateEdgeCluster(logger,stub_config,transport_node_id):
    edge_cluster_id = None
    try:
        logger.info("Creating Edge Cluster")
        edge_clusters_client = nsx_client.EdgeClusters(stub_config)
        member = model_client.EdgeClusterMember(transport_node_id=transport_node_id)
        edge_cluster_spec = model_client.EdgeCluster(description="Egde Cluster for NSX", display_name="Edge-Cluster-0",
                                                     members=[member])

        edge_cluster = edge_clusters_client.create(edge_cluster_spec)
        return edge_cluster.id , True
    except Exception,e:
        logger.error("Edge cluster creation failed with %s"%e)
        return edge_cluster_id , False




def CreateDHCPServerProfile(logger,stub_config,edge_cluster_id):
    server_profile = None
    try:
        server_profile_client = dhcp_client.ServerProfiles(stub_config)

        dhcp_profile_spec = model_client.DhcpProfile(description="DHCP Server Profile",
                                                     display_name="dhcp-server-profile-0",
                                                     edge_cluster_id=edge_cluster_id,
                                                     resource_type="DhcpProfile")

        server_profile = server_profile_client.create(dhcp_profile_spec)

        return server_profile.id, True
    except Exception,e:
        logger.info ("DHCP Server Profile Creation failed with Error %s"%e)
        return server_profile, False




#Create DHCP Servers
#dhcp_server_ip = "192.168.191.2/24"

def CreateDHCPServer(logger,stub_config,dhcp_server_ip,dhcp_profile_id):
    dhcp_server_id = None

    try:

        dhcp_server_client = dhcp_client.Servers(stub_config)

        ipv4dhcpserverspec = model_client.IPv4DhcpServer(dhcp_server_ip=dhcp_server_ip)

        logical_dhcp_server_spec = model_client.LogicalDhcpServer(description="DHCP Server Auto",
                                                                  display_name="dhcp-server-one",
                                                                  dhcp_profile_id=dhcp_profile_id,
                                                                  ipv4_dhcp_server=ipv4dhcpserverspec)

        dhcp_server = dhcp_server_client.create(logical_dhcp_server_spec)

        dhcp_server_id = dhcp_server.id
        return dhcp_server_id , True
    except Exception,e:
        logger.info("DHCP Server creation failed with error %s"%e)
        return dhcp_server_id, False





def CreateDHCPPool(logger,stub_config,start_ip,end_ip,dhcp_gateway_ip,dhcp_server_id):
    dhcp_pool_id = None
    try:

        dhcp_ip_pool_client = dhcp_servers_client.IpPools(stub_config)

        ipRange = model_client.IpPoolRange(start=start_ip,
                                           end=end_ip)

        dhcp_ip_pool_spec = model_client.DhcpIpPool(resource_type="DhcpIpPool",
                                                    display_name="dhcp-ip-pool",
                                                    gateway_ip=dhcp_gateway_ip,
                                                    allocation_ranges=[ipRange])
        dhcp_ip_pool_stat = dhcp_ip_pool_client.create(server_id=dhcp_server_id,
                                                       dhcp_ip_pool=dhcp_ip_pool_spec)

        dhcp_pool_id = dhcp_ip_pool_stat.id

        return dhcp_pool_id, True
    except Exception,e:
        logger.error("Error while creating DHCP Pool %s"%e)
        return dhcp_pool_id , False




def CreateLogicalSwitch(logger,stub_config,switch_name,transport_zone_id):

    logical_switch_id = None
    try:
        logical_switch_client = nsx_client.LogicalSwitches(stub_config)

        logical_switch_spec = model_client.LogicalSwitch(display_name=switch_name,
                                                         transport_zone_id=transport_zone_id,
                                                         admin_state="UP",
                                                         replication_mode='MTEP')

        logical_switch = logical_switch_client.create(logical_switch_spec)
        logical_switch_id = logical_switch.id
        return logical_switch_id , True
    except Exception,e:
        logger.error("Logical switch creation failed with error %s"%e)
        return logical_switch_id, False





def AttachDhcpToLS(logger,stub_config,dhcp_server_id,logical_switch_id):
    dcp_port_id = None

    try:


        logical_port_client = nsx_client.LogicalPorts(stub_config)



        attachmentspec = model_client.LogicalPortAttachment(attachment_type="DHCP_SERVICE",
                                                            id=dhcp_server_id)

        logical_port_spec = model_client.LogicalPort(display_name="DHCP-Server-Port",
                                                     admin_state="UP",
                                                     logical_switch_id=logical_switch_id,
                                                     attachment=attachmentspec)

        dhcp_port = logical_port_client.create(logical_port_spec)

        dcp_port_id= dhcp_port.id

        return dcp_port_id, True

    except Exception,e:
        logger.error("Error while attaching DHCP Server to Logical Switch %s"%e)
        return dcp_port_id, None


