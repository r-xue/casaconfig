# Copyright 2020 AUI, Inc. Washington DC, USA
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
"""
this module will be included in the api
"""


def measures_available():
    """
    List available measures versions on the ASTRON server

    This returns a list of the measures files available on the ASTRON
    server. The version parameter of measures_update must be one
    of the values in that list if set (otherwise the most recent version
    in this list is used).

    Parameters
       None
    
    Returns
       version names returned as list of strings

    Raises:
       - casaconfig.NoNetwork - raised when there is no network (have_data returns False)
       - casaconfig.RemoteError - raised when when a socket.gaierror is seen, unlikely due to the have_network check
       - Exception: raised when any unexpected exception happens

    """
    from ftplib import FTP
    import socket

    from casaconfig import RemoteError
    from casaconfig import NoNetwork

    from .have_network import have_network

    if not have_network():
        raise NoNetwork("can not find the list of available measures data")
    
    files = []
    try:
        ftp = FTP('ftp.astron.nl')
        rc = ftp.login()
        rc = ftp.cwd('outgoing/Measures')
        files = ftp.nlst()
        ftp.quit()
        #files = [ff.replace('WSRT_Measures','').replace('.ztar','').replace('_','') for ff in files]
        files = [ff for ff in files if (len(ff) > 0) and (not ff.endswith('.dat'))]
    except socket.gaierror as gaierr:
        raise RemoteError("Unable to retrieve list of available measures versions : " + str(gaierr)) from None
    except Exception as exc:
        msg = "Unexpected exception while getting list of available measures versions : " + str(exc)
        raise Exception(msg)
        
    return files
