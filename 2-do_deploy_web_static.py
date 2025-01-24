#!/usr/bin/python3
"""
Distributes an archive to web servers
"""

from fabric.api import env, put, run
import os

env.hosts = ['<IP web-01>', '<IP web-02>']

def do_deploy(archive_path):
    """
    Deploys archive to web servers
    Returns: True if successful, False otherwise
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # Extract filename and folder name
        file_name = archive_path.split("/")[-1]
        folder_name = f"/data/web_static/releases/{file_name.split('.')[0]}"
        
        # Upload archive to /tmp/ directory
        put(archive_path, "/tmp/")
        
        # Create target directory and uncompress archive
        run(f"mkdir -p {folder_name}")
        run(f"tar -xzf /tmp/{file_name} -C {folder_name}")
        
        # Remove the archive from /tmp/
        run(f"rm /tmp/{file_name}")
        
        # Move contents out of web_static subfolder
        run(f"mv {folder_name}/web_static/* {folder_name}/")
        run(f"rm -rf {folder_name}/web_static")
        
        # Update the symbolic link
        run("rm -rf /data/web_static/current")
        run(f"ln -s {folder_name} /data/web_static/current")
        
        print("New version deployed!")
        return True
    except:
        return False
