import os
import subprocess
import time
from threading import Timer

class RemoteInstaller(object):
    '''Psexec wrapper for deploy on remote host'''

    _PS_TOOLS_ENV = 'PSTOOLS_PATH'

    @classmethod
    def IsPsTools(self):
        return os.environ.has_key(self._PS_TOOLS_ENV)

    @classmethod
    def GetPsToolsEnv(self):
        return self._PS_TOOLS_ENV

    def _run(self, params):
        start_time = time.time()
        returncode = subprocess.call(params, shell=True)
        print "operation time: {0:.2g} sec".format(time.time() - start_time)
 
        return returncode

    def __init__(self, address, user, password, connectTimeout):
        self._address = address
        self._user = user
        self._password = password
        self._connectTimeout = connectTimeout
        self._psexec = os.environ[self._PS_TOOLS_ENV] + "\PsExec.exe"

    def install(self, params):
        cmd = "\"{0}\" -accepteula -n {4} \\\{1} -h -u {2} -p {3} -f -c {5}".\
        format(self._psexec, self._address, self._user, self._password, self._connectTimeout, params)
        print cmd
        return self._run(cmd)

    def uninstall(self, params):
        cmd = "\"{0}\" -accepteula -n {4} \\\{1} -h -u {2} -p {3} {5}".\
        format(self._psexec, self._address, self._user, self._password, self._connectTimeout, params)
        print cmd
        return self._run(cmd)

if __name__ == "__main__":
    user = 'name'
    pwd = '132456'
    ip = '192.168.1.1'
    ip_incorrect = '10.1.1.1'
    path = 'C:\path'
    uninstaller = 'Uninstall_file'

    installer = RemoteInstaller(ip_incorrect, user, pwd, 5)
    
    uninstall_cmd = '{0}/{1} /S'.format(path, uninstaller)
    installer.uninstall(uninstall_cmd)