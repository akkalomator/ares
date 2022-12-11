# ares - a useful utility for dealing with android png resources for unix

ares copies all files annotated with suffixes to your project resource folder.
For example, you have `icon.zip` file which contains following files:

```
icon@1x.png
icon@2x.png
icon@3x.png
icon@4x.png
```

ares will make them appear in your project `res/drawable-<resolution>` folders as `icon.png`

## How to use

1. Download script

    - Optional: run `ares_install`:
      ```
      ./ares_install.py
      ```

2. Setup. Do this once and you will never have to do this again.

   In your console type

   ```
   ares profile -a <PROFILE_NAME> <RESOURCE_DIRECTORY> \
    [--ldpi <ldpi_SUFFIX>] \
    [--mdpi <mdpi_SUFFIX>] \
    [--hdpi <hdpi_SUFFIX>] \
    [--xhdpi <xhdpi_SUFFIX>] \
    [--xxhdpi <xxhdpi_SUFFIX>]  \
    [--xxxhdpi <xxxhdpi_SUFFIX>] \
    [--nodpi <nodpi_SUFFIX>] \
    [--tvdpi <tvdpi_SUFFIX>]
   ```

   - `<PROFILE_NAME>` is is a string alias for your profile. You can create different profiles
   and switch between them using

       `ares unpack -p <PROFILE_NAME>`

       As you create new profile, it will become active immediately

   - `<RESOURCE_DIRECTORY>` is `res` folder in your project
   
   - All suffixes are optional. You may specify ones you like. Suffixes that you omit
   will be ignored

3. Type
   ```
   ares unpack <PATH_TO_ZIP> [-n <NEW_FILES_NAME>]
   ```
   Files from zip will appear in your project!
   If you specify -n, files will be renamed

   You can also type
   ```
   ares unpack -p <PROFILE_NAME> <PATH_TO_ZIP> -n <NEW_FILES_NAME>
   ```
   to change profile on the fly. It will be selected as active for future


## Example
```
ares profile -a pet_project ~/dev/my_pet_project/app/src/main/res \
 --mdpi @1x \
 --xhdpi @2x \
 --xxhdpi @3x
```
Now download resources in zip (i.e. using Figma export) and unpack it
```
ares unpack ~Downloads/icon.zip -n icon
```

## All functions

- `ares profile -a <PROFILE_NAME> <RESOURCE_DIRECTORY> [SUFFIXES]` - adds profile
- `ares profile -l` - prints all profiles
- `ares profile -d <PROFILE_NAME>` - removes profile if it is not active
- `ares unpack -p` - change profile
- `ares unpack <PATH_TO_ZIP> [-n FILE_NAME]` - unpacks resources