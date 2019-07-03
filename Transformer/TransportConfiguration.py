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
import com.vmware.nsx.model_client as model_client
import com.vmware.nsx.pools_client as pools_client
from com.vmware.nsx import fabric_client
from com.vmware import nsx_client
from vmware.vapi.bindings.stub import ApiClient
from Utility import get_certificate_value,stub_configuration
from com.vmware.nsx import compute_collection_transport_node_templates_client
import time
import com.vmware.nsx.fabric.nodes_client as  nodes_client
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



def CreateVtepIpPool(logger,stub_config,ip_pool_name,start_ip,end_ip,network_cidr):
    """
    @param logger:
    @param stub_config: vmware.vapi.bindings.stub.StubConfiguration
    @param ip_pool_name: Name of IP Pool
    @param start_ip: The Starting IP for VTEP IP Pool
    @param end_ip: The Ending IP for VTEP IP Pool
    @param network_cidr: The Network in CIDR formatt.
    @return: Return VTEP Pool ID
    """

    try:
        vtep_pool_id = None

        logger.info("CreateVtepIpPool - Creating VTEP pool")

        vtepPool = pools_client.IpPools(stub_config)

        allocation_range = model_client.IpPoolRange(end=end_ip, start=start_ip)

        subnet = model_client.IpPoolSubnet(allocation_ranges=[allocation_range], cidr=network_cidr)

        ip_pool_spec = model_client.IpPool(display_name=ip_pool_name, subnets=[subnet])

        vtepPoolDetails = vtepPool.create(ip_pool_spec)

        logger.info("CreateVtepIpPool - VTEP Pools created %s "% vtepPoolDetails)

        vtep_pool_id = vtepPoolDetails.id

        return vtep_pool_id , True

    except Exception,e:
        return "CreateVtepIpPool - Failed creating VTEP Pool with exception %s"%(e) , False




class TransportZone():

    def __init__(self,stub_config,zone_type,display_name,host_switch_name,description=None):
        """

        @param stub_config: vmware.vapi.bindings.stub.StubConfiguration
        @param zone_type: OVERLAY / VLAN
        @param display_name: Display Name of this Transport Zone
        @param description: Description of this Transport Zone
        @param host_switch_name: NVDS Name
        """
        self.stub_config =  stub_config
        self.zone_type = zone_type
        self.display_name = display_name
        self.description = description
        self.host_switch_name = host_switch_name

    def create(self):
        try:
            transport_zone_id = None

            stub_factory = nsx_client.StubFactory(self.stub_config)

            api_client = ApiClient(stub_factory)

            overlay_transport_zone_spec = model_client.TransportZone(transport_type=self.zone_type,
                                                                     display_name=self.display_name,
                                                                     description=self.description,
                                                                     host_switch_name=self.host_switch_name)
            transport_zone = api_client.TransportZones.create(overlay_transport_zone_spec)
            print("TransportZone - Overlay Transport zone created. id is %s" % transport_zone)
            transport_zone_id = transport_zone.id
            return transport_zone_id, True
        except Exception,e:
            return "TransportZone -  %s Transport Zone %s creation failed with %s"%(self.zone_type,self.display_name,e) , False



def GetComputeCollectionID(logger,stub_config,clusterlist):
    """

    @param logger:
    @param stub_config: vmware.vapi.bindings.stub.StubConfiguration
    @param clusterlist: Array of Cluster Name
    @return: Tuple of Compute Collection ID Array and Error
    """
    cluster_ids = []

    error = []


    for cluster in clusterlist:
        try:
            computecollections_client = fabric_client.ComputeCollections(stub_config)
            computecollection = computecollections_client.list(display_name=cluster)
            compute_id = computecollection.results[0].external_id
            logger.info("GetComputeCollectionID - The compute ID for %s cluster is %s"%(cluster,compute_id))
            cluster_ids.append(compute_id)
        except Exception,e:
            error.append("Error while getting %s compute id %s"%(cluster,e))

    return cluster_ids , error


def AutoInstallNSX(logger,stub_config,compute_id_lists):
    """

    @param stub_config: vmware.vapi.bindings.stub.StubConfiguration
    @param compute_id_lists: Array of Compute ID List
    @return:
    """
    cc_fab_client = fabric_client.ComputeCollectionFabricTemplates(stub_config)
    i=0
    success = {}
    error = {}


    for compute_id in compute_id_lists:
        try:
            compute_collection_fabric_template_spec = model_client.ComputeCollectionFabricTemplate(
                display_name="compute_cluster_fabric_%s"%i,
                auto_install_nsx=True,
                compute_collection_id=compute_id)

            i += 1

            cc_new = cc_fab_client.create(compute_collection_fabric_template_spec)

            logger.info ("AutoInstallNSX - Initiating on %s - Response %s"%(compute_id,str(cc_new)))
            success[compute_id] = "AutoInstallNSX - Successfully initiated NSX components Installation."

        except Exception,e:
            logger.error("AutoInstallNSX - Failed Installing NSX components on %s cluster due to error %s."%(compute_id,e))
            error[compute_id] = "AutoInstallNSX - Failed Installing NSX components on %s cluster due to error %s."%(compute_id,e)


    logger.info("AutoInstallNSX - Getting Status of Installation")

    discover_nodes_client = fabric_client.DiscoveredNodes(stub_config)
    fabric_nodes_client = fabric_client.Nodes(stub_config)
    node_status_client = nodes_client.Status(stub_config)

    cluster_hosts = {}
    all_hosts = []

    for compute_id in compute_id_lists:
        host_name = []
        discovered_nodes = discover_nodes_client.list(parent_compute_collection=compute_id).results
        for discovered_node in discovered_nodes:
            host_display_name = discovered_node.display_name
            host_name.append(host_display_name)
            all_hosts.append(host_display_name)
        cluster_hosts[compute_id] = host_name

    host_nsx_install = {}
    hostlength = len(all_hosts)
    checked_length = 0
    loop = True

    while (loop):
        success_failed = []
        for host in all_hosts:
            host_nsx_install[host] = "INSTALL_FAILED"  # Inigialized with failed status. Thsi doesnot mean the NSX instal has failed.
            node_result = fabric_nodes_client.list(display_name=host).results[0]
            node_id = node_result.convert_to(model_client.Node).id
            node_status = node_status_client.get(node_id).host_node_deployment_status
            if node_status == "INSTALL_SUCCESSFUL":
                logger.info ("CheckNSXFabricInstall - %s - Successful" % (host))
                host_nsx_install[host] = "INSTALL_SUCCESSFUL"
                success_failed.append(host)
                checked_length = checked_length + 1
            elif node_status == "INSTALL_FAILED":
                logger.info ("CheckNSXFabricInstall - %s - Failed" % (host))
                checked_length = checked_length + 1
                success_failed.append(host)
            else:
                logger.info("CheckNSXFabricInstall - %s - %s" % (host, node_status))



        if checked_length == hostlength:
            loop = False
        else:
            logger.info("Sleeping for 75 seconds before Next Polling")
            if success_failed:
                for item in success_failed:
                    all_hosts.remove(item)
            time.sleep(75)



    error_host = {}

    for compute, host_list in cluster_hosts.iteritems():
        for host in host_list:
            if host_nsx_install[host] != "INSTALL_SUCCESSFUL":
                error_host[host] = compute

    return success,error,error_host




def CreateTransportNodes(logger,stub,ip_pool_id,pnic,transport_zone_id,compute_collection_ids,host_switch_name="OverlaySwitch"):
    """

    @param logger:
    @param stub: vmware.vapi.bindings.stub.StubConfiguration
    @param ip_pool_id: VTEP Pool ID
    @param pnic: vmnic of Host on which VTEP Traffic would flow.
    @param transport_zone_id: Transport Zone ID
    @param compute_collection_ids: Array of cluster ids.
    @param host_switch_name: The virtual switch name that would be created across Transport Node Hosts.
    @return: Dictionary of Host and Transport Node Creation status.
    """

    compute_tnode = {}

    i=1

    tn_ids_dict = {}

    status = False

    for compute_collection_id in compute_collection_ids:

        logger.info ("Initialize Creation of Transport Node for compute id %s"%compute_collection_id)

        cluster_transportnode = nsx_client.ComputeCollectionTransportNodeTemplates(stub)
        ip_assignment_spec = model_client.StaticIpPoolSpec(ip_pool_id=ip_pool_id,
                                                           resource_type='StaticIpPoolSpec')
        pnic_spec = model_client.Pnic(device_name=pnic, uplink_name="uplink-1")
        host_switches = model_client.StandardHostSwitch(host_switch_name=host_switch_name,
                                                        ip_assignment_spec=ip_assignment_spec, pnics=[pnic_spec])
        hostswitchspec = model_client.StandardHostSwitchSpec(host_switches=[host_switches],
                                                             resource_type='StandardHostSwitchSpec')
        tz_endpoints = model_client.TransportZoneEndPoint(transport_zone_id=transport_zone_id)
        cluster_transport_node_spec = model_client.ComputeCollectionTransportNodeTemplate(
            description=None,
            display_name="Cluster_VTEP_Transport_Node_%s"%i,
            compute_collection_ids=[compute_collection_id],
            host_switch_spec=hostswitchspec,
            network_migration_spec_ids=None,
            transport_zone_endpoints=[tz_endpoints])

        i = i+2

        tn_result = cluster_transportnode.create(cluster_transport_node_spec)

        tn_ids_dict[compute_collection_id] = tn_result.id

        #tz_state = model_client.TransportNodeTemplateState(transport_node_id=tn_id)

    tz_state_client = compute_collection_transport_node_templates_client.State(stub)



    for compute_collection_id in tn_ids_dict:

        tn_id = tn_ids_dict[compute_collection_id]

        host_node_failure = []
        host_node_success = []

        looping = True
        no_nodes = tz_state_client.list(tn_id).results[0]

        loop = len(no_nodes.template_states)

        while (loop > 0):
            logger.info("Sleeping for 60 seconds before initializing check for transport nodes creation")
            time.sleep(60)

            tn_state_result = tz_state_client.list(tn_id).results[0]

            tn_compute =  tn_state_result.compute_collection_id

            logger.info ("Getting Node State for Cluster %s"%tn_compute)


            #print "Loop Value ----------------------------------------------->>>>>>>>> %s"%loop

            hostnodes = tn_state_result.template_states
            for hostnode in hostnodes:
                if hostnode.node_id in host_node_failure or hostnode.node_id in host_node_success:
                    continue
                elif hostnode.state in ['FAILED_TO_REALIZE', 'FAILED_TO_CREATE'] :
                    logger.info ("Transport Node creation Failed for Host %s " % (hostnode.node_id))
                    host_node_failure.append(hostnode.node_id)
                    loop = loop -1
                elif hostnode.state ==  'IN_PROGRESS':
                    logger.info ("Transport Node creation Host %s IN_PROGRESS" % (hostnode.node_id))
                elif hostnode.state == 'SUCCESS':
                    logger.info ("Transport Node creation Success for Host %s."%(hostnode.node_id))
                    host_node_success.append(hostnode.node_id)
                    loop = loop -1

        compute_tnode[compute_collection_id] = {"success":host_node_success,"failure":host_node_failure}

    status = True

    return compute_tnode , status



