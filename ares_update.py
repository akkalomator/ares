#!/usr/bin/env python3

import os
import shutil
import stat

ARES_HOME = os.path.expanduser('~/.ares')


def main():
    if not os.path.exists(ARES_HOME):
        os.mkdir(ARES_HOME)
    ares_path = ARES_HOME + '/ares'
    shutil.copy('./ares.py', ares_path)
    st = os.stat(ares_path)
    os.chmod(ares_path, st.st_mode | stat.S_IEXEC)


if __name__ == '__main__':
    main()