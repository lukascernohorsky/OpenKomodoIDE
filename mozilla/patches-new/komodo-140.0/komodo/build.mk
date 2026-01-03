# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Komodo build configuration

include $(topsrcdir)/config/rules.mk

# Komodo-specific build targets
libs::
	$(INSTALL) $(IFLAGS1) $(srcdir)/profile/komodo.js $(DIST)/bin/defaults/pref/
	$(INSTALL) $(IFLAGS1) $(srcdir)/profile/prefs.js $(DIST)/bin/defaults/pref/

# Komodo branding files
ifdef MOZ_BRANDING_DIRECTORY
libs::
	$(INSTALL) $(IFLAGS1) $(srcdir)/branding/komodo.ico $(DIST)/bin/chrome/icons/default/
	$(INSTALL) $(IFLAGS1) $(srcdir)/branding/komodo.png $(DIST)/bin/chrome/icons/default/
endif

# Komodo application files
ifdef MOZ_WIDGET_TOOLKIT
ifneq (,$(filter windows cocoa,$(MOZ_WIDGET_TOOLKIT)))
libs::
	$(INSTALL) $(IFLAGS1) $(srcdir)/app/komodo.ico $(DIST)/bin/
endif
ifneq (,$(filter cocoa,$(MOZ_WIDGET_TOOLKIT)))
libs::
	$(INSTALL) $(IFLAGS1) $(srcdir)/app/komodo.icns $(DIST)/bin/
endif
ifneq (,$(filter gtk2 gtk3,$(MOZ_WIDGET_TOOLKIT)))
libs::
	$(INSTALL) $(IFLAGS1) $(srcdir)/app/default.xpm $(DIST)/bin/chrome/icons/default/
endif
endif

# Komodo-specific cleanup
clean::
	$(RM) $(DIST)/bin/defaults/pref/komodo.js
	$(RM) $(DIST)/bin/defaults/pref/prefs.js
	$(RM) $(DIST)/bin/chrome/icons/default/komodo.ico
	$(RM) $(DIST)/bin/chrome/icons/default/komodo.png
	$(RM) $(DIST)/bin/komodo.ico
	$(RM) $(DIST)/bin/komodo.icns
	$(RM) $(DIST)/bin/chrome/icons/default/default.xpm