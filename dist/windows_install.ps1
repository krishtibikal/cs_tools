# Setup and install the CS Tools virtual environment.
#
# Written by: Nick Cooper <nicholas.cooper@thoughtspot.com>
# Last Modified: 2022/06/02
# Version: 0.3.0
#
# CHANGELOG
# v0.1.0 - INITIAL RELEASE
# v0.2.0 - activate from .bat --> .ps1
# v0.3.0 - care for py36 installs
#
param ($INSTALL_TYPE = 'local')


$NL = [Environment]::NewLine
$SCRIPT_DIR = $PSScriptRoot
$APP_DIR = "$env:APPDATA\cs_tools"
$_ACTIVATE = "$APP_DIR\.cs_tools\Scripts\Activate"


function error ($msg) {
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
    write-warning $msg
    write-host    $NL
    pause
    exit
}


function check_python($major, $minor, $micro) {
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
    try   {
        $req_met = (&{python -c "import sys;print(sys.version_info >= ($major, $minor, $micro))"})

        if ( $req_met -eq "True" ) { return }

        $msg = "
        Python needs to be updated in order to run CS Tools!

        The mininum supported version is $major.$minor.$micro

        Please download python at the following link:
        https://www.python.org/downloads/
        "
        error $msg
    }
    catch {
        $msg = "
        Python does not exist on this machine.

        The mininum supported version is $major.$minor.$micro
        
        Please download python at the following link:
        https://www.python.org/downloads/

        Ensure that you check the option to 'Add Python to PATH' in the
        setup window!
        "
        error $msg
    }
}


function setup_venv ($install_type = 'local') {
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
    $python_version = (&{python -c "import sys;print(f'{sys.version_info.major}.{sys.version_info.minor}')"})
    $pip_install = "$APP_DIR\.cs_tools\Scripts\python.exe -m pip install --upgrade --no-cache-dir --force-reinstall"
    mkdir $APP_DIR -ErrorAction SilentlyContinue
    python -m venv "$APP_DIR\.cs_tools"
    & "$_ACTIVATE.ps1"

    if ( $python_version -eq '3.6' ) {
        $py = "py36-"
    }
    else {
        $py = ""
    }

    if ( $install_type -eq 'local' ) {
        Invoke-Expression "$pip_install -r $SCRIPT_DIR/reqs/" + $py + "offline-install.txt --find-links=$SCRIPT_DIR/pkgs/ --no-index"
    }
    elseif ( $install_type -eq 'remote' ) {
        Invoke-Expression "$pip_install -r $SCRIPT_DIR/reqs/" + $py + "requirements.txt"
    }
    else {
        error 'no option like $install_type, type either "local" or "remote"'
    }
}

check_python 3 6 8
setup_venv $INSTALL_TYPE
powershell -ExecutionPolicy Bypass ./windows_activate.ps1
