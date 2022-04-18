
'''
communicate.py
'''

from struct import pack
from struct import unpack

from json import dumps
from json import loads
from json import JSONDecodeError

from io import TextIOWrapper
from socket import SocketType
from datetime import datetime

from typing import Union

class NativeMessage:

    _key = None
    _value = None
    _datetime = None

    def __init__(
            self, 
            key:str, 
            value:object
            ):
        '''
        
        '''
        # set native message key
        self._key = key
        
        # set native message value
        self._value = value

        # set native message datetime
        self._datetime = datetime.now()

    @property
    def dict(self) -> dict:
        '''
        
        '''
        return {
            'key': self._key,
            'value': self._value
            }

    @property
    def key(self) -> str:
        '''
        
        '''
        return self._key

    @property
    def value(self) -> object:
        '''
        
        '''
        return self._value

    @property
    def datetime(self) -> datetime:
        '''
        
        '''
        return self._datetime

    @key.setter
    def key(self, str_:str) -> None:
        '''
        
        '''
        self._key = str_
        self._datetime = datetime.now()

    @value.setter
    def value(self, obj:object) -> None:
        '''
        
        '''
        self._value = obj
        self._datetime = datetime.now()

def _write(
    io_:Union[TextIOWrapper,SocketType],
    obj:Union[dict,str],
    fmt:str,
    enc:str
    ) -> bytes:
    '''
    
    '''
    # is type validated ?
    if not isinstance(io_, TextIOWrapper) and \
        not  isinstance(io_, SocketType):
        raise TypeError('should be socket type or text io wrapper type')

    # set bytes
    bytes_ = dumps(obj, ensure_ascii=False).encode(enc)

    # set bytes length 
    len_ = len(bytes_)

    # set packed bytes length + packed bytes
    packed = pack(fmt, len_) + \
        pack('{}s'.format(len_), bytes_)

    if isinstance(io_, SocketType):
        # write bytes to socket
        io_.send(packed)

    elif isinstance(io_, TextIOWrapper):
        # write packed bytes to buffer 
        io_.buffer.write(packed)

        # flush buffer
        io_.buffer.flush()

    else:
        raise TypeError('io should be socket or text io')

    return packed

def _read(
        io_:Union[TextIOWrapper,SocketType],
        fmt:str,
        enc:str
        ) -> Union[dict,str]:
    '''
    
    '''
    # is type validated ?
    if not isinstance(io_, TextIOWrapper) and \
        not  isinstance(io_, SocketType):
        raise TypeError('should be socket type or text io wrapper type')

    if isinstance(io_, SocketType):
        # set first 4 bytes
        head = io_.recv(4)

        # set bytes length
        len_ = unpack(fmt, head)[0]
        
        # set string
        str_ = io_.recv(len_).decode(enc)
        
    elif isinstance(io_, TextIOWrapper):
        # set first 4 bytes
        head = io_.buffer.read(4)

        # set bytes length
        len_ = unpack(fmt, head)[0]

        # set string
        str_ = io_.buffer.read(len_).decode(enc)
    
    try:
        # with json format
        unpacked = loads(str_)
    
    except JSONDecodeError as e:
        # with non-json format
        unpacked = str_

    return unpacked