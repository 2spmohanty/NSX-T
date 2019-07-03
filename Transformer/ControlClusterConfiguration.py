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
import com.vmware.nsx.cluster.nodes_client as nodes_client
import time
import com.vmware.nsx.cluster.nodes.deployments_client as deployments_client

class Controller():

    def __init__(self,allow_ssh_root_login,compute_id,default_gateway_addresses,dns_servers,enable_ssh,host_id,
                 hostname,management_network_id,ntp_servers,storage_id,vc_id,form_factor,ipaddress,prefix):
        """

        @param allow_ssh_root_login: Boolean value to allow root login
        @param compute_id: The MOB ID of Cluster on which the Controller would be deployed
        @param default_gateway_addresses: Array of  default gateway
        @param dns_servers: Array of DNS Server
        @param enable_ssh: Boolean value to allow ssh
        @param host_id: Host MOB value on which the control cluster would be deployed
        @param hostname: the FQDN Name of the control cluster
        @param management_network_id: The Management Network on which the COntrol CLuster will be Deployed
        @param ntp_servers: Array of Time Servers
        @param storage_id: The Datastore MOB ID.
        @param vc_id: The ID of compute manager as registered in the NSX Manager
        @param form_factor: The Size of control cluster Small, Medium, Large
        @param ipaddress: IP Address of Controller
        @param prefix: Network Subnet Proefic
        """
        self.allow_ssh_root_login = allow_ssh_root_login
        self.compute_id = compute_id
        self.default_gateway_addresses = default_gateway_addresses
        self.dns_servers = dns_servers
        self.enable_ssh = enable_ssh
        self.host_id = host_id
        self.hostname = hostname
        self.management_network_id = management_network_id
        self.ntp_servers = ntp_servers
        self.storage_id = storage_id
        self.vc_id = vc_id
        self.form_factor = form_factor
        self.ip_addresses = ipaddress
        self.prefix_length = prefix

    def deployment_requests_spec(self):
        """

        @return: Controller Deployment Spec
        """

        user_setting = model_client.NodeUserSettings(audit_password='Admin!23', audit_username='admin',
                                                     cli_password='Admin!23', cli_username='admin',
                                                     root_password='Admin!23')

        management_port_subnet = model_client.IPSubnet(ip_addresses=[self.ip_addresses], prefix_length=self.prefix_length)





        VsphereClusterNodeVMDeploymentConfig0 = model_client.VsphereClusterNodeVMDeploymentConfig(
            allow_ssh_root_login=True,
            compute_id=self.compute_id,
            default_gateway_addresses=self.default_gateway_addresses,
            dns_servers=self.dns_servers,
            enable_ssh=self.enable_ssh,
            host_id=self.host_id,
            hostname=self.hostname,
            management_network_id=self.management_network_id,
            management_port_subnets= [management_port_subnet],
            ntp_servers=self.ntp_servers,
            storage_id=self.storage_id,
            vc_id=self.vc_id,
            placement_type='VsphereClusterNodeVMDeploymentConfig')

        deployment_request = model_client.ClusterNodeVMDeploymentRequest(
            deployment_config=VsphereClusterNodeVMDeploymentConfig0,
            form_factor=self.form_factor,
            roles=['CONTROLLER'],
            user_settings=user_setting)

        return deployment_request



def CreateControllerCluster(logger,stub_config,deployment_request_array):
    """
    @param stub_config :  vmware.vapi.bindings.stub.StubConfiguration
    @param deployment_request_array: Array of Controller().deployment_requests_spec
    @return: Controller IDs
    """

    clustering_config = model_client.ControlClusteringConfig(join_to_existing_cluster=False, shared_secret='Admin!23',
                                                             clustering_type='ControlClusteringConfig')

    add_cluster_node_vms = model_client.AddClusterNodeVMInfo(clustering_config=clustering_config,
                                                             deployment_requests=deployment_request_array)

    ControllerNodes = nodes_client.Deployments(stub_config)

    logger.info("Creating controller ...")

    ClusterNodeVMDeploymentRequestList = ControllerNodes.create(add_cluster_node_vms)

    controllerResults = ClusterNodeVMDeploymentRequestList.results

    ControllerNodesStatus = deployments_client.Status(stub_config)

    check_controller = 0

    controller_fail_status = ['VM_CLUSTERING_FAILED', 'VM_DEPLOYMENT_FAILED', 'VM_POWER_ON_FAILED']

    successful_cluster = []
    failed_cluster = []

    while check_controller != len(deployment_request_array):
        for controller in controllerResults:
            controller_vm_id = controller.vm_id
            logger.info ("Getting status for controller VM %s." % controller_vm_id)
            status = ControllerNodesStatus.get(controller_vm_id).status
            logger.info ("The status if controller %s is %s" % (controller_vm_id, status))
            if status == 'VM_CLUSTERING_SUCCESSFUL':
                check_controller = check_controller + 1
                controllerResults.remove(controller)
                successful_cluster.append(controller)
            elif status in controller_fail_status:
                check_controller = check_controller + 1
                controllerResults.remove(controller)
                failed_cluster.append(controller)
            logger.info("Sleeping for 90 seconds before polling for controller status.")
            time.sleep(90)

    if failed_cluster:
        logger.error("Controllers %s deployment failed" % failed_cluster)

    if successful_cluster:
        logger.info ("Proceeding with Host Prep as %s controllers got deployed" % len(successful_cluster))
    else:
        raise Exception("Failed deploying controllers. Quitting subsequent steps.")

    return successful_cluster , failed_cluster



########################


