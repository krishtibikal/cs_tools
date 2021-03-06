#!/bin/bash
# Setup and install the CS Tools virtual environment.
#
# Written by: Nick Cooper <nicholas.cooper@thoughtspot.com>
# Last Modified: 2021/05/18
# Version: 0.1.0
#
# CHANGELOG
# v0.1.0 - INITIAL RELEASE
#
INSTALL_TYPE=${1:-local}

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
APP_DIR="${HOME}/.config/cs_tools"
_ACTIVATE="${APP_DIR}/.cs_tools/bin/activate"


error () {
    # Log a warning message and exit.
    #
    # Nothing special. There's a pause in here so the user knows where they
    # might've gone wrong.
    #
    # Parameters
    # ----------
    # msg : str
    #   message to emit in the warning
    #
    >&2 echo "$*"
    exit
}


check_python () {
    # Check if installed Python distro meets a specific verison.
    #
    # If no python can be found on the machine, then we error out and ask the
    # user to install python first.
    #
    # If an insufficient version of python is found on the machine, then we
    # error out and ask the user to upgrade to meet the specified version.
    #
    # Parameters
    # ----------
    # major : int
    #   supported python major version
    #
    # minor : int
    #   supported python minor version
    #
    # micro : int
    #   supported python micro version
    #
    major=$1
    minor=$2
    micro=$3

    req_met=$(python3 -c "import sys;print(sys.version_info >= (${major}, ${minor}, ${micro}))")
    if [[ $req_met == "True" ]]; then return; fi

    msg="
    Python needs to be updated in order to run CS Tools!
    
    The mininum supported version is $major.$minor.$micro

    If this machine is the same that your ThoughtSpot application is hosted on, please
    consult with your ThoughtSpot support team to upgrade Python.

    If this machine is your own, consider first your IT department's security policies,
    and then running the below commands in order to get the latest Python distribution.

        sudo apt-get update
        sudo apt-get install python3
    "
    error "$msg"
}


setup_venv () {
    # Setup a virtual environment.
    #
    # The requirements are different based on if you can access the outside
    # internet or not. All packages are distributed locally alonside this
    # script, but it's possible to grab them all from PyPI and Github instead.
    # 
    # Parameters
    # ----------
    # install_type : str , default 'local'
    #   either local or remote, where to source install packages from
    #
    install_type=${1:-local}
    python_version=$(python3 -c "import sys;print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    pip_install="$APP_DIR/.cs_tools/bin/python -m pip install --upgrade --no-cache-dir --force-reinstall"
    mkdir -p $APP_DIR
    python3 -m venv "${APP_DIR}/.cs_tools"
    source $_ACTIVATE

    if [[ $python_version == '3.6' ]]; then
        py="py36-"
    else
        py=""
    fi

    if [[ $install_type == 'local' ]]; then
        $pip_install -r $SCRIPT_DIR/reqs/${py}offline-install.txt --find-links=$SCRIPT_DIR/pkgs/ --no-index
    elif [[ $install_type == 'remote' ]]; then
        $pip_install -r $SCRIPT_DIR/reqs/${py}requirements.txt --no-cache-dir
    else
        error "no option like ${install_type}, type either 'local' or 'remote'"
    fi
}


set_envt_variables () {
    #
    #
    #

    # convert UTF-8 to en_US.
    LC_ALL=en_US
    export LC_ALL

    # ensure proper encoding for python
    PYTHONIOENCODING=utf-8
    export PYTHONIOENCODING
}


check_python 3 6 8
setup_venv $INSTALL_TYPE
set_envt_variables
source "$SCRIPT_DIR/unix_activate.sh"
