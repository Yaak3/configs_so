import os
import re
from time import sleep

lista_hosts_ssh = None
new_hosts_grid = ""
result = ""

while(True):
	with os.popen("nmap -p 22 --open -oG - 192.168.0.1/24 | grep -oP '\d+\.\d+\.\d+\.\d+'") as terminal:
		lista_hosts_ssh = terminal.read()
        
	lista_hosts_ssh = set(re.findall(r'\d+\.\d+\.\d+\.\d+',lista_hosts_ssh))
	lista_hosts_ssh = list(filter(lambda x: False if x == "192.168.0.110" else True, lista_hosts_ssh))
	new_hosts_grid += f'192.168.0.110:4\n'

	for host in lista_hosts_ssh:
		with os.popen(f"ssh {host} -o StrictHostKeyChecking=no UserKnownHostFile=/mirror/.ssh/known_hosts 'lscpu'") as terminal:
			result = terminal.read()
			result = re.search(r'(CPU\(s\))(.*)(\d+)', result)
			if(result != None):
				new_hosts_grid += f'{host}:{result.groups()[-1]}\n'

	
	with open('/mirror/machinefile', 'w') as file:
		file.write(new_hosts_grid)
	
	new_hosts_grid = ""
	sleep(60)
