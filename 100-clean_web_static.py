#!/usr/bin/python3
# Fabfile to delete out-of-date archives.
import os
from fabric.api import *

env.hosts = ["54.236.30.191", "54.82.135.171"]


def do_clean(number=0):
    """Deletes outdated archives.
    Args:
        number (int):  number of archives to keep.
    if number is 1 or 0, keeps the most recent archive. If
    number is 2, keeps the two recent archives,
    etc.
    """
    number = 1 if int(number) == 0 else int(number)

    archives = sorted(os.listdir("versions"))
    [archives.pop() for i in range(number)]
    with lcd("versions"):
        [local("rm ./{}".format(a)) for a in archives]

    with cd("/data/web_static/releases"):
        archives = run("ls -tr").split()
        archives = [a for a in archives if "web_static_" in a]
        [archives.pop() for i in range(number)]
        [run("rm -rf ./{}".format(a)) for a in archives]
