from tornado.iostream import IOStream
from tornado.gen import coroutine,Return,sleep,moment
from tornado.tcpserver import TCPServer
import socket
import tornado
import sys

@coroutine
def makeTunnel():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM,0)
    stream = IOStream(s)
    yield stream.connect((sys.argv[1],int(sys.argv[2])))
    yield stream.write('GET /backdoor HTTP/1.1\r\nHost: SomewhereOvertheRainbow\r\n\r\n')
    raise Return(stream)

class T(TCPServer):

    @coroutine
    def handle_stream(self, stream, addr):
        print('requests from %s' % (addr,),'forward to new tunnel')
        tunnel = yield makeTunnel()
        stream.read_until_close(streaming_callback=tunnel.write)
        tunnel.read_until_close(streaming_callback=stream.write)

T().listen(9999)
tornado.ioloop.IOLoop().current().start()
