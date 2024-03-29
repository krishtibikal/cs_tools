from collections.abc import Iterable
from typing import Any, List, Tuple
import itertools
import argparse
import pathlib
import zipfile
import shutil
import os

import nox_poetry as nox


ON_GITHUB = "GITHUB_ACTIONS" in os.environ
PY_VERSIONS = [
    "3.6.8",
    "3.7", "3.8",
    "3.9",
    "3.10"
]
HERE = pathlib.Path(__file__).parent
DIST = HERE / "dist"
DIST_PKGS = DIST / "pkgs"
REQS_TXT = DIST_PKGS / 'requirements.txt'
SUPPORTED_PLATFORM_MATRIX = {
    # fmt: off
    # PEP425: Compatibility Tags for Built Distributions
    "windows": ("win_amd64", ),

    # "macosx_12_x86_64",  # Moneterey [released: 2021.10.25]
    # "macosx_11_x86_64",  # Big Sur   [released: 2020.11.12]
    # Catalina (10.15) ----------------------> [EOL tbd]
    # Mojave   (10.14) ----------------------> [EOL 2021.10.25]
    "mac": (
        # Apple M1 Chip
        # "macosx_12_universal2",
        # Intel x84-64
        "macosx_12_x86_64",
        "macosx_11_x86_64",
        "macosx_10_15_x86_64",
        "macosx_10_14_x86_64"
    ),

    # PEP600: manylinux_x_y_<arch> based on glibc>=x.y  (future-proofed)
    # PEP599: manylinux2014_<arch> --> CentOS7 [EOL 2024.06.30]
    # PEP571: manylinux2010_<arch> --> CentOS6 [EOL 2020.11.30]
    # PEP513: manylinux1_<arch> -----> CentOS5 [EOL 2017.03.31]
    "linux": (
        "manylinux2014_x86_64", "manylinux_2_17_x86_64",  # strict, alias
        "manylinux2010_x86_64", "manylinux_2_12_x86_64",  # strict, alias
        "manylinux1_x86_64", "manylinux_2_5_x86_64",      # strict, alias
    ),
    # fmt: on
}


def grouped(iterable: Iterable, n: int = 2) -> Iterable:
    """
    Groups elements of iterable together.

      grouped('ABCDEFGH', n=2) --> AB CD EF GH
      grouped('ABCDEFGH', n=4) --> ABCD DEFG

    Parameters
    ----------
    iterable : Iterable
      any collection of elements

    n : int  [default, 2]
      chunks of the iterable to return
    """
    return zip(*[iter(iterable)] * n)


def _manual_resolver_fixes(requirements: pathlib.Path) -> None:
    # For some reason, the dependency solver produces an unreachable typing-extensions
    # marker. We're going to rewrite it.
    fixes = {
        'typing-extensions': 'typing-extensions==4.1.1; python_full_version >= "3.6.2" and python_full_version < "4.0.0"'
    }
    lines = []
    for line in requirements.read_text().split('\n'):
        if line.startswith(tuple(fixes)):
            package, _, _ = line.partition('==')
            line = fixes[package]
        lines.append(line)
    requirements.write_text('\n'.join(lines))


def zip_it(dir_: pathlib.Path, *, name: str, path: str = None, new: bool = True) -> None:
    """
    Zip a directory up.

    Parameters
    ----------
    dir_ : pathlib.Path
      directory to be zipped

    name :  str
      name of the zipfile

    path : str  [default: None]
      directory structure within the zipfile to enforce

    new: bool  [default: True]
      whether or not to create a new zipfile
    """
    if path is not None and path.endswith('/'):
        path = pathlib.Path(path).name

    if new:
        pathlib.Path(name).unlink(missing_ok=True)

    with zipfile.ZipFile(name, "a", zipfile.ZIP_DEFLATED) as zip_:
        for file in dir_.iterdir():
            arcname = path if path is None else f'{path}/{file.name}'

            if file.name == '__pycache__':
                continue
            if arcname in zip_.namelist():
                continue

            zip_.write(file, arcname=arcname)


@nox.session(name="vendor-packages", python=PY_VERSIONS, reuse_venv=not ON_GITHUB)
def vendor_packages(session):
    """
    Build offline distributable installer.

    For this to be truly effective, the builder must have access to all
    python versions in the PY_VERSIONS constraint. Consider using pyenv
    or docker to build.
    """
    first_run = session.python == '3.6.8'

    # TODO: use argparse for the following args
    # --silent         :: defaults to ON_GITHUB
    # --ensure-install :: run the poetry-install step
    # --no-cleanup     :: don't remove files

    session.run("poetry", "install", "--no-dev", external=True, silent=not ON_GITHUB)
    session.run(
        # fmt: off
        "poetry", "export",
        "-f", "requirements.txt",
        "--output", REQS_TXT.as_posix(),
        "--without-hashes",
        external=True,
        silent=not ON_GITHUB
        # fmt: on
    )

    session.run("poetry", "build", "--format", "wheel", external=True, silent=not ON_GITHUB)
    WHL_FILE = pathlib.Path(next(DIST_PKGS.parent.glob("cs_tools*.whl")))

    for platform, platforms in SUPPORTED_PLATFORM_MATRIX.items():
        dest = DIST_PKGS / platform

        session.log(f'cleaning {dest}..')
        shutil.rmtree(dest, ignore_errors=True)

        # CentOS 7 ships with pip vesion 9.x.x which doesn't understand PEP 571+
        # standardization efforts. Current versions of pip will only use the aliased
        # platform tags, so we'll have to ask for them separately. This is why we group
        # the platform tags.

        # download our dependencies
        # - since poetry found and resolved our dependencies, --no-deps is fine to use
        for platform_tags in grouped(platforms, n=2 if platform == "linux" else 1):
            session.run(
                # fmt: off
                "pip", "download",
                "-r", REQS_TXT.as_posix(),
                "--dest", dest.as_posix(),
                "--no-cache-dir",
                "--no-deps",
                *itertools.chain.from_iterable(["--platform", p] for p in platform_tags),
                silent=not ON_GITHUB
                # fmt: on
            )

        _manual_resolver_fixes(REQS_TXT)

        session.log(f'adding {WHL_FILE.name} to {platform}/')
        shutil.copyfile(WHL_FILE, dest / WHL_FILE.name)

        session.log(f'adding {REQS_TXT.name} to {platform}/')
        shutil.copyfile(REQS_TXT, dest / REQS_TXT.name)

        if not ON_GITHUB:
            session.log(f'zipping {platform}/ for distribution..')
            _, version, *_ = WHL_FILE.stem.split('-')
            archive = DIST / f"{platform}-cs_tools-{version}.zip"
            zip_it(dest, name=archive, path='pkgs/', new=first_run)
            zip_it(DIST / 'bootstrap', name=archive, path='bootstrap/', new=False)
            shutil.rmtree(dest, ignore_errors=True)

    if not ON_GITHUB:
        session.log('cleaning temporary files..')
        WHL_FILE.unlink()
        REQS_TXT.unlink()


@nox.session(name="bump-version", reuse_venv=not ON_GITHUB)
def bump_version(session: nox.Session) -> None:
    """
    Bump the package version.
    """
    parser = argparse.ArgumentParser(prog="nox -s version-bump")
    parser.add_argument(
        "--beta",
        help="mark the release or bump the beta version",
        dest="beta",
        action="store_true",
        default=False,        
    )
    ver = parser.add_mutually_exclusive_group()
    ver.add_argument(
        "--major",
        help="bump the major version, resetting minor and patch to 0",
        dest="major",
        action="store_true",
        default=False,
    )
    ver.add_argument(
        "--minor",
        help="bump the minor version, resetting patch to 0",
        dest="minor",
        action="store_true",
        default=False,
    )
    ver.add_argument(
        "--patch",
        help="bump the patch version",
        dest="patch",
        action="store_true",
        default=False,
    )

    args = parser.parse_args(args=session.posargs)

    def _get_version() -> str:
        local = {}
        txt = (HERE / 'cs_tools' / '_version.py').read_text()
        exec(txt, {}, local)
        return local['__version__']

    def _write_version(version: str) -> None:
        (HERE / 'cs_tools' / '_version.py').write_text(f"__version__ = '{version}'")

        import tomlkit
        pyproject = (HERE / 'pyproject.toml').read_text()
        doc = tomlkit.parse(pyproject)
        doc['tool']['poetry']['version'] = version
        txt = tomlkit.dumps(doc)
        (HERE / 'pyproject.toml').write_text(txt)

    __version__ = _get_version()
    major, minor, patch = __version__.split('.')
    patch, *in_beta = patch.split('b')

    if args.major and not in_beta:
        major, minor, patch = int(major) + 1, 0, 0
    elif args.minor and not in_beta:
        minor, patch = int(minor) + 1, 0
    elif args.patch and not in_beta:
        patch = int(patch) + 1

    if args.beta:
        v = "beta version"
        beta = f"b{int(in_beta[0]) + 1 if in_beta else 1}"

        if not in_beta and not any(args.major, args.minor, args.patch):
            patch = int(patch) + 1
    else:
        v = "version"
        beta = ""

    version = f'{major}.{minor}.{patch}{beta}'

    _write_version(version)
    session.run("git", "add", f"{HERE}/pyproject.toml", f"{HERE}/cs_tools/_version.py", external=True)
    # session.run("git", "commit", "-m", f"bump {v} --> ({version})", external=True)


@nox.session(python=PY_VERSIONS, reuse_venv=not ON_GITHUB)
def tests(session: nox.Session) -> None:
    """
    Ensure we test our code.
    """
    session.run("poetry", "install", external=True)
    session.run("ward")


# @nox.session(python=PY_VERSIONS, reuse_venv=not ON_GITHUB)
# def code_quality(session):
#     session.run("poetry", "install", external=True)
