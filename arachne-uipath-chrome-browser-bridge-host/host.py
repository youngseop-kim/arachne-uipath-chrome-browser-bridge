
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
    from cbnmplib.pipeline import Pipeline
    from cbnmplib.pipeline import serve
    from asyncio import run
    
    # set host name
    host = 'com.arachne.uipath.chrome.browser.bridge.host'

    # set application id
    app = 'dcgmnehcnnncofekjjoikncbikojekje'

    # set application version
    version = '0.1_0'

    # set injection javascript directory
    jsdirectory = rf'%userprofile%\AppData\Local\Google\Chrome\User Data\Default\Extensions\{app}\{version}'

    # set logging directory
    ldirectory = rf'%userprofile%\.arachne-uipath\.settings\.chrome-extension\{host}'

    # open pipeline (local host, free port)
    # please read below this message first before opening the port.
    # we know that where the port opens at depends on the user and it cannot be forced.
    # however, we do not recommend opening the port in public.
    # even if you have to open the port in public, 
    # please you should aware of that it is extremely dangerous behavior.
    with Pipeline(name=host, ldir=ldirectory, jsdir=jsdirectory, addr=('localhost',0,)) as p:

        # serve on pipeline
        run(serve(p))
    