import logging.config
import datetime as dt
import platform
import pathlib
import logging
import shutil

from typer import Argument as A_, Option as O_
import pydantic
import click
import typer
import toml

from cs_tools.helpers.cli_ux import console, CSToolsGroup, CSToolsCommand
from cs_tools.helpers.loader import _gather_tools
from cs_tools.util.algo import deep_update
from cs_tools._version import __version__
from cs_tools.settings import TSConfig
from cs_tools.const import APP_DIR


log = logging.getLogger(__name__)


def _show_hidden_tool_options(
    private: bool=O_(False, '--private', hidden=True)
):
    """
    Care for the hidden options.
    """
    ctx = click.get_current_context()

    if ctx.invoked_subcommand:
        return

    if private:
        unhidden_cmds = {}

        for name, command in ctx.command.commands.items():
            if name == '__example_app__':
                continue

            command.hidden = False
            unhidden_cmds[name] = command

        ctx.command.commands = unhidden_cmds

    console.print(ctx.get_help())
    raise typer.Exit(code=0)


app = typer.Typer(
    cls=CSToolsGroup,
    name="cs_tools",
    help="""
    Welcome to CS Tools!

    These are scripts and utilities used to assist in the development,
    implementation, and administration of your ThoughtSpot platform.

    All tools are provided as-is. While every effort has been made to
    test and certify use of these tools in the various supported
    ThoughtSpot deployments, each environment is different!

    [bold yellow]You should ALWAYS take a snapshot before you make any
    significant changes to your environment![/]

    \b
    [green]For additional help, please visit our documentation![/]
    [blue]https://thoughtspot.github.io/cs_tools/[/]
    """,
    add_completion=False,
    context_settings={
        # global settings
        'help_option_names': ['--help', '-h'],

        # allow responsive console design
        'max_content_width':
            console.width if console.width <= 120 else max(120, console.width * .65),

        # allow case-insensitive commands
        'token_normalize_func': lambda x: x.lower()
    },
    options_metavar='[--version, --help]'
)


tools_app = typer.Typer(
    cls=CSToolsGroup,
    name='tools',
    help="""
    Run an installed tool.

    Tools are a collection of different scripts to perform different functions
    which aren't native to the ThoughtSpot or advanced functionality for
    clients who have a well-adopted platform.
    """,
    subcommand_metavar='<tool>',
    callback=_show_hidden_tool_options,
    invoke_without_command=True
)


log_app = typer.Typer(
    cls=CSToolsGroup,
    name='logs',
    help="""
    Export and view log files.

    Something went wrong? Log files will help the ThoughtSpot team understand
    how to debug and fix it.
    """
)


cfg_app = typer.Typer(
    cls=CSToolsGroup,
    name='config',
    help="""
    Work with dedicated config files.

    Configuration files can be set and saved on a machine in order to eliminate
    passing cluster details and credentials to every tool.
    """
)


@app.command('platform', cls=CSToolsCommand, hidden=True)
def _platform():
    """
    Return details about this machine for debugging purposes.
    """
    console.print(f"""
        [PLATFORM DETAILS]
        system: {platform.system()} (detail: {platform.platform()})
        python: {platform.python_version()}
        datetime: {dt.datetime.now(dt.timezone.utc).astimezone().strftime('%Y-%m-%d %H:%M:%S%z')}
        cs_tools: {__version__}
    """)


@log_app.command(cls=CSToolsCommand)
def export(
    save_path: pathlib.Path = A_(
        ...,
        help='location on disk to save logs to',
        metavar='DIRECTORY',
        file_okay=False,
        resolve_path=True
    ),
):
    """
    Grab logs to share with ThoughtSpot.
    """
    save_path.mkdir(parents=True, exist_ok=True)
    log_dir = APP_DIR / 'logs'

    for log in log_dir.iterdir():
        shutil.copy(log, save_path)


@cfg_app.command(cls=CSToolsCommand)
def show():
    """
    Show the location of the currently saved config files.
    """
    if not APP_DIR.exists():
        console.print('[yellow]no config files found just yet![/]')
        raise typer.Exit()

    configs = [f for f in APP_DIR.iterdir() if f.name.startswith('cluster-cfg_')]
    s = 's' if (len(configs) > 1 or len(configs) == 0) else ''

    console.print(f'Cluster configs located at: {APP_DIR}')
    console.print(f'\nFound {len(configs)} config{s}')

    for file in configs:
        console.print(f"  - {file.stem[len('cluster-cfg_'):]}")


@cfg_app.command(cls=CSToolsCommand)
def create(
    name: str=O_(..., help='config file identifier', prompt=True),
    host: str=O_(..., help='thoughtspot server', prompt=True),
    port: int=O_(None, help='optional, port of the thoughtspot server'),
    username: str=O_(..., help='username when logging into ThoughtSpot', prompt=True),
    password: str=O_(..., help='password when logging into ThoughtSpot', hide_input=True, prompt=True),
    temp_dir: pathlib.Path=O_(
        APP_DIR,
        '--temp_dir',
        help='location on disk to save temporary files',
        file_okay=False,
        resolve_path=True,
        show_default=False
    ),
    disable_ssl: bool=O_(False, '--disable_ssl', help='disable SSL verification', show_default=False),
    disable_sso: bool=O_(False, '--disable_sso', help='disable automatic SAML redirect', show_default=False),
    verbose: bool=O_(False, '--verbose', help='enable verbose logging by default', show_default=False)
):
    """
    Create a new config file.
    """
    config = TSConfig.from_cli_args(
                 host=host, username=username, password=password, temp_dir=temp_dir,
                 disable_ssl=disable_ssl, disable_sso=disable_sso, verbose=verbose
             )

    file = APP_DIR / f'cluster-cfg_{name}.toml'

    if file.exists():
        console.print(f'[red]cluster configuration file "{name}" already exists[/]')
        console.print(f'try using "cs_tools modify {name}" instead!')
        raise typer.Exit()

    with file.open('w') as t:
        toml.dump(config.dict(), t)

    console.print(f'saved cluster configuration file "{name}"')


@cfg_app.command(cls=CSToolsCommand)
def modify(
    name: str=O_(..., help='config file identifier', prompt=True),
    host: str=O_(None, help='thoughtspot server'),
    port: int=O_(None, help='optional, port of the thoughtspot server'),
    username: str=O_(None, help='username when logging into ThoughtSpot'),
    password: str=O_(None, help='password when logging into ThoughtSpot'),
    temp_dir: pathlib.Path=O_(
        None,
        '--temp_dir',
        help='location on disk to save temporary files',
        file_okay=False,
        resolve_path=True,
        show_default=False
    ),
    disable_ssl: bool=O_(None, '--disable_ssl/--no-disable_ssl', help='disable SSL verification', show_default=False),
    disable_sso: bool=O_(None, '--disable_sso/--no-disable_sso', help='disable automatic SAML redirect', show_default=False),
    verbose: bool=O_(None, '--verbose/--normal', help='enable verbose logging by default', show_default=False)
):
    """
    Modify an existing config file.
    """
    file = APP_DIR / f'cluster-cfg_{name}.toml'
    old  = TSConfig.from_toml(file).dict()

    data = TSConfig.from_cli_args(
                host=host, port=port, username=username, password=password,
                temp_dir=temp_dir, disable_ssl=disable_ssl, disable_sso=disable_sso,
                verbose=verbose, validate=False, default=False
            ).dict()

    new = deep_update(old, data, ignore=None)

    try:
        config = TSConfig(**new)
    except pydantic.ValidationError as e:
        console.print(f'[error]{e}')
        raise typer.Exit(-1)

    with file.open('w') as t:
        toml.dump(config.dict(), t)

    console.print(f'saved cluster configuration file "{name}"')


@cfg_app.command(cls=CSToolsCommand)
def delete(
    name: str=O_(..., help='config file identifier', prompt=True)
):
    """
    Delete a config file.
    """
    file = pathlib.Path(typer.get_app_dir('cs_tools')) / f'cluster-cfg_{name}.toml'

    if not file.exists():
        console.print(f'[yellow]cluster configuration file "{name}" does not exist[/]')
        raise typer.Exit()

    file.unlink()
    console.print(f'removed cluster configuration file "{name}"')


def _clean_logs(now):
    logs_dir = APP_DIR / 'logs'
    logs_dir.mkdir(parents=True, exist_ok=True)

    # keep only the last 25 logfiles
    lifo = sorted(logs_dir.iterdir(), reverse=True)

    for idx, log in enumerate(lifo):
        if idx > 25:
            log.unlink()


def run():
    """
    Entrypoint into cs_tools.
    """
    _gather_tools(tools_app)
    app.add_typer(tools_app)
    app.add_typer(cfg_app)
    app.add_typer(log_app)

    # SETUP LOGGING
    now = dt.datetime.now().strftime('%Y-%m-%dT%H_%M_%S')
    _clean_logs(now)

    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '[%(levelname)s - %(asctime)s] [%(name)s - %(module)s.%(funcName)s %(lineno)d] %(message)s'
            }
        },
        'handlers': {
            'to_file': {
                'formatter': 'verbose',
                'level': 'DEBUG',     # user can override in their config file
                'class': 'logging.FileHandler',
                # RotatingFileHandler.__init__ params...
                'filename': f'{APP_DIR}/logs/{now}.log',
                'mode': 'w',          # Create a new file for each run of cs_tools.
                'encoding': 'utf-8',  # Handle unicode fun.
                'delay': True         # Don't create a file if no logging is done.
            },
            'to_console': {
                'level': 'INFO',
                'class': 'rich.logging.RichHandler',
                # rich.__init__ params...
                'console': console,
                'show_level': False,
                'markup': True,
                'log_time_format': '[%X]'
            }
        },
        'loggers': {},
        'root': {
            'level': 'DEBUG',
            'handlers': ['to_file', 'to_console']
        }
    })

    logging.getLogger('urllib3').setLevel(logging.ERROR)
    logging.getLogger('httpx').setLevel(logging.ERROR)

    try:
        app()
    except Exception as e:
        log.debug('whoopsie, something went wrong!', exc_info=True)

        if hasattr(e, 'warning'):
            e = e.warning
        else:
            e = f'{type(e).__name__}: {e}'

        log.exception(f'[error]{e}')