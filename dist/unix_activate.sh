#!/bin/bash
# Activate the CS Tools virtual environment.
#
# Written by: Nick Cooper <nicholas.cooper@thoughtspot.com>
# Last Modified: 2021/05/18
# Version: 0.1.0
#
# CHANGELOG
# v0.1.0 - INITIAL RELEASE
#
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
    mkdir -p $APP_DIR
    python3 -m venv "${APP_DIR}/.cs_tools"
    source $_ACTIVATE

    if [[ $install_type == 'local' ]]; then
        pip install -r reqs/offline-install.txt --find-links=pkgs/ --no-cache-dir --no-index
    elif [[ $install_type == 'remote' ]]; then
        pip install -r reqs/requirements.txt --no-cache-dir --no-index
    else
        error "no option like ${install_type}, type either 'local' or 'remote'"
    fi
}


activate () {
    # Activate the virtual environment.
    #
    # cmd switch /k instructs command prompt to issue the command and then
    # stay open (normally so you can view results). In our case, we're starting
    # a separate process for the explicit purpose of using that as our tools
    # window.
    #
    py_args=${1:-interactive}

    if [[ $py_args == 'interactive' ]]; then
        clear
        source $_ACTIVATE
        cs_tools
        echo ' '
    fi
    # TODO: augment with the ability to use in Task Scheduler.
    #       - should accept args list and pass to $_ACTIVATE appropriately.
}


if [[ -f "${APP_DIR}/.cs_tools/bin/activate" ]]; then
    activate
else
    setup_venv 'local'
    activate
fi
