from install import RemoteInstaller

def install(remoteInstaller, setup, install_path):
    install_cmd = '{0} /S /D={1}'.format(setup, install_path)
    return remoteInstaller.install(install_cmd)

def uninstall(remoteInstaller, uninstaller, install_path):
    uninstall_cmd = '{0}/{1} /S'.format(install_path, uninstaller)
    return remoteInstaller.uninstall(uninstall_cmd)