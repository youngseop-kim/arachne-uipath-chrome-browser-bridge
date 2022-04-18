
'''
> notice
as the chrome extension which contains file or folder starting with underscore cannot be executed,
please do not remove the line 'sys.dont_write_bytecode = True'.
it will make the python interpreter avoid to create byte compiled codes like '__pycache__' folder
when the interperter try to import individual modules.
'''

import sys
sys.dont_write_bytecode = True

if __name__ == '__main__':

    from os.path import expandvars
    from os.path import join

    from socket import socket
    from socket import AF_INET
    from socket import SOCK_STREAM

    from cbnmplib.communicate import _write
    from cbnmplib.communicate import _read
    
    # === warning! these variables should be the same with your host application === 

    # set host name
    host = 'com.arachne.uipath.chrome.browser.bridge.host'

    # set logging directory
    ldirectory = rf'%userprofile%\.arachne-uipath\.settings\.chrome-extension\{host}'

    # set struct format following the native messaging protocol
    fmt = '=I'

    # set encoding following the native messaging protocol
    enc = 'utf-8'

    # === warning! these variables should be the same with your host application === 

    # set javascript
    javascript = 'function exampleFunction() {return "hello";}; exampleFunction();'

    # set message
    message = {'key':'', 'value':javascript}

    # set port 
    # do not open in additional mode, 
    # it could cause hanging issue on the host application
    with open(join(expandvars(ldirectory), 'port.log'), mode='r', encoding=enc) as fd:
        port = _read(fd, fmt=fmt, enc=enc)

    # open socket
    with socket(AF_INET, SOCK_STREAM) as client_socket:
        # please read below this message first before opening the port.
        # we know that where the port opens at depends on the user and it cannot be forced.
        # however, we do not recommend opening the port in public.
        # even if you have to open the port in public, 
        # please you should aware of that it is extremely dangerous behavior.
        client_socket.connect(tuple(port[1:]))

        # set socket timeout
        client_socket.settimeout(5)

        # send the request message
        _write(client_socket, message, fmt, enc)

        # receive the response message
        recv = _read(client_socket, fmt, enc)

        # let's see how it works
        print('recv :', recv)
        