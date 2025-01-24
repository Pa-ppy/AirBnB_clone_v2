#!/usr/bin/env bash
# Sets up a web server for the deployment of web_static

# Install Nginx if not already installed
if ! command -v nginx &> /dev/null; then
    sudo apt-get update
    sudo apt-get install -y nginx
fi

# Create required directories
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# Create a fake HTML file for testing
echo "<html>
  <head>
  </head>
  <body>
    ALX
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

# Create a symbolic link to the test directory
if [ -L /data/web_static/current ]; then
    sudo rm /data/web_static/current
fi
sudo ln -s /data/web_static/releases/test/ /data/web_static/current

# Give ownership of /data/ to ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
config="/etc/nginx/sites-available/default"
if ! grep -q "hbnb_static" "$config"; then
    sudo sed -i "/server_name _;/a \\\n    location /hbnb_static/ {\n        alias /data/web_static/current/;\n    }" "$config"
fi

# Restart Nginx to apply changes
sudo service nginx restart

exit 0
