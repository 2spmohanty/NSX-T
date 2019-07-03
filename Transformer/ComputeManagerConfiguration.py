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
from Utility import get_certificate_value,stub_configuration
import com.vmware.nsx.model_client as model_client
from com.vmware.nsx import fabric_client
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)






def RegisterComputerManager(logger,stub_config,vcUrl,root_user,root_pass,vc_user,vc_pass):
    """

    @param logger:
    @param stub_config:
    @param vcUrl:
    @param root_user:
    @param root_pass:
    @param vc_user:
    @param vc_pass:
    @return:
    """

    try:
        logger.info("Getting Certificate Thumberin from VC %s"%vcUrl)
        certificate_thumbprint = get_certificate_value(logger,vcUrl,root_user,root_pass)
        logger.info("The thumbprint for %s is %s"%(vcUrl,certificate_thumbprint))


        loginCredential = model_client.UsernamePasswordLoginCredential(password=vc_pass,
                                                                      username=vc_user,
                                                                      credential_type='UsernamePasswordLoginCredential',
                                                                      thumbprint=certificate_thumbprint)

        compManagerSpec = model_client.ComputeManager(display_name="TestComputeManagerOne", credential=loginCredential,
                                                      server="10.172.109.23", origin_type='vCenter')

        logger.info("RegisterComputerManager - Resgister Compute Manager %s in NSX Manager."%(vcUrl))

        ComputeManager = fabric_client.ComputeManagers(stub_config)


        NewComputeManager = ComputeManager.create(compManagerSpec)

        return str(NewComputeManager.id) , True

    except Exception,e:

        return "Registration of VC failed with Exception %s"%str(e) , False

