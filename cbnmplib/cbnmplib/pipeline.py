
'''
pipeline.py
'''

from logging import Logger
from logging import Formatter
from logging import FileHandler

from os import getpid
from os import kill
from os import makedirs
from os import remove
from os import O_BINARY

from os.path import join
from os.path import expandvars

from sys import stdin
from sys import stdout

from asyncio import get_running_loop
from asyncio import gather

from socket import socket
from socket import AF_INET
from socket import SOCK_STREAM

from time import sleep
from uuid import uuid4
from struct import error
from msvcrt import setmode
from datetime import datetime
from traceback import format_tb

from cbnmplib.communicate import _read
from cbnmplib.communicate import _write
from cbnmplib.communicate import NativeMessage

from typing import NewType
from typing import Iterable
from typing import Tuple
from typing import Union
from types import TracebackType
from socket import SocketType
from io import TextIOWrapper

PipelineType = NewType(
    'Pipeline',
    Tuple[Tuple[str,int],str,str,float,float,str,str]
    )

class Pipeline:
    '''
    [class pipeline]
    before using the pipeline,
    you need to recognize that
    the process which is built with the pipeline
    should be folked under the chrome browser.
    '''
    
    def __init__(
            self,
            name:str,
            jsdir:str='',
            addr:Tuple[str,int]=('localhost',0,),
            fmt:str='=I', 
            enc:str='utf-8',
            expire:float=10.0,
            timeout:float=10.0,
            ldir:str='',
            lfmt:str='%(asctime)s [%(levelname)s] %(message)s',
            ):
        '''

        '''
        # === pipeline === #

        # set pid
        self._pid = getpid()

        # set injection javascript directory
        self._jsdir = expandvars(jsdir)

        # set address (host & port)
        self._addr = addr

        # set struct format
        self._fmt = fmt

        # set encoding
        self._enc = enc

        # set timeout (float)
        self._timeout = timeout

        # set expire (float)
        self._expire = expire

        # set last ping (datetime)
        self._last_ping = datetime.now()

        # set internal interface (stdin & stdout)
        self._internal = [stdin, stdout]

        # set external interface (socket)
        self._external = socket(AF_INET, SOCK_STREAM)

        # set external interface accepted sockets {uuid : socket}
        self._external_accepted = {}

        # === logging === #

        # set logger directory
        self._ldir = expandvars(ldir)

        # create logger directory
        makedirs(self._ldir, exist_ok=True)

        # set logger path : port logging
        self._lppath = join(
            self._ldir, 
            'port.log'
            )

        # set logger path : execution logging
        self._lepath = join(
            self._ldir, 
            'execution_{}.log'.format(
                datetime.now().strftime('%Y%m%d')
                )
            )

        # set logger format
        self._lfmt = lfmt

        # set logger instance
        self._logger = Logger(name)

        # set logger instance : handler
        lhandler = FileHandler(filename=self._lepath)
        
        # set logger instance : formatter
        lformatter = Formatter(self._lfmt)
        
        # set formatter to handler
        lhandler.setFormatter(lformatter)

        # set handler to logger
        self._logger.addHandler(lhandler)

    def __enter__(self) -> object:
        '''
        
        '''
        # set mode
        setmode(self._internal[0].fileno(), O_BINARY)
        setmode(self._internal[1].fileno(), O_BINARY)

        # start to listen external interface
        self.listen()

        return self

    def __exit__(self, exc_type:type, exc_value:object, exc_traceback:TracebackType) -> bool:
        '''
        
        '''
        self.close()

        return False

    @property
    def port(self) -> Tuple[str,int]:
        '''
        
        '''
        return [self._pid]+list(self._external.getsockname())

    def log(self, *args:Iterable[object], attr:str='info') -> None:
        '''
        
        '''
        # log message as info
        getattr(self._logger, attr)(' '.join([str(arg) for arg in args]))

        return None
        
    def listen(self) -> SocketType:
        '''
        
        '''
        # bind on address
        self._external.bind(self._addr)

        # start to listen
        self._external.listen()

        # write binding port
        with open(self._lppath, mode='w', encoding=self._enc) as fd:
            self.write(fd, self.port)

        return self._external

    def close(self) -> SocketType:
        '''
        
        '''
        # close only external interface
        # closing internal interface will be blocked
        if self._external is not None:
            if not self._external.fileno() == -1:
                self._external.close()

        return self._external

    def write(self, io_:Union[TextIOWrapper,SocketType], obj:Union[dict,str]) -> bytes:
        '''
        
        '''

        return _write(io_, obj, self._fmt, self._enc)

    def read(self, io_:Union[TextIOWrapper,SocketType]) -> Union[dict,str]:
        '''
        
        '''

        return _read(io_, self._fmt, self._enc)

    def expired(self) -> bool:
        '''
        
        '''
        # set last ping difference
        diff = (datetime.now() - self._last_ping).seconds

        # has last ping been sent over than timeout ?
        return diff > self._expire

    def timedout(self, cid:Union[str,None]) -> dict:
        '''
        
        '''
        def _timedout(_cid:str) -> bool:
            '''
            
            '''
            item = self._external_accepted[_cid]
            _, _, datetime_ = item
            diff = (datetime.now() - datetime_).seconds
            return diff > self._timeout

        # set container
        container = {}
        
        if cid is None:
            # every client id
            for cid in self._external_accepted.keys():
                container[cid] = _timedout(cid)

        else:
            # specified client id
            container[cid] = _timedout(cid)
        
        return container

    def enqueue(self) -> bytes:
        '''
        
        '''
        if self._external.fileno() == -1:
            raise InterruptedError('external interface is closed.')
            
        # accept client socket from external interface
        csocket, _ = self._external.accept()

        # set client universal unique idendifier
        cid = str(uuid4())

        # set client inject javascript file name
        cfname = 'inject_{}.js'.format(cid)

        # read from client socket
        message = NativeMessage( **self.read(csocket) )

        # set to external interface accepted sockets
        self._external_accepted[cid] = [csocket, cfname, message.datetime]

        # write inject javascript file
        with open(join(self._jsdir,cfname), mode='w', encoding=self._enc) as fd:
            fd.write(message.value)
            fd.flush()

        # set received data key
        message.key = cid

        # set received data value
        message.value = cfname

        # write to internal interface (stdout)
        return self.write(self._internal[1], message.dict)

    def dequeue(self) -> dict:
        '''
        
        '''
        # read from internal interface (stdin)
        message = NativeMessage( **self.read(self._internal[0]) )

        # set last ping (datetime)
        self._last_ping = message.datetime

        # return early for ping message
        if message.value == 'ping':
            return message.dict

        # return early for expired external interface accepted sockets
        if message.key not in self._external_accepted.keys():
            return message.dict

        # set from external interface accepted sockets
        csocket, cfname, _ = self._external_accepted[message.key]
        
        # if client socket is not closed
        # write to external interface 
        if csocket.fileno() > 0:
            self.write(csocket, message.dict)

        # close client socket
        csocket.close()

        try:
            # remove inject javascript file
            remove(join(self._jsdir,cfname))
        
        except:
            pass
        
        finally:
            # delete from external interface accepted sockets
            del(self._external_accepted[message.key])

        return message.dict

    def catch_exception(self, exception:Exception, termination:bool) -> None:
        # set exception message with traceback
        message = 'exception {} has been occured: {}\n'.format(
            type(exception), 
            str(exception)
            ) + \
            '\n'.join(format_tb(exception.__traceback__))

        # print exception message with traceback
        self.log(message, attr='error')

        if termination:
            # close external interface
            self.close()

            # kill this process id
            kill(self._pid, 2)
        
def enqueuing(p:Pipeline) -> None:
    '''
    
    '''
    while True:
        try:
            p.enqueue()

        except Exception as exception:
            p.catch_exception(exception, True)

    return None

def dequeuing(p:Pipeline) -> None:
    '''
    
    '''
    while True:
        try:
            try:
                p.dequeue()

            except error as exception:
                raise InterruptedError('pipeline has been broken.')

        except Exception:
            p.catch_exception(exception, True)
        
    return None
    
def watching_ping(p:Pipeline) -> None:
    '''
    
    '''
    while True:
        try:
            if p.expired():
                raise TimeoutError('pipeline has been expired.')
            
            sleep(1)

        except Exception as exception:
            p.catch_exception(exception, True)
        
    return None
    
def watching_socket(p:Pipeline) -> None:
    '''
    
    '''
    while True:
        for cid, timedout in p.timedout(None).items():
            if not timedout:
                continue
            
            # set from external interface accepted sockets
            csocket, cfname, _ = p._external_accepted[cid]

            # close client socket
            csocket.close()

            try:
                # remove inject javascript file
                remove(join(p._jsdir,cfname))

            except Exception as exception:
                p.catch_exception(exception, False)
            
            finally:
                # delete from external interface accepted sockets
                del(p._external_accepted[cid])

        sleep(1)
        
    return None

async def serve(p:Pipeline):
    '''
    
    '''
    # set methods
    methods = [
        enqueuing, 
        dequeuing, 
        watching_ping,
        watching_socket
        ]
        
    # set event loop
    loop = get_running_loop()
    
    # run in executor
    tasks = [
        loop.run_in_executor(None, method, p) \
        for method in methods
        ]

    return await gather(*tasks, return_exceptions=True)