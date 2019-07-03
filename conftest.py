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



def pytest_configure():
    nsxt_variable = {}
    nsxt_variable["stub_config"] = None
    nsxt_variable["compute_manager_id"] = None
    nsxt_variable["si"] = None
    nsxt_variable["controller_dc"] = None
    nsxt_variable["vtep_pool_id"] = None
    nsxt_variable["overlay_tz_id"] = None
    nsxt_variable["compute_collection_ids"] = []
    nsxt_variable["transport_overlay_switch_name"] = None
    nsxt_variable["edge_id"] = None
    nsxt_variable["edge_uplink_profile_id"] = None
    nsxt_variable["edge_tn_result_id"] = None
    nsxt_variable["edge_cluster_id"] = None
    nsxt_variable["dhcp_server_profile_id"] = None
    nsxt_variable["dhcp_server_id"] = None
    nsxt_variable["logical_switch_id"] = None

    return nsxt_variable

