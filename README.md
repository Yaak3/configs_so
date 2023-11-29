# Processo de instalação para uso do projeto

### Configuração de rede no roteador

Criar uma rede local com a mascara 192.168.0.1/24

### Sistema operacional suportado

Instalar o Ubuntu Server ou Ubuntu Desktop

### Configuração no host master

Fixar o IP 192.168.0.110 no host master (via interface)

Instalar os seguintes pacotes no host master:
 - apt-get install -y nfs-client
 - apt-get install -y openssh-server
 - apt-get install -y build-essential
 - apt-get install -y mpich
 - apt-get install apache2

Criar um usuário chamado mpi:
 - adduser --home /mirror --uid 1100 --disabled-password --gecos "" mpi

Criar os seguintes diretórios:
 - mkdir /mirror
 - mkdir /var/www/html/grid_install_script

Mudar a permissão do diretório /mirror para o usuário mpi:
 - chown mpi:mpi /mirror

Copiar os seguintes arquivos:
 - cp grid_managerv2.py /mirror/
 - cp matrix_multiplication /mirror/
 - cp service_discovery_grid.py /mirror/
 - cp install_worker.sh /var/www/html/grid_install_script/
 - cp gdiscovery.service /etc/systemd/system/

Configurar o SSH:
 - sudo su (digitar sua senha)
 - su mpi
 - cd /mirror
 - ssh-keygen -t rsa (só dar enter até aparecer uma chave criptografada e retornar ao terminal)
 - cd .ssh/
 - cat id_rsa.pub >> authorized_keys

Iniciar o serviço de descoberta da grid:
 - systemctl start gdiscovery

### Configuração para inicializar um worker

 - Sistema operacional suportado: Ubuntu Server ou Ubuntu Desktop

Baixar o script e realizar instalação do worker
 - wget 192.168.0.110/grid_install_scritp/install_worker.sh
 - sh install_worker.sh

### Rodando uma aplicação MPI

No host master, executar o seguinte comando
 - sudo su (digitar a senha do seu usuário)
 - su mpi
 - cd /mirror
 - para descobrir se o host for descoberto, é só escrever o comando "cat machinefile" e conferir se o IP está la
 - python3 gird_managerv2.py --numprocs NUMERO_DE_PROCESSOS --exec APLICAÇÃO_MPI (disponibilizamos o matrix_multiplication no repositorio)
 - Existem outras opções no grid_managerv2.py, você pode consultar passando o comando --help
Para compilar uma nova aplicação MPI, você pode usar um código em C que foi escrito com base no MPI e compilar com o seguinte comando
 - mpicc CODIGO.c NOME_ARQUIVO_DESTINO (não precisa de .c no final do arquivo de destino)


Em caso de dúvida ou alguma dificuldade com as configurações, estamos à disposição
bgsousa@furb.br, lfmelo@furb.br.