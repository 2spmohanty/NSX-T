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

import requests
import paramiko
from vmware.vapi.lib import connect
from vmware.vapi.security.user_password import \
    create_user_password_security_context
from vmware.vapi.stdlib.client.factories import StubConfigurationFactory
import time




def stub_configuration(nsx_ip,nsx_user,nsx_pass):
    stub_config = None
    try:
        session = requests.session()
        session.verify = False
        nsx_url = 'https://%s:%s' % (nsx_ip, 443)
        connector = connect.get_requests_connector(
            session=session, msg_protocol='rest', url=nsx_url)
        stub_config = StubConfigurationFactory.new_std_configuration(connector)
        security_context = create_user_password_security_context(nsx_user, nsx_pass)
        connector.set_security_context(security_context)
    except Exception,e:
        stub_config = None
        raise Exception("Could not get Stub for NSX %s"%nsx_ip)

    return stub_config


def get_certificate_value(logger,vcUrl,root_user,root_pass):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(vcUrl, username=root_user, password=root_pass)
        cert_cmd = "openssl x509 -in /etc/vmware-vpx/ssl/rui.crt -fingerprint -sha256 -noout"
        stdin, stdout, stderr = ssh.exec_command(cert_cmd)
        while not stdout.channel.exit_status_ready():
            time.sleep(2)
        certValue = stdout.readlines()[0].strip().split('=')[-1]
        logger.info("THREAD - get_certificate_value - The Certificate for VC %s "%certValue)
        return certValue
    except Exception, e:
        logger.error("THREAD - get_certificate_value - Error while Certificate for VC %s "%str(e))
    finally:
        ssh.close()

