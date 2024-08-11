clean:
	rm tom3.img
	rm meta-data.yaml

rootfs: 
	qemu-img create -b noble-server-cloudimg-amd64.img -f qcow2 -F qcow2 tom3.img 32G

meta-data:
	@echo "instance-id: tom3" > meta-data.yaml
	@echo "local-hostname: tom3" >> meta-data.yaml

vm:	meta-data rootfs	
	#virt-install --name=tom3 --ram=4096 --vcpus=4 --import --disk path=tom3.img,format=qcow2 --os-variant=ubuntu24.04 --cloud-init user-data=user-data.yaml,network-config=network-config.yaml --graphics vnc,listen=0.0.0.0 --noautoconsole --noreboot
	virt-install \
		--name=tom3 \
		--ram=4096 \
		--vcpus=4 \
		--import \
		--disk path=tom3.img,format=qcow2 \
		--os-variant=ubuntu24.04 \
		--cloud-init meta-data=meta-data.yaml,user-data=user-data.yaml,network-config=network-config.yaml \
		--graphics vnc,listen=0.0.0.0 \
		--noreboot
