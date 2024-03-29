from typing import Any, Dict
import logging
import copy

import httpx

from cs_tools.api.models import (
    _Connection,
    _Dependency,
    _Metadata,
    _Periscope,
    _Security,
    _Session,
    Data,
    Group,
    Logs,
    Metadata,
    Security,
    TSDataService,
    User
)
from cs_tools.api.util import filter_none


log = logging.getLogger(__name__)


def _secure_for_log(kw) -> Dict[str, Any]:
    # This doesn't need to be a formal utility.
    # We're essentially just popping the password so it doesn't get logged
    try:
        secure = copy.deepcopy(kw)
    except TypeError:
        secure = copy.deepcopy({k: v for k, v in kw.items() if k not in ('file', 'files')})

    secure.get('data', {}).pop('password', None)
    return secure


class _RESTAPIv1:
    """
    Implementation of the REST API v1.

    Model endpoints are classified by how they appear in Swagger.
    """
    def __init__(self, config, ts):
        self._config = config
        self._ts = ts
        self._http = httpx.Client(
            headers={'X-Requested-By': 'ThoughtSpot'},
            verify=not config.thoughtspot.disable_ssl,
            timeout=5 * 60.0,
            base_url=config.thoughtspot.fullpath
        )

        # remote TQL & tsload services
        self.ts_dataservice = TSDataService(self)

        # public API endpoints
        self.data = Data(self)
        self.group = Group(self)
        self.metadata = Metadata(self)
        self.security = Security(self)
        self.user = User(self)
        self.logs = Logs(self)

        # private API endpoints
        self._connection = _Connection(self)
        self._dependency = _Dependency(self)
        self._metadata = _Metadata(self)
        self._periscope = _Periscope(self)
        self._security = _Security(self)
        self._session = _Session(self)

    def request(
        self,
        method: str,
        endpoint: str,
        *,
        privacy: str='public',
        timeout: int=-1,
        **kw
    ) -> httpx.Response:
        """
        Make a request over to the API.

        Parameters
        ----------
        method : str
            http method to call: one of GET, POST, PUT, DELETE

        endpoint : str
            api endpoint to call, as the slug appears in swagger

            examples..
              metadata/list
              session/login

            If an absolute URL is given, ignore the base URL set on the rest
            client interface. In this setting, the privacy keyword argument is
            ignored.

        privacy : str = 'public'
            privacy setting for the api call, which determines the route

            examples..
                     public = callosum/v1/tspublic/v1
                    private = callusom/v1
                dataservice = ts_dataservice/v1/public

        **kw
            passed into the httpx.request call
        """
        # "httpx.Client.timeout = None" has meaning, -1 does not.
        if timeout == -1:
            timeout = self._http.timeout

        if httpx.URL(endpoint).is_relative_url:
            _privacy = {
                # IF NOT FOUND IN THIS MAPPING, THEN IT'S AN UNDOCUMENTED API
                'public': 'callosum/v1/tspublic/v1',
                'private': 'callosum/v1',
                'dataservice': 'ts_dataservice/v1/public'
            }

            endpoint = f'{_privacy.get(privacy, privacy)}/{endpoint}'

            if privacy not in _privacy:
                log.warning(f'using an undocumented api! :: {endpoint}')

        kw = filter_none(kw)
        log.debug(f'{method} >> {endpoint} with data:\n\tkwargs={_secure_for_log(kw)}')

        meth = getattr(self._http, method.lower())
        r = meth(endpoint, **kw, timeout=timeout)
        r.raise_for_status()
        log.debug(f'<< HTTP: {r.status_code}')

        if r.text and self._config.verbose:
            log.debug('<< CONTENT:\n\n%s', r.text)

        return r
