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

import pytest
import time
from CustomLogger import CustomLogging
from Data import property
from Transformer import ComputeManagerConfiguration,Utility,ControlClusterConfiguration, TransportConfiguration, EdgeConfiguration
import json
import requests
from vSphere import Vcenter, Datacenter, Cluster
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


#Create Logger for the Test
logger = CustomLogging.generate_logger(log_file=property.LOG_FILE_NAME)

@pytest.mark.dependency()
def test_GetStub():
    logger.info("TEST - Getting NSX Stub")
    pytest.stub_config = Utility.stub_configuration(property.NSX_MANAGER_IP,property.NSX_MANAGER_USER,property.NSX_MANAGER_PASS)
    assert pytest.stub_config is not None, "Getting NSX Stub not successful."



@pytest.mark.dependency(depends=["test_GetStub"])
def test_RegisterComputeManager():
    logger.info("TEST - Registering NSX with VC")
    compute_manager_id,status = ComputeManagerConfiguration.RegisterComputerManager(logger,pytest.stub_config,property.COMPUTE_MANAGER_IP,
                                                                                    property.COMPUTE_MANAGER_USER,property.COMPUTE_MANAGER_PASS,
                                                                                    property.COMPUTE_MANAGER_LOCAL_USER,property.COMPUTE_MANAGER_LOCAL_PASS)
    assert status == True , "Could Not Register vCenter to NSX"
    pytest.compute_manager_id = compute_manager_id



@pytest.mark.dependency(depends=["test_GetStub","test_RegisterComputeManager"])
@pytest.mark.skipif(property.SKIP_CONTROLLER_CREATION,reason="This Test Bed Doesnot Need Controllers Deployment")
def test_CreateController():
    logger.info("TEST - Deploying Controller.")
    deployment_spec = []
    controller_json = json.dumps(property.CONTROL_CLUSTER)
    controller_data = json.loads(controller_json)
    datacenter = property.CONTROLLER_DATACENTER

    for controller in controller_data:
        logger.info("Creating Controller Deployment Spec for Controller %s"%controller)
        controller_data_variable = controller_data[controller]

        host = controller_data_variable["CONTROLLER_host"]
        datastore = controller_data_variable["CONTROLLER_datastore"]
        cluster = controller_data_variable["CONTROLLER_cluster"]
        mgmt_nw = controller_data_variable["CONTROLLER_management_network"]

        audit_pass = controller_data_variable["CONTROLLER_audit_password"]
        hostname = controller_data_variable["CONTROLLER_hostname"]
        root_pass = controller_data_variable["CONTROLLER_root_password"]
        prefix = controller_data_variable["CONTROLLER_prefix_length"]
        form_factor = controller_data_variable["CONTROLLER_form_factor"]
        ip_address = controller_data_variable["CONTROLLER_ip_addresses"]
        gw = controller_data_variable["CONTROLLER_default_gateway_addresses"]
        cli_user = controller_data_variable["CONTROLLER_cli_username"]
        ntp = controller_data_variable["CONTROLLER_ntp_servers_fqdn"]
        cli = controller_data_variable["CONTROLLER_cli_password"]
        dns = controller_data_variable["CONTROLLER_dns_servers"]
        audit_user = controller_data_variable["CONTROLLER_audit_username"]

        pytest.si = Vcenter.Login(property.COMPUTE_MANAGER_IP, property.COMPUTE_MANAGER_LOCAL_USER, property.COMPUTE_MANAGER_LOCAL_PASS, port=443)

        controller_dc = Datacenter.GetDatacenter(datacenter,pytest.si)

        cluster_mob = Datacenter.GetCluster(controller_dc, cluster, pytest.si)

        cluster_mob_id = str(cluster_mob).strip('\'').split(':')[1]

        logger.info("Controller %s Cluster %s"%(controller,cluster_mob_id))

        host_mob = Cluster.GetHostsMob(controller_dc, cluster, host)

        host_mob_id =  str(host_mob).strip('\'').split(':')[1]

        logger.info("Controller %s Host %s" % (controller, host_mob_id))

        network_mob = Cluster.GetHostNetworkMob(host_mob, mgmt_nw)

        network_mob_id =  str(network_mob).strip('\'').split(':')[1]

        logger.info("Controller %s Network %s" % (controller, network_mob_id))

        ds_mob = Cluster.GetDatastoreMob(host_mob, datastore)

        ds_mob_id = str(ds_mob).strip('\'').split(':')[1]

        logger.info("Controller %s Datastore %s" % (controller, ds_mob_id))

        controller_spec = ControlClusterConfiguration.Controller(True,cluster_mob_id,gw,dns,True,host_mob_id,
                                                                 hostname,network_mob_id,ntp,ds_mob_id,
                                                                 pytest.compute_manager_id,form_factor,ip_address,prefix)



        logger.info("Network Mob ID %s"%controller_spec.management_network_id)


        controller_spec_deployment = controller_spec.deployment_requests_spec()

        deployment_spec.append(controller_spec_deployment)

    logger.info("Deployment Spec %s"%deployment_spec)

    logger.info("Starting to Deploy control cluster")

    success,fail = ControlClusterConfiguration.CreateControllerCluster(logger,pytest.stub_config,deployment_spec)

    assert len(success) > 0 , "Control Cluster Deployed"



@pytest.mark.dependency(depends=["test_GetStub","test_RegisterComputeManager"])
def test_CreateVtepPool():
    logger.info("TEST - Create VTEP Pool.")
    vtep_pool_id, vtep_status = TransportConfiguration.CreateVtepIpPool(logger, pytest.stub_config, property.VTEP_POOL_NAME,
                                                                        property.VTEP_START_IP, property.VTEP_END_IP, property.VTEP_NETWORK)
    assert vtep_status == True , "VTEP IP Pool could not be created"
    pytest.vtep_pool_id = vtep_pool_id




@pytest.mark.dependency(depends=["test_CreateVtepPool"])
def test_CreateOverlayTransportZones():
    logger.info("TEST - Create Transport Zones.")

    for item in property.TRANSPORT_ZONES:
        pytest.transport_overlay_switch_name = item
        tz_data = property.TRANSPORT_ZONES[item]
        tz_type = tz_data["Type"]
        tz_name = tz_data["display_name"]
        overlay_tz = TransportConfiguration.TransportZone(pytest.stub_config, tz_type, tz_name, pytest.transport_overlay_switch_name,
                                                          description="Create a Overlay TransportZone")
        pytest.overlay_tz_id, overlay_tz_status = overlay_tz.create()

        assert overlay_tz_status == True, "Overlay Transport Zone copuld not be created."



@pytest.mark.dependency(depends=["test_CreateOverlayTransportZones"])
def test_GetComputeCollections():
    logger.info("TEST - Get Compute Collections to be Prepped with NSX")
    pytest.compute_collection_ids , error = TransportConfiguration.GetComputeCollectionID(logger, pytest.stub_config, property.CLUSTER_LIST)
    assert len(pytest.compute_collection_ids) > 0 , "Not able to obtain compute ids for Prepping Clusters with NSX."
    if error:
        logger.error(error)


@pytest.mark.dependency(depends=["test_GetComputeCollections"])
def test_AutoInstallNSX():
    logger.info("TEST - Auto Install NSX on the Hosts in the clusters specified")
    success, error, error_host = TransportConfiguration.AutoInstallNSX(logger,pytest.stub_config,pytest.compute_collection_ids)
    if error:
        logger.error(error)
    if error_host:
        logger.error(error_host)
    assert len(success) > 0 , "Could not install NSX Fabric in any of the cluster's hosts."


@pytest.mark.dependency(depends=["test_AutoInstallNSX"])
def test_AddTransportNodes():
    logger.info("TEST - Add Hosts to Transport Nodes")
    transport_node_data, status = TransportConfiguration.CreateTransportNodes(logger, pytest.stub_config, pytest.vtep_pool_id, property.TRANSPORT_NODE_NIC,
                                                pytest.overlay_tz_id, pytest.compute_collection_ids,host_switch_name=pytest.transport_overlay_switch_name)
    assert status == True , "Failure in Adding Hosts as Transport Nodes."



@pytest.mark.dependency(depends=["test_AddTransportNodes"])
def test_DeployEdge():
    logger.info("TEST - Deploy Edge ")

    edge_dc = Datacenter.GetDatacenter(property.EDGE_DEPLOYMENT_DATACENTER, pytest.si)

    cluster_mob = Datacenter.GetCluster(edge_dc, property.EDGE_DEPLOYMENT_CLUSTER_NAME, pytest.si)

    cluster_mob_id = str(cluster_mob).strip('\'').split(':')[1]

    logger.info("Edge Appliance Cluster %s" % (cluster_mob_id))

    host_mob = Cluster.GetHostsMob(edge_dc, property.EDGE_DEPLOYMENT_CLUSTER_NAME, property.EDGE_DEPLOYMENT_HOST)

    host_mob_id = str(host_mob).strip('\'').split(':')[1]

    logger.info("Edge Host %s" % ( host_mob_id))

    network_mob = Cluster.GetHostNetworkMob(host_mob, property.EDGE_MGMT_NETWORK)

    network_mob_id = str(network_mob).strip('\'').split(':')[1]

    logger.info("Edge Network %s" % (network_mob_id))

    ds_mob = Cluster.GetDatastoreMob(host_mob, property.EDGE_DATASTORE)

    ds_mob_id = str(ds_mob).strip('\'').split(':')[1]

    logger.info("Edge Datastore %s" % (ds_mob_id))

    data_network_mob_ids = []

    for nw in property.EDGE_DATA_NETWORKS:
        data_network_mob = Cluster.GetHostNetworkMob(host_mob, nw)
        data_network_mob_id = str(data_network_mob).strip('\'').split(':')[1]
        data_network_mob_ids.append(data_network_mob_id)


    new_edge = EdgeConfiguration.Edge(pytest.stub_config,property.EDGE_SIZE,property.EDGE_HOSTNAME,property.EDGE_IP,property.EDGE_NETWORK_PREFIX,property.EDGE_DEFAULT_GW,
                 property.EDGE_DNS_SERVERS,cluster_mob_id,data_network_mob_ids,host_mob_id,network_mob_id,property.EDGE_NTP_SERVERS,ds_mob_id,pytest.compute_manager_id)

    pytest.edge_id, final_edge = new_edge.create()

    assert final_edge == True , "Edge Deployed Successfully"


@pytest.mark.dependency(depends=["test_DeployEdge"])
def test_EdgeUplinkProfile():
    logger.info("TEST - Create Edge Uplink Profile")
    pytest.edge_uplink_profile_id = EdgeConfiguration.CreateEdgeUplinkProfile(pytest.stub_config)
    assert pytest.edge_uplink_profile_id is not None, "Edge Uplink Profile Could not be created"


@pytest.mark.dependency(depends=["test_EdgeUplinkProfile"])
def test_EdgeTransportNode():
    logger.info("TEST - Add Edge as Transport Node")
    pytest.edge_tn_result_id, status = EdgeConfiguration.MarkEdgeAsTransportNode(logger, pytest.stub_config, pytest.vtep_pool_id,
                                                                                 pytest.edge_uplink_profile_id, pytest.overlay_tz_id, pytest.edge_id)
    assert status == True , "Edge Node could be added as a Transport Node."


@pytest.mark.dependency(depends=["test_EdgeTransportNode"])
def test_CreateEdgeCluster():
    logger.info("TEST - Create Edge Cluster")
    pytest.edge_cluster_id, status = EdgeConfiguration.CreateEdgeCluster(logger, pytest.stub_config, pytest.edge_tn_result_id)
    assert status == True , "Could not Create Edge cluster"



@pytest.mark.dependency(depends=["test_CreateEdgeCluster"])
def test_CreateDHCPServerProfile():
    logger.info("TEST - Create DHCP Server Profile")
    pytest.dhcp_server_profile_id, status = EdgeConfiguration.CreateDHCPServerProfile(logger,pytest.stub_config,pytest.edge_cluster_id)
    assert status == True ,  "DHCP Server profile creation failed."




@pytest.mark.dependency(depends=["test_CreateDHCPServerProfile"])
def test_CreateDHCPServer():
    logger.info("TEST - Create DHCP Server.")
    pytest.dhcp_server_id, status = EdgeConfiguration.CreateDHCPServer(logger, pytest.stub_config, property.DHCP_SERVER_IP, pytest.dhcp_server_profile_id)
    assert status == True , "DHCP Server could not be created"



@pytest.mark.dependency(depends=["test_CreateDHCPServer"])
def test_CreateDHCPPool():
    logger.info("TEST - Create DHCP Server IP Pool")
    pytest.dhcp_pool_id, status = EdgeConfiguration.CreateDHCPPool(logger, pytest.stub_config,
                                                                   property.DHCP_POOL_START_IP, property.DHCP_POOL_END_IP,
                                                                   property.DHCP_GW_IP, pytest.dhcp_server_id)
    assert status == True , "Could not create DHCP Pool"



@pytest.mark.dependency(depends=["test_CreateDHCPPool"])
def test_CreateDHCPLogicalSwitch():
    logger.info("TEST - Create Logical Switch for DHCP")
    pytest.logical_switch_id, status = EdgeConfiguration.CreateLogicalSwitch(logger, pytest.stub_config, property.DHCP_SWITCH, pytest.overlay_tz_id)
    assert  status == True, "Logical Switch for DHCP Service could not be created."



@pytest.mark.dependency(depends=["test_CreateDHCPLogicalSwitch"])
def test_CreateDHCPPortOnLogicalSwitch():
    logger.info("TEST - Create Port on Logical Switch for DHCP")
    pytest.dcp_port_id, status = EdgeConfiguration.AttachDhcpToLS(logger,pytest.stub_config,pytest.dhcp_server_id,pytest.logical_switch_id)
    assert status == True, "Could not attach Port to DHCP Logical Switch"

