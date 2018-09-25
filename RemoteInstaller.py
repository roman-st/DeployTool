import sys, os
import argparse
from deploy import RemoteInstaller
from deploy import nsis

usageString = '''\
\rpython RemoteInstaller.py -u user_name -p 123456 -a 192.168.1.1 -i C:\InstallPath -s Setup.exe
python RemoteInstaller.py -u user_name -p 123456 -a 192.168.1.1 -i C:\InstallPath -r Uninstaller.exe
'''

def main():
    parser = argparse.ArgumentParser(description='PsExec wrapper for deploy distribs', usage=usageString)
    parser.add_argument('-u', '--user', type=str, help='User name', required=True)
    parser.add_argument('-p', '--password', type=str, help='Password', required=True)
    parser.add_argument('-a', '--address', type=str, help='Remote host IP address or name', required=True)
    parser.add_argument('-i', '--install', type=str, help='Install path on remote host', required=True)
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-s', '--setup', type=str, help='Setup file name')
    group.add_argument('-r', '--remove', type=str, help='Uninstall file name on remote host')

    args = parser.parse_args()
    
    connectionTimeout = 5
    installer = RemoteInstaller(args.address, args.user, args.password, connectionTimeout)

    if args.setup:
        result =  nsis.install(installer, args.setup, args.install)
        print os.strerror(result)
        return result
    else:
        result = nsis.uninstall(installer, args.remove, args.install)
        if result == 2 or result == 3:
            return 0
        print os.strerror(result)
        return result

if __name__ == "__main__":
    if not RemoteInstaller.IsPsTools():
        print 'Error: Environment variable ' + RemoteInstaller.GetPsToolsEnv() + ' not set'
        exit(1)

    exit(main())

    