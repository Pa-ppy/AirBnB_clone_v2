#!/usr/bin/python3
"""
Creates and distributes an archive to web servers
"""

from fabric.api import env, put, run, local
from datetime import datetime
import os

env.hosts = ['<100.24.72.31 806443-web-01>', '<54.88.51.70 806443-web-02>']  # Replace with your server IPs


def do_pack():
    """
    Generates a .tgz archive from the web_static folder
    Returns: The archive path if successful, otherwise None
    """
    try:
        local("mkdir -p versions")
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = f"versions/web_static_{timestamp}.tgz"
        local(f"tar -cvzf {archive_path} web_static")
        return archive_path
    except:
        return None


def do_deploy(archive_path):
    """
    Distributes an archive to web servers
    Returns: True if successful, False otherwise
    """
    if not os.path.exists(archive_path):
        return False

    try:
        file_name = archive_path.split("/")[-1]
        folder_name = f"/data/web_static/releases/{file_name.split('.')[0]}"

        # Upload the archive
        put(archive_path, "/tmp/")
        
        # Create the directory and extract the archive
        run(f"mkdir -p {folder_name}")
        run(f"tar -xzf /tmp/{file_name} -C {folder_name}")
        
        # Remove the archive from /tmp/
        run(f"rm /tmp/{file_name}")
        
        # Move files to the correct location
        run(f"mv {folder_name}/web_static/* {folder_name}/")
        run(f"rm -rf {folder_name}/web_static")
        
        # Update the symbolic link
        run("rm -rf /data/web_static/current")
        run(f"ln -s {folder_name} /data/web_static/current")

        print("New version deployed!")
        return True
    except:
        return False


def deploy():
    """
    Full deployment process:
    - Creates an archive using do_pack
    - Distributes it to web servers using do_deploy
    Returns: True if all steps were successful, otherwise False
    """
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)
