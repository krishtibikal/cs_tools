from typer import Argument as A_, Option as O_  # noqa
import uvicorn
import typer

from cs_tools.helpers.cli_ux import console, frontend, RichGroup, RichCommand
from cs_tools.settings import TSConfig
from cs_tools.api import ThoughtSpot

from .web_app import _scoped


app = typer.Typer(
    help="""
    One-liner describing the tool.

    Further explanation explaining the tool's usage or purpose. This can
    be as long as is necessary, but be mindful of much content you type
    here as the full text will display in the console when the user
    types...

      cs_tools tools my-cool-app --help

    If more ideas need to be conveyed, use separate paragraphs. Content
    will be wrapped to the console spec (default: 125 characters) unless
    you use a control character.

    Many tools augment a ThoughtSpot service. If they do, a relevant
    documentation link should be provided.

    \b
    For further information on <idea expressed in doc>, please refer to:
      https://docs.thoughtspot.com/path/to/documenation-link.html

    \f
    DEV NOTE:

      Two control characters are offered in order to help with
      docstrings in typer App helptext and command helptext
      (docstrings).

      \b - Preserve Whitespace / formatting.
      \f - EOF, don't include anything after this character in helptext.
    """,
    cls=RichGroup
)


@app.command(cls=RichCommand)
@frontend
def run(
    **frontend_kw
):
    """
    """
    cfg = TSConfig.from_cli_args(**frontend_kw, interactive=True)
    console.print('starting webserver...')

    with ThoughtSpot(cfg) as api:
        _scoped['api'] = api

        uvicorn.run(
            'cs_tools.tools._cls-sharing.web_app:web_app',
            host='127.0.0.1',
            port=5000,
            # log_config=None
        )
