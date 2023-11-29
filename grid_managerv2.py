import argparse
import os
import pendulum
import subprocess

def check_number_of_cores(cores, hosts_grid):
    number_of_cores_grid = sum(list(map(lambda x: int(x.split(':')[1]), hosts_grid)))

    if(number_of_cores_grid < cores):
        raise ValueError("O número de cores informado é maior do que a grid suporta")

def check_hosts_argument(hosts_argument, hosts_grid):
    new_hosts = []
    not_in_grid = True

    for host_arg in hosts_argument:
        for host_grid in hosts_grid:
            if(host_arg in host_grid):
                not_in_grid = False
                new_hosts.append(host_grid)
                break
        
        if(not_in_grid):
            raise ValueError(f"O host {host_arg} não pertence a grid")
        
        not_in_grid = True

    return new_hosts

def fair_scheduler(hosts_grid, numprocs):
    hosts_and_procs = {}
    idx_host = 0
    new_hosts = []
    
    for _ in range(numprocs):
        aloc = False
        while(not aloc):
            host = hosts_grid[idx_host].split(':')
            if(host[0] not in hosts_and_procs.keys()):
                hosts_and_procs[host[0]] = 1
                aloc = True
            else:
                if(hosts_and_procs[host[0]] < int(host[1])):
                    hosts_and_procs[host[0]] = hosts_and_procs[host[0]] + 1
                    aloc = True

            idx_host += 1

            if(idx_host == len(hosts_grid)):
                idx_host = 0
        
    
    for ip, proc in hosts_and_procs.items():
        new_hosts.append(f'{ip}:{proc}')

    return new_hosts
    

if __name__ == '__main__':
    args = argparse.ArgumentParser()

    args.add_argument('--fairscheduler', required=False, type=str, help="Dividir o número de processos entre os hosts")
    args.add_argument('--hosts', required=False, type=str, nargs='+', help="Hosts que serão usados")
    args.add_argument('--numprocs', required=True, type=int, help="Número de processos que serão usados")
    args.add_argument('--exec', required=True, type=str, help="Arquivo compilado para executar")
    args = args.parse_args()
    
    today = pendulum.now()
    file_machines = f'exec{today.year}{today.month}{today.day}{today.hour}{today.minute}{today.second}'
    
    arquivo_execucao = os.getcwd()
    arquivo_execucao = os.path.join(arquivo_execucao, args.exec)
   
    if not os.path.exists(arquivo_execucao):
        raise FileExistsError("O arquivo mencionado não existe")
    
    with open('machinefile', 'r') as file:
        hosts_grid = file.readlines()
        hosts_grid = [host.strip() for host in hosts_grid]

    if(args.hosts):
        hosts_grid = check_hosts_argument(args.hosts, hosts_grid)

    check_number_of_cores(args.numprocs, hosts_grid)

    if(args.fairscheduler == 'yes'):
        hosts_grid = fair_scheduler(hosts_grid, args.numprocs)
    
    with open(file_machines, 'w') as file:
        for host in hosts_grid:
            file.write(f'{host}\n')

    list_exec = [f'mpiexec -n { args.numprocs} -f {file_machines} ./{args.exec}']

    try:
        begin_run = pendulum.now()
        run = subprocess.run(list_exec, shell=True, check=True, text=True)
        end_run = pendulum.now()
        duracao = end_run.diff(begin_run)
        
        print("Script executado com sucesso!")
        print(f"Tempo de duração: {duracao.in_words()}")
        print(f"Número de processadores: {args.numprocs}")

        used_machines = ""
        for machine in hosts_grid:
            used_machines += f"{machine.split(':')[0]} "

        print(f"Maquinas utilizadas: {used_machines}")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o processo: {e}")
