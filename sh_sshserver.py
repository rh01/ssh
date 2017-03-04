import paramiko
import threading
import subprocess
import sys
import socket


host_key = paramiko.RSAKey(filename = 'test_rsa.key')

class Server(paramiko.ServerInterface):
	"""docstring for Server"""
	def __init__(self):
		self.event = threading.Event()		
	def check_channel_request(self, kind, chanid):
		if kind == 'session':
			return paramiko.OPEN_SUCCEEDED
		return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
	def check_auth_password(self, username, password):
		if (username == 'administrator') and(password == 'hadoop'):
			return paramiko.AUTH_SUCCESSFUL
		return paramiko.AUTH_FAILED

server = sys.argv[1]
ssh_port = int(sys.argv[2])
try:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.bind((server, ssh_port))
	sock.listen(100)
	print '[+] listening for connection ...'
	client, addr = sock.accept()

except Exception, e:
	print '[-] listen failed :' +str(e)
	sys.exit(1)

print '[+] Got a connection'

try:
	shSession = paramiko.Transport(client)
	shSession.add_server_key(host_key)
	server = Server()
	try:
		shSession.start_server(server=server)

	except paramiko.SSHEXceptionn, x:
		print '[-] SSH negotition failed'
	chan = shSession.accept(20)
	print '[+] Authenticaed!'
	print chan.send("""
                               _,.-----.,_
                            ,-~           ~-.
                           ,^___           ___^.
                          /~"   ~"   .   "~   "~\

                         | Y     ~-. | ,-~     Y |
                         | |        }:{        | |
                         j l       / | \       ! l
                      .-~  (__,.--" .^. "--.,__)  ~-.
                     (           / / | \ \           )
                      \.____,   ~  \/"\/  ~   .____,/
                       ^.____                 ____.^
                          | |T ~\  !   !  /~ T| |
                          | |l   _ _ _ _ _   !| |
                          | l \/V V V V V V\/ j |
                          l  \ \|_|_|_|_|_|/ /  !
                           \  \[T T T T T TI/  /
                            \  `^-^-^-^-^-^'  /
                             \               /
                              \.           ,/
                                "^-.___,-^"

		---    -   -    -       ----- -   -   -       -
		 -     -   -   - -    -       -  -    -       -
		 -     -----  -----  -        - -     -       -
		 -     -   - - 	   -  -       -  -     -     -
		---    -   --       -   ----- -   -     -----
		**************************************************
		***            SSH Server And Client           ***
		***     Heng-Shen Heng         Bo-Zhang        ***
		***      13031110141          13031110165      ***
		**************************************************
""")

	while 1:
		try:
			command = raw_input("Enter command:").strip('\n')
			if command != 'exit':
				chan.send(command)
				print chan.recv(1024) + '\n'
			else:
				chan.send('exit')
				print 'exiting'
				shSession.close()
				raise Exception("Exit")
		except KeyboardInterrupt:
			shSession.close()
except Exception, e:
	print '[-] Caught exception: ' +  str(e)
	try:
		shSession.close()
	except:
		pass
	sys.exit(1)
