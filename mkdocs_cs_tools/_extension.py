from typing import Any, List, Iterator

from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from cs_tools.cli.loader import CSTool
from cs_tools.const import TOOLS_DIR

from ._exceptions import MkDocsTyperException
from ._processing import replace_blocks
from ._docs import make_command_docs


def replace_command_docs(**options: Any) -> Iterator[str]:
    if 'tool' not in options:
        raise MkDocsTyperException("Option 'tool' is required")

    tool = CSTool(TOOLS_DIR / options.pop('tool'))
    return make_command_docs(tool, **options)


class TyperProcessor(Preprocessor):
    def run(self, lines: List[str]) -> List[str]:
        return list(replace_blocks(lines, title='mkdocs-cs_tools', replace=replace_command_docs))


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
