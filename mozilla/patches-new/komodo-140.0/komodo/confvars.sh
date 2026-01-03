#! /bin/sh
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

MOZ_APP_NAME=komodo
MOZ_APP_DISPLAYNAME="Komodo IDE"
MOZ_APP_VERSION=14.0.0
MOZ_APP_ID=komodo@activestate.com
MOZ_APP_VENDOR="ActiveState"
MOZ_APP_BASENAME="Komodo IDE"
MOZ_APP_REMOTINGNAME="komodo"

# Komodo-specific configuration
MOZ_KOMODO=1
MOZ_EXTENSIONS=1
MOZ_WEBEXTENSIONS=1

# Branding configuration
MOZ_BRANDING_DIRECTORY=komodo/branding
MOZ_OFFICIAL_BRANDING_DIRECTORY=other-licenses/branding/firefox

# Disable Firefox-specific features
MOZ_BROWSER_CHROME_URL=chrome://komodo/content/komodo.xul
MOZ_SAFE_BROWSING= 
MOZ_DATA_REPORTING= 
MOZ_HEALTHREPORT= 
MOZ_SERVICES_HEALTHREPORT= 
MOZ_SERVICES_SYNC= 

# Enable Komodo-specific features
MOZ_KOMODO_INTEGRATION=1
MOZ_KOMODO_DEVTOOLS=1
MOZ_KOMODO_DEBUGGER=1

# Disable unwanted Firefox features
MOZ_REQUIRE_SIGNING= 
MOZ_ADDON_SIGNING= 
MOZ_DISABLE_EXPORT_JS=1

# Enable development features
MOZ_DEVELOPER_REPO=1