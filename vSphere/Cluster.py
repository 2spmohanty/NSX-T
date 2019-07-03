__author__ = 'smrutim'

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

from logging import error, warning, info, debug
from Datacenter import GetAllClusters,GetClusters,GetCluster


#log handler

def generate_logger():
    import logging
#    PROJECT_DIR="/home/vmlib/spm/nsx"
#    LOG_FILENAME = os.path.join(PROJECT_DIR, "mylog.log")
    FORMAT = "%(asctime)s : %(message)s"
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    # Reset the logger.handlers if it already exists.
    if logger.handlers:
        logger.handlers = []
#    fh = logging.FileHandler(LOG_FILENAME)
    ch = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
#    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
#    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


logger=generate_logger()

def GetDatastoreMob(hostMor,datastore_name):
    datastores = hostMor.datastore
    for datastore in datastores:
        if datastore.info.name == datastore_name:
            return datastore
    return None


def GetHostNetworkMob(hostMor,network_name):
    networks = hostMor.network
    for network in networks:

        if network.name == network_name:
            return network
    return None



def GetHostsMob(datacenter, clusterName=None, hostName= None, connectionState=None):
    """
    Return list of host objects from given cluster name.

    @param datacenter: datacenter object
    @type datacenter: Vim.Datacenter
    @param clusterName: cluster name
    @type clusterName: string
    @param connectionState: host connection state ("connected", "disconnected", "notResponding"), None means all states.
    @type connectionState: string
    """

    if clusterName != None:
        hosts =  GetHostsInClusters(datacenter, [clusterName], connectionState)
        for h in hosts:
            if h.name == hostName:
                return h
    else:
        error("clusterName is NoneType")
        return

def GetHostsInCluster(datacenter, clusterName=None, connectionState=None):
    """
    Return list of host objects from given cluster name.

    @param datacenter: datacenter object
    @type datacenter: Vim.Datacenter
    @param clusterName: cluster name
    @type clusterName: string
    @param connectionState: host connection state ("connected", "disconnected", "notResponding"), None means all states.
    @type connectionState: string
    """

    if clusterName != None:
        return GetHostsInClusters(datacenter, [clusterName], connectionState)
    else:
        error("clusterName is NoneType")
        return

def GetHostsInClusters(datacenter, clusterNames=[], connectionState=None):
    """
    Return list of host objects from given cluster names.

    @param datacenter: datacenter object
    @type datacenter: Vim.Datacenter
    @param clusterNames: cluster name list
    @type clusterNames: string[]
    @param connectionState: host connection state ("connected", "disconnected", "notResponding"), None means all states.
    @typr connectionState: string
    """

    if len(clusterNames) == 0:
        clusterObjs = GetAllClusters(datacenter)
    else:
        clusterObjs = GetClusters(datacenter, clusterNames)

    hostObjs = []
    if connectionState == None:
        hostObjs = [h for cl in clusterObjs for h in cl.host]
    else:
        hostObjs = [h for cl in clusterObjs for h in cl.host if h.runtime.connectionState == connectionState]

    return hostObjs



def GetAllResourcePool(datacenter):

    """
    Return list of resourcePool objects from given datacenter.

    @param datacenter: datacenter object
    @type datacenter: Vim.Datacenter
    """

    clusterListObj = GetAllClusters(datacenter)
    respool = []
    for c in clusterListObj:
        respool.append(c.resourcePool)
        """
        for r in c.resourcePool:
            respool.append(r.resourcePool)
        """
    return respool