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


from pyVim.connect import SmartConnect, Disconnect
import atexit

from logging import error, warning, info, debug

import ssl
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def Login(host, user, pwd, port=443):
    context = ssl._create_unverified_context()
    si = SmartConnect(host=host,user=user,pwd=pwd,port=port,sslContext=context)
    atexit.register(Disconnect, si)
    return si

def wait_for_task(task):
    """ wait for a vCenter task to finish """
    task_done = False
    while not task_done:
        if task.info.state == 'success':
            return task.info.result

        if task.info.state == 'error':
            print "there was an error"
            task_done = True


def AddLicense(si, licensekey):
    licenseManager = si.RetrieveContent().licenseManager
    licenseManager.AddLicense(licensekey)

def AssignLicense(si, entity, licensekey):
    try:
        licenseAssignmentManager = si.RetrieveContent().licenseManager.licenseAssignmentManager
        licenseAssignmentManager.UpdateAssignedLicense(entity, licensekey)
    except Exception, e:
        error(e)

def AssignVCLicense(si, licensekey):
    vcEntity = si.content.about.instanceUuid
    AssignLicense(si, vcEntity, licensekey)

