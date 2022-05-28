from typing import Iterator, List, Optional

import typer
import click
from typer.main import get_command
from cs_tools.cli.loader import CSTool

from ._exceptions import MkDocsTyperException


def make_command_docs(
    tool: 'CSTool',
    command: str = None,
    meth: str = 'get_help',
    cd: str = r'C:\work\thoughtspot\cs_tools',
    venv: str = '.cs_tools',
    indent: int = 0
) -> Iterator[str]:
    """Create the Markdown lines for a command and its sub-commands."""
    tool.app._add_completion = False

    ctx_settings = {
        'help_option_names': ['--help', '--helpfull'],
        'max_content_width': 120,
    }

    cmd = get_command(tool.app)
    ctx = click.Context(cmd, info_name=f'cs_tools tools {tool.name}', **ctx_settings)

    if command is not None:
        cmd = cmd.get_command(ctx, command)
        ctx = click.Context(cmd, info_name=command, parent=ctx, **ctx_settings)

    from io import StringIO
    from rich.console import Console
    console = Console(file=StringIO())

    method = getattr(cmd, meth)
    console.print(method(ctx))
    text = console.file.getvalue()

    lines  = text.split('\n')
    yield (' ' * indent) + f'({venv}) {cd}>{ctx.command_path} --help'
    yield (' ' * indent) + ''
    yield from [(' ' * indent) + line for line in lines]
