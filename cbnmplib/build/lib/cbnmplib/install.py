
'''
install.py
'''

from os.path import join
from os.path import abspath

from winreg import HKEY_CURRENT_USER
from winreg import KEY_ALL_ACCESS
from winreg import REG_SZ
from winreg import ConnectRegistry
from winreg import OpenKey
from winreg import CreateKey
from winreg import DeleteKey
from winreg import CloseKey
from winreg import SetValueEx

NATIVE_MESSAGING_HOSTS = r'SOFTWARE\Google\Chrome\NativeMessagingHosts'

def install_host(host:str, value:str):
    # set key
    path = join(NATIVE_MESSAGING_HOSTS, host)

    # create key
    CreateKey(HKEY_CURRENT_USER, path)

    # open root key
    hkey_root = ConnectRegistry(None, HKEY_CURRENT_USER)

    # open instance key
    hkey_inst = OpenKey(hkey_root, path, 0, KEY_ALL_ACCESS)
    
    # set value (default, reg_sz, file path)
    SetValueEx(hkey_inst, '', 0, REG_SZ, abspath(value))

    # close key
    CloseKey(hkey_inst)


def uninstall_host(host:str):
    # set key
    path = join(NATIVE_MESSAGING_HOSTS, host)

    # open root key
    hkey_root = ConnectRegistry(None, HKEY_CURRENT_USER)

    # open instance key
    hkey_inst = OpenKey(hkey_root, path, 0, KEY_ALL_ACCESS)
    
    # delete key (default)
    DeleteKey(hkey_inst, '')

    # close key
    CloseKey(hkey_inst)
