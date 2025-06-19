private-key-ca:
	sudo certtool --generate-privkey --bits 4096 --outfile /etc/ssl/private/mycakey.pem

ca-info:
	sudo cp ca.info /etc/ssl/ca.info

self-signed-ca-cert:
	sudo certtool --generate-self-signed \
	--load-privkey /etc/ssl/private/mycakey.pem \
	--template /etc/ssl/ca.info \
	--outfile /usr/local/share/ca-certificates/mycacert.crt

update-certs:
	sudo update-ca-certificates

private-key-server:
	sudo certtool --generate-privkey \
	--bits 2048 \
	--outfile /etc/ldap/tom1_slapd_key.pem

server-info:
	sudo cp server.info /etc/ssl/tom1.info

server-cert:
	sudo certtool --generate-certificate \
	--load-privkey /etc/ldap/tom1_slapd_key.pem \
	--load-ca-certificate /etc/ssl/certs/mycacert.pem \
	--load-ca-privkey /etc/ssl/private/mycakey.pem \
	--template ./cert.tmpl \
	--outfile /etc/ldap/tom1_slapd_cert.pem


	
