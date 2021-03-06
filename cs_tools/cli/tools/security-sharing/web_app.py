from typing import List, Dict, Any
import pathlib
import json

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request, Body


HERE = pathlib.Path(__file__).parent
_scoped = {}


web_app = FastAPI()
web_app.mount('/static', StaticFiles(directory=f'{HERE}/static'), name='static')
templates = Jinja2Templates(directory=f'{HERE}/static')


#
# EVENT LISTENERS
#


# @web_app.on_event('startup')
# async def _():
#     typer.launch('http://cs_tools.localho.st:5000/')


#
# MAIN WEB APPLICATION
#


@web_app.get('/', response_class=HTMLResponse)
async def read_index(request: Request):
    data = {
        'request': request,
        'host': _scoped['ts'].platform.url,
        'user': _scoped['ts'].me.display_name
    }
    return templates.TemplateResponse('index.html', data)


#
# REST API SHIM
#
#  NOTE:
#    The primary goal of cs_tools is to be as no-nonsense as possible. Navigating CORS
#    restrictions, while not incredibly difficult, can get fairly involved based on the
#    client's network architecture.
#
#    By allowing the frontend to talk to the internal python API, we bypass the need to
#    have the browser calling the ThoughtSpot server directly.
#


@web_app.post('/api/security/share')
async def _(type: str=Body(...), guids: List[str]=Body(...), permissions: Dict[str, Any]=Body(...)):
    """
    TSSetPermissionRequest
    """
    permissions = {guid: data['shareMode'] for guid, data in permissions.items()}
    r = _scoped['ts'].api._security.share(type=type, id=guids, permissions=permissions)

    try:
        return r.json()
    except json.JSONDecodeError:
        pass


@web_app.post('/api/defined_permission')
# async def _(request: Request):  # could also do it like this ... how lazy to be?
async def _(type: str=Body(...), guids: List[str]=Body(...)):
    """
    TSGetTablePermissionsRequest
    """
    r = _scoped['ts'].api._security.defined_permission(type=type, id=guids)
    return r.json()


@web_app.get('/api/list_columns/{guid}')
async def _(guid: str):
    """
    TSGetColumnsRequest
    """
    r = _scoped['ts'].api._metadata.list_columns(id=guid)
    return r.json()


@web_app.get('/api/user_groups')
async def _():
    """
    TSGetUserGroupsRequest
    """
    params = {
        'type': 'USER_GROUP',
        'category': 'ALL',
        'sort': 'DEFAULT',
        'offset': -1,
        'auto_created': False
    }
    r = _scoped['ts'].api.metadata.list_object_headers(**params)
    return r.json()


@web_app.get('/api/tables')
async def _():
    """
    TSGetTablesRequest
    """
    params = {
        'type': 'LOGICAL_TABLE',
        'subtypes': ['ONE_TO_ONE_LOGICAL'],
        'category': 'ALL',
        'sort': 'DEFAULT',
        'offset': -1
    }
    r = _scoped['ts'].api.metadata.list_object_headers(**params)
    return r.json()
