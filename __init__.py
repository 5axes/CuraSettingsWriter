# Copyright (c) 2020 5axes
# The SnapShot plugin is released under the terms of the AGPLv3 or higher.

from . import CuraSettingsWriter

from UM.i18n import i18nCatalog
catalog = i18nCatalog("cura")

def getMetaData():
    return {
        "workspace_writer": { 
            "output": [{
                "extension": "html",
                "description": catalog.i18nc("@item:inlistbox", "Cura Settings Documentation"),
                "mime_type": "text/html"
            }]
        }
    }

def register(app):
    return { "workspace_writer": CuraSettingsWriter.CuraSettingsWriter() }
