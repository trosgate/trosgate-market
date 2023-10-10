Step 1: Install Nginx Unit on Ubuntu
To install Nginx Unit on your Ubuntu droplet, you can follow these steps:

1. Add the Nginx Unit repository:
sudo sh -c "echo 'deb https://packages.nginx.org/unit/ubuntu/ focal unit' > /etc/apt/sources.list.d/unit.list"

This command adds the Nginx Unit repository to your sources list.


2. Add the Nginx Unit public key:
curl -o /etc/apt/trusted.gpg.d/nginx.gpg https://nginx.org/keys/nginx_signing.key

This command adds the Nginx Unit public key for package verification.

3. Update your package list:
sudo apt-get update

4. Install Nginx Unit:
sudo apt-get install unit

This command is run outside virtual environment as a 
system-wide command to install Nginx Unit on your server.


Step 2: Create Nginx Unit Configuration for SSL and Dynamic Domains
Now that you have Nginx Unit installed, 
you can create a configuration file that replicates 
your existing Nginx configuration for SSL and dynamic domains. 
-------see nginx_unit.json configuration in this directory------

When you use Nginx Unit to proxy requests to your application, 
some headers like Host, X-Real-IP, and X-Forwarded-For are typically passed automatically,
while others like X-Scheme and X-Forwarded-Proto need to be explicitly set 
in your unit.json configuration.

Here's how these headers are handled:

Host: The Host header is automatically passed to your application by Nginx Unit. You don't need to explicitly set it in your unit.json configuration.

X-Real-IP and X-Forwarded-For: These headers are also automatically passed by Nginx Unit. You don't need to set them in your unit.json configuration.

X-Scheme and X-Forwarded-Proto: By default, Nginx Unit does not automatically set these headers, so you should explicitly set them in your unit.json configuration if your application relies on them. Here's an example of how to set them:


Step 3: Configure Nginx Unit to Use the unit.json Configuration
To start Nginx Unit with your nginx_unit.json configuration, 
you can use the following command:

sudo unitd --control unix:/var/run/control.unit.sock --no-daemon --state /var/lib/unit --config /path/to/your/unit.json





