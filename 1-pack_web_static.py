#!/usr/bin/python3
"""
Generates a .tgz archive from the web_static folder
"""
from fabric.api import local
from datetime import datetime


def do_pack():
    """
    Creates a .tgz archive of web_static folder
    Returns: Archive path if successful, otherwise None
    """
    try:
        local("mkdir -p versions")
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = f"versions/web_static_{timestamp}.tgz"
        local(f"tar -cvzf {archive_path} web_static")
        return archive_path
    except:
        return None
