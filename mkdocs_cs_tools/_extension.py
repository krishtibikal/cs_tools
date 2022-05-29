from typing import Callable, Iterable, Iterator
from typing import List, Any, List, Iterator
import re

import click
from typer.main import get_command
from cs_tools.cli.loader import CSTool

from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from cs_tools.cli.loader import CSTool
from cs_tools.const import TOOLS_DIR


class TyperProcessor(Preprocessor):
    def run(self, lines: List[str]) -> List[str]:
        return list(self._replace_blocks(lines, title='mkdocs-cs_tools', replace=self.replace_command_docs))

    def _replace_command_docs(self, **options) -> Iterator[str]:
        if 'tool' not in options:
            raise ValueError("Option 'tool' is required")

        tool = CSTool(TOOLS_DIR / options.pop('tool'))
        return self._make_command_docs(tool, **options)

    def _make_command_docs(
        self, 
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

    def _replace_blocks(self, lines: Iterable[str], title: str, replace: Callable[..., Iterable[str]]) -> Iterator[str]:
        """
        Find blocks of lines in the form of:

        :~~: <title>
            :<key1>: <value>
            :<key2>:
            ...

        And replace them with the lines returned by `replace(key1="<value1>", key2="", ...)`.
        """

        options = {}
        in_block_section = False
        indent = 0

        for line in lines:
            if in_block_section:
                match = re.search(r"^\s+:(?P<key>.+): (?:\s*(?P<value>\S+))?", line)
                if match is not None:
                    # New ':key:' or ':key: value' line, ingest it.
                    key = match.group("key")
                    value = match.group("value") or ""
                    options[key] = value
                    continue

                # Block is finished, flush it.
                in_block_section = False
                options['indent'] = indent
                yield from replace(**options)
                yield line
                continue

            match = re.search(rf":~~: {title}", line)
            if match is not None:
                indent = len(line) - len(line.lstrip(' '))
                # Block header, ingest it.
                in_block_section = True
                options = {}
            else:
                yield line



class MKTyperExtension(Extension):
    """
    Replace blocks like the following:

    ::: mkdocs-cs_tools
        :tool: searchable
        :command: app
        :meth: ...
        :cd: ...
        :venv: ...

    by Markdown documentation generated from the specified Typer application.
    """

    def extendMarkdown(self, md: Any) -> None:
        md.registerExtension(self)
        processor = TyperProcessor(md.parser)
        md.preprocessors.register(processor, "mk_typer", 142)


def makeExtension() -> Extension:
    return MKTyperExtension()
