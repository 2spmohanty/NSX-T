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

from pyVmomi import vim

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import traceback
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




def get_obj(content, vimtype, name):
    obj = None
    container = content.viewManager.CreateContainerView(
        content.rootFolder, vimtype, True)
    for c in container.view:
        if c.name == name:
            obj = c
            break
    return obj


def GetDatacenter(name=None, si=None):
    try:
        content = si.RetrieveContent()
        dcObj=get_obj(content, [vim.Datacenter], name)

    except Exception, e:
        logger.error(e)
        raise
    return dcObj


def GetCluster(datacenter=None, clusterName=None, si=None):
    #Get Cluster Objects
    hostFolder = datacenter.hostFolder
    foundCr = None
    clusterListObj = GetAllClusters(datacenter)
    for cr in clusterListObj:
        if cr.name == clusterName:
            foundCr = cr
            logger.debug("\nCluster " + str(cr) + "(" + clusterName +") is found ")
            break
    if foundCr == None:
        logger.error("Cluster [" + clusterName + "] not found in " + datacenter.GetName() + "!!!")
    return foundCr

def GetClusters(datacenter, clusterNames = []):
    """
    Return list of cluster objects from given cluster name.

    @param datacenter: datacenter object
    @type datacenter: Vim.Datacenter
    @param clusterNames: cluster name list
    @type clusterNames: string[]
    """
    foundCr = []
    clusterListObj = GetAllClusters(datacenter)
    logger.debug("'%s' has %d clusters." %(datacenter.name, len(clusterListObj)))
    if len(clusterNames) == 0:
        # equivalent to GetAllClusters()
        if len(clusterListObj) == 0:
            logger.warning("No Cluster found in %s" % (datacenter.name))
            return []
        else:
            return clusterListObj
    else:
        foundCr = [c for c in clusterListObj if c.name in clusterNames]

    if len(foundCr) == 0:
        logger.warning("Cluster '%s' not found in '%s'" % (
            str(clusterNames), datacenter.name))

    return foundCr

def GetAllClusters(datacenter):
    if datacenter == None:
        logger.error("You have to specify datacenter object")
        return []
    elif not (isinstance(datacenter, vim.Datacenter)):
        logger.error(str(datacenter) + " is not a datacenter object")
        return []
    else:
        logger.info("datacenter name: " + datacenter.name)

    hostFolder = datacenter.hostFolder
    allClusterObjList = []
    crs = hostFolder.childEntity
    logger.debug("crs: " + str(crs))

    def WalkFolder(folder, allClusterObjList):
        childEntities = folder.childEntity
        for i in range(len(childEntities)):
            WalkManagedEntity(childEntities[i], allClusterObjList)

    def WalkManagedEntity(entity, allClusterObjList):
        if isinstance(entity, vim.Folder):
            WalkFolder(entity, allClusterObjList)
        elif isinstance(entity, vim.ClusterComputeResource):
            allClusterObjList.append(entity)
    if crs == None:
        return []
    for cr in crs:
        WalkManagedEntity(cr, allClusterObjList)

    return allClusterObjList







