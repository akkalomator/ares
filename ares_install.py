#!/usr/bin/env python3

import os.path
import shutil

ARES_HOME = os.path.expanduser('~/.ares')
BASH_PROFILE_PATH = os.path.expanduser('~/.bash_profile')
ZSHRC_PATH = os.path.expanduser('~/.zshrc')


def main():
    if not os.path.exists(ARES_HOME):
        os.mkdir(ARES_HOME)
    shutil.copy('./ares.py', ARES_HOME + '/ares')

    if os.path.exists(BASH_PROFILE_PATH):
        with open(BASH_PROFILE_PATH, mode='a') as bash_profile:
            bash_profile.write('\nexport PATH=${PATH}:/Users/$USER/.ares\n')

    if os.path.exists(ZSHRC_PATH):
        with open(ZSHRC_PATH, mode='a') as zshrc:
            zshrc.write('\nexport PATH=${PATH}:/Users/$USER/.ares\n')


if __name__ == '__main__':
    main()
