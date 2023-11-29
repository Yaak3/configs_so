echo "192.168.0.110 master" | tee -a /etc/hosts
apt-get install -y nfs-client
apt-get install -y openssh-server
mkdir /mirror
mount master:/mirror /mirror
echo "master:/mirror 		/mirror		nfs" | tee -a /etc/fstab
adduser --home /mirror --uid 1100 --disabled-password --gecos "" mpi
apt-get install -y build-essential
apt-get install -y mpich
