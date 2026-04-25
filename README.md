# autobuild
Tools to automate build of ubuntu kvm virtual machines

This code was started when I was using Suse linux.
It is currently running on Kubuntu 24.04.
KVM Must be configured and enabled.
A host brige is a MUST, named br0.
I have used this tool using static addresses, thus the defaults 
in the Makefile are set for static.
You MUST put the ip-address and FQDN into the /etc/hosts of 
the new VM you are creating.  The tool uses "getent" to fetch
entries from /etc/hosts.
You must create directory "/data" and have FULL WRITE permsision
You must setup directory /var/lib/kvmbld so you have FULL WRITE permission
You must install the full libvirt suite.
The tool uses virt-install to create kvm-nodes.
The tool uses virsh to manage the vms.

Features:  
Distro is downloaded on-the-fly, based on settings in distro file.  
Cloud-image is used as backing store for nodes rootfs.  
Each node rootfs is backed to the cloud-image, this results is shared images when multiple nodes using the same.  
Auto registration with Ansible server.  
Auto snapshot after install.  
Proxy is enabled and declared in apt-dir/(DISTRO)/apt-(ROLE)-proxy.tmpl and  
user-data-dir/(DISTRO)/user-data-proxy.tmpl

syntax:

make -e NAME=FQDN ROLE=general node  
--> this create host FQDN as a general build node

make -e NAME=FQDN ROLE=docker node  
--> this creates host FQDN as a docker node that supports docker-in-docker

To add a distribution:  
Edit the distro file and save the label, url, etc for the desired distro.
Take a look at the distro-vendors cloud page for cloud-images

Why do I do this?  
It's fun.

