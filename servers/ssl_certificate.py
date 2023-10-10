import os
import subprocess

def request_ssl_certificate(domain):
    try:
        # Use Certbot to request a certificate for the new domain
        subprocess.run(['certbot', 'certonly', '--nginx', '-d', domain, '--non-interactive', '--agree-tos', '--email', 'your@email.com'])

        # Certbot should place the certificates in /etc/letsencrypt/live/domain/
        certificate_path = f'/etc/letsencrypt/live/{domain}/fullchain.pem'
        key_path = f'/etc/letsencrypt/live/{domain}/privkey.pem'

        return certificate_path, key_path

    except Exception as e:
        print(f"Error requesting SSL certificate: {str(e)}")
        return None, None

# Example usage:
new_domain = 'newdomain.com'
certificate_path, key_path = request_ssl_certificate(new_domain)
if certificate_path and key_path:
    print(f"Certificate Path: {certificate_path}")
    print(f"Key Path: {key_path}")
