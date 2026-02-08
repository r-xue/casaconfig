#!/usr/bin/env python3
# Copyright 2025 AUI, Inc. Washington DC, USA
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

# tries multiple sites to deal with the case where one site might be blocked
# to the user. This also deals with the case where a captive portal (e.g.
# a hotel wifi redirecting to a login page, so full access isn't available).

# have_network is also found in casagui

import concurrent.futures
from urllib.request import urlopen

def is_actually_online(url, timeout=3):
    """Returns True only if the URL returns a 204 No Content."""
    try:
        with urlopen(url, timeout=timeout) as resp:
            # Captive portals usually return 200 (the login page) 
            # or 302 (redirect). 204 means you are truly on the web.
            return resp.status == 204
    except Exception:
        return False

def have_network():
    urls = [
        "http://clients3.google.com",
        "http://cp.cloudflare.com",
        "http://connectivitycheck.gstatic.com",
        #"http://www.apple.com"  Note: Apple returns 200 usually
        "http://www.gstatic.com"
    ]

    # Use a ThreadPool to fire all requests at once
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(urls)) as executor:
        # map launches them all; as_completed lets us grab the first winner
        future_to_url = {executor.submit(is_actually_online, url): url for url in urls}
        
        for future in concurrent.futures.as_completed(future_to_url):
            if future.result(): # The first one that returns True
                # Shutdown remaining threads immediately to save resources
                executor.shutdown(wait=False, cancel_futures=True)
                return True
                
    return False

# Usage in a standard laptop app
if __name__ == "__main__":
    if have_network():
        print("Real internet access confirmed.")
    else:
        print("Offline or behind a captive portal.")
