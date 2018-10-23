# Create Dictionary Search Tool
This tool use for build dictionary by your self.

    TXT -> TAB -> OPF -> PRC(Mobi)

## Requirements
- Python 3.6
- Clime
- Numpy
- Pyinstaller
- PyQt5

## Install libraries

    pip install -r requirements.txt

## Build
Build UI
    
    pyuic5.exe -x ui_design\Dict4Kindle.ui -o ui_dict_4_kindle.py

Build project

    pyinstaller build_dict4kinlde.spec
    
## Usage (for developer)
    python main.py  [option]  [use_for_option]

## Usage (for end user)
    dict4kindle.exe  [option]  [use_for_option]
    
## Release
    - 2018/10/20 (ver1.0): https://mega.nz/#!RlhhUQjJ!WfQtBC-Hja4NL0yWYu8lQgbnTfsvCCSdZ8Sb8mQ-7P0
    
