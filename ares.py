#!/usr/bin/env python3

import argparse
import json
import os
import pathlib
import shutil
import sys
import zipfile

ARES_HOME = os.path.expanduser('~/.ares')
ARES_TEMP = ARES_HOME + '/temp'
CONFIG_FILE_PATH = ARES_HOME + '/config.json'


def create_unpack_parameters(subparsers):
    unpack_parser = subparsers.add_parser('unpack',
                                          description='Unpacks zip resources to projects resources with current '
                                                      'profile',
                                          help='Unpacks zip resources to projects resources with current profile')

    unpack_parser.add_argument('zip',
                               nargs='*',
                               default=None,
                               type=pathlib.Path,
                               help="zip file to unpack")

    unpack_parser.add_argument('-n', '--name',
                               nargs='?',
                               default=None,
                               help="new file name")

    unpack_parser.add_argument('-p', '--profile',
                               nargs='?',
                               default=None,
                               help="set profile as current. Profiles are predefined key-value properties, "
                                    "that store project resource directory and mappings between file "
                                    "suffixes and resource folders. They are stored in "
                                    "~/.ares/config.json")


def create_profile_parameters(subparsers):
    profile_parser = subparsers.add_parser('profile',
                                           description='Manages your profile',
                                           help='Manages your profile')
    profile_parser.add_argument('-l', '--list',
                                action='store_true',
                                help="List names of all profiles")

    profile_parser.add_argument('-a', '--add',
                                metavar="PROFILE_NAME",
                                default=None,
                                help="add new profile with given name. Requires RESOURCE_DIRECTORY")

    profile_parser.add_argument('-d', '--delete',
                                metavar="PROFILE_NAME",
                                default=None,
                                help="delete profile with given name")

    profile_parser.add_argument('res',
                                nargs='?',
                                metavar='RESOURCE_DIRECTORY',
                                help="path to project resource directory")

    add_resource_folders_parameters(profile_parser)


def add_resource_folders_parameters(profile_parser):
    profile_parser.add_argument('--ldpi',
                                metavar='LDPI_SUFFIX',
                                help='Suffix that matches ldpi folder')
    profile_parser.add_argument('--mdpi',
                                metavar='MDPI_SUFFIX',
                                help='Suffix that matches mdpi folder')
    profile_parser.add_argument('--hdpi',
                                metavar='HDPI_SUFFIX',
                                help='Suffix that matches hdpi folder')
    profile_parser.add_argument('--xhdpi',
                                metavar='XHDPI_SUFFIX',
                                help='Suffix that matches xhdpi folder')
    profile_parser.add_argument('--xxhdpi',
                                metavar='XXHDPI_SUFFIX',
                                help='Suffix that matches xxhdpi folder')
    profile_parser.add_argument('--xxxhdpi',
                                metavar='XXXHDPI_SUFFIX',
                                help='Suffix that matches xxxhdpi folder')
    profile_parser.add_argument('--nodpi',
                                metavar='NODPI_SUFFIX',
                                help='Suffix that matches nodpi folder')
    profile_parser.add_argument('--tvdpi',
                                metavar='TVDPI_SUFFIX',
                                help='Suffix that matches tvdpi folder')


def exit_not_initialized(parser):
    parser.error("You need to initialize profile first. Use `ares profile -a <PROFILE_NAME> "
                 "<RESOURCE_DIRECTORY>` or try `ares profile -h`")


def execute_profile(args, parser):
    if args.list:
        list_profiles(parser)
    elif args.delete is not None:
        delete_profile(args, parser)
    elif args.add is not None:
        add_profile(args, parser)


def list_profiles(parser):
    if os.path.isfile(CONFIG_FILE_PATH):
        with open(CONFIG_FILE_PATH, mode='r') as config_file:
            config = json.load(config_file)
            print(*map(lambda profile: profile['name'], config['profiles']), sep='\n')

    else:
        exit_not_initialized(parser)


def delete_profile(args, parser):
    if os.path.isfile(CONFIG_FILE_PATH):
        with open(CONFIG_FILE_PATH, mode='r+') as config_file:
            config = json.load(config_file)
            name = args.delete
            if name == config['active_profile']:
                parser.error("Cannot delete active profile {}".format(name))
                return

            config['profiles'] = list(filter(lambda profile: profile['name'] != name, config['profiles']))
            config_json = json.dumps(config, indent=4)
            config_file.seek(0)
            config_file.truncate()
            config_file.write(config_json)
    else:
        exit_not_initialized(parser)


def add_profile(args, parser):
    name = args.add
    resdir = args.res
    if resdir is None:
        parser.error("You must specify -r <RESOURCE_DIRECTORY>")

    if os.path.isfile(CONFIG_FILE_PATH):
        with open(CONFIG_FILE_PATH, mode='r+') as config_file:
            config = json.load(config_file)
            if any(profile["name"] == name for profile in config["profiles"]):
                parser.error("Profile with this name already exists")
            else:
                profile = {
                    "name": name,
                    "resdir": resdir,
                    "ldpi": args.ldpi,
                    "mdpi": args.mdpi,
                    "hdpi": args.hdpi,
                    "xhdpi": args.xhdpi,
                    "xxhdpi": args.xxhdpi,
                    "xxxhdpi": args.xxxhdpi,
                    "nodpi": args.nodpi,
                    "tvdpi": args.tvdpi
                }
                config["profiles"].append(profile)
                config["active_profile"] = name
                config_json = json.dumps(config, indent=4)
                config_file.seek(0)
                config_file.truncate()
                config_file.write(config_json)
    else:
        profile = {
            "name": name,
            "resdir": resdir,
            "ldpi": args.ldpi,
            "mdpi": args.mdpi,
            "hdpi": args.hdpi,
            "xhdpi": args.xhdpi,
            "xxhdpi": args.xxhdpi,
            "xxxhdpi": args.xxxhdpi,
            "nodpi": args.nodpi,
            "tvdpi": args.tvdpi
        }
        config = {
            "active_profile": name,
            "profiles": [profile]
        }

        config_json = json.dumps(config, indent=4)
        if not os.path.exists(ARES_HOME):
            os.mkdir(ARES_HOME)
        with open(CONFIG_FILE_PATH, mode='w') as config_file:
            config_file.write(config_json)

    print("Profile '{}' has been added and is now active".format(name))


def get_profile_by_name(profile_name, config):
    return [profile for profile in config["profiles"] if profile["name"] == profile_name][0]


def get_default_profile(config):
    return get_profile_by_name(config["active_profile"], config)


def set_profile_as_active(profile, config, config_file):
    profile_name = profile["name"]
    if config['active_profile'] != profile_name:
        config['active_profile'] = profile_name
        config_json = json.dumps(config, indent=4)
        config_file.seek(0)
        config_file.truncate()
        config_file.write(config_json)
        print("Profile '{}' is now active".format(profile_name))


def execute_unpack(args, parser):
    if os.path.isfile(CONFIG_FILE_PATH):
        with open(CONFIG_FILE_PATH, mode='r+') as config_file:
            config = json.load(config_file)
            profile_name = args.profile
            if profile_name is not None:
                try:
                    profile = get_profile_by_name(profile_name, config)
                    set_profile_as_active(profile, config, config_file)
                except IndexError:
                    parser.error("Profile '{}' not found".format(profile_name))
            else:
                profile = get_default_profile(config)
    else:
        exit_not_initialized(parser)

    zip_paths = args.zip
    suffixes_to_folders = [(v, k) for k, v in list(profile.items())[2::]]
    resource_dir = profile['resdir']
    if zip_paths is not None:
        for zip_path in zip_paths:
            print("Unzipping '{}' using profile '{}'".format(zip_path, profile['name']))

            temp_dir = ARES_TEMP + '/' + zip_path.stem
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            for (suffix, folder) in suffixes_to_folders:
                if suffix is None:
                    continue
                found_file_for_suffix = False
                for resource in pathlib.Path(temp_dir).rglob('*{}.*'.format(suffix)):
                    folder_to_move = pathlib.Path(resource_dir + '/drawable-' + folder + '/')
                    file_name = pathlib.Path(args.name)
                    if file_name.suffix == '':
                        file_name = file_name.with_suffix(resource.suffix)
                    found_file_for_suffix = True
                    try:
                        shutil.move(resource, folder_to_move.joinpath(file_name))
                    except FileNotFoundError:
                        sys.stderr.write("Folder '{}' does not exist\n".format(folder_to_move))
                if not found_file_for_suffix:
                    print("No files for suffix '{}' found".format(suffix))
            shutil.rmtree(temp_dir)
            print("Unzipping '{}' using profile '{}' successful!".format(zip_path, profile['name']))


def main():
    parser = argparse.ArgumentParser(
        description="Unpacks png resources from zip file and distributes it among your project"
    )

    subparsers = parser.add_subparsers(title='commands', dest="mode")

    create_unpack_parameters(subparsers)
    create_profile_parameters(subparsers)

    args, _ = parser.parse_known_args()

    if args.mode == 'profile':
        execute_profile(args, parser)
    elif args.mode == "unpack":
        execute_unpack(args, parser)


if __name__ == '__main__':
    main()
