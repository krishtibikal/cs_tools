"""
This file contains the methods to execute the 'scriptability compare' command.
"""
import pathlib

from thoughtspot_tml import YAMLTML
from thoughtspot_tml.tml import TML
from typer import Argument as A_

from cs_tools.cli.ux import console


def compare(
        file1: pathlib.Path = A_(
            ...,
            help='full path to the first TML file to compare.',
            metavar='FILE1',
            dir_okay=False,
            resolve_path=True
        ),
        file2: pathlib.Path = A_(
            ...,
            help='full path to the second TML file to compare.',
            metavar='FILE2',
            dir_okay=False,
            resolve_path=True
        ),
):
    """
    Compares two TML files for differences.
    """

    tml1 = _get_tmlobj(file1)
    tml2 = _get_tmlobj(file2)

    with console.status(f"[bold green]Comparing {file1} and {file2}[/]"):
        same = _compare_tml(file1.name, tml1, file2.name, tml2)
        console.log(f"{file1} is{'' if same else ' not'} the same as {file2}")


def _get_tmlobj(path: pathlib.Path) -> TML:
    """Returns a TML object from the file path."""
    with open(path, "r") as tmlfile:
        tmlstr = tmlfile.read()

    return YAMLTML.get_tml_object(tml_yaml_str=tmlstr)


def _compare_tml(file1: str, tml1: TML, file2: str, tml2: TML) -> bool:
    """Compares two TML objects, listing any differences."""
    return __compare_dict(file1, tml1.tml, file2, tml2.tml)


def __compare_dict(f1: str, d1: dict, f2: str, d2: dict) -> bool:
    """Compares two dictionaries, logging any changes."""
    if not (type(d1) is dict and type(d2) is dict):
        console.log(f"[bold red]{d1} and {d2} are different types.")
        return False

    same = True

    # See if there are any keys in the first one that are not in the second.
    for k1 in d1.keys():
        if k1 not in d2.keys():
            console.log(f"[bold red]{k1} not in {f2}[/]")
            same = False

    # See if there are any keys in the second one that are not in the first.
    for k2 in d2.keys():
        if k2 not in d1.keys():
            console.log(f"[bold red]{k2} not in {f1}[/]")
            same = False

    # get the common keys
    common_keys = list(set(d1.keys()) & set(d2.keys()))

    for k in common_keys:
        if type(d1[k]) is dict:
            same = __compare_dict(f1, d1[k], f2, d2[k]) and same  # need to set to false if one is false
        elif type(d1[k]) is list:
            same = __compare_list(f1, d1[k], f2, d2[k]) and same  # need to set to false if one is false
        else:
            if d1[k] != d2[k]:
                console.log(f"[bold red]Values for key '{k}' are different: [/]")
                console.log(f"[bold red]]\t{d1[k]} != {d2[k]}[/]")
                same = False

    return same


def __compare_list(f1: str, l1: list, f2: str, l2: list) -> bool:
    """Compares the contents of a list."""
    same = True

    if not (type(l1) is list and type(l2) is list):
        console.log(f"[bold red]{l1} and {l2} are different types.")
        return False

    if len(l1) != len(l2):
        console.log(f"[bold red]]\t{l1} != {l2}[/]")
        same = False

    for cnt in range(0, len(l1)):
        if type(l1[cnt]) is dict:
            same = __compare_dict(f1, l1[cnt], f2, l2[cnt]) and same
        elif type(l1[cnt]) is list:
            same = __compare_list(f1, l1[cnt], f2, l2[cnt]) and same
        else:
            if l1[cnt] != l2[cnt]:
                console.log(f"[bold red]Values are different: [/]")
                console.log(f"[bold red]]\t{l1[cnt]} != {l2[cnt]}[/]")
                same = False

    return same
