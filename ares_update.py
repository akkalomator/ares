#!/usr/bin/env python3

import os
import shutil

ARES_HOME = os.path.expanduser('~/.ares')


def main():
    if not os.path.exists(ARES_HOME):
        os.mkdir(ARES_HOME)
    shutil.copy('./ares.py', ARES_HOME + '/ares')


if __name__ == '__main__':
    main()