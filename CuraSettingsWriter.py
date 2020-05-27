# Copyright (c) 2020 5axes
# Initiale Source from Johnny Matthews 
# The SnapShot plugin is released under the terms of the AGPLv3 or higher.

from UM.Application import Application
from cura.CuraVersion import CuraVersion  # type: ignore
from UM.Preferences import Preferences
from UM.Settings.ContainerRegistry import ContainerRegistry
from UM.Workspace.WorkspaceWriter import WorkspaceWriter

from UM.i18n import i18nCatalog
catalog = i18nCatalog("cura")


import UM.Settings.SettingRelation

class CuraSettingsWriter(WorkspaceWriter):
   
    def write(self, stream, nodes, mode):
        stream.write("<style>")
        stream.write(" .category { font-size:1.5em; } ")
        stream.write(" .off { background-color:grey; } ")
        stream.write(" .valueCol { width:200px;text-align:right }")
        stream.write("</style>")
        
        application = Application.getInstance()
        machine_manager = application.getMachineManager()        
        stack = application.getGlobalContainerStack()

        global_stack = machine_manager.activeMachine


        #jquery = open("plugins/plugins/CuraSettingsWriter/jquery-3.3.1.min.js","r", encoding="utf-8")
        
        stream.write("<script src='https://code.jquery.com/jquery-3.3.1.slim.min.js'></script>\n")
        stream.write("""<script>
                            $(document).ready(function(){
                                    $("#enabled").on("click",toggleDisabled);

                            });

                            function toggleDisabled(){
                                    $("tr.disabled").toggle();
                            }
                        </script>
                        <h1>Cura Settings Export</h1>
                        <button id='enabled'>Toggle Disabled</button><P>""")

        stream.write("<table width=50% border=1 cellpadding=3>")
        
        # Version
        stream.write("<tr>")
        stream.write("<td class='ok' style='width:50%;padding-left:25'>Cura Version</td>")
        stream.write("<td class='ok' colspan=2>" + str(CuraVersion) + "</td>")
        stream.write("</tr>\n")  
        # Job
        J_Name = Application.getInstance().getPrintInformation().jobName
        stream.write("<tr>")
        stream.write("<td class='ok' style='width:50%;padding-left:25'>Job Name</td>")
        stream.write("<td class='ok' colspan=2>" + str(J_Name) + "</td>")
        stream.write("</tr>\n")         
        # Snapshot
        #stream.write("<tr>")
        #stream.write("<td class='ok' colspan=3>" + str(F_Name) + "</td>")
        #stream.write("</tr>\n")
        #   Profile
        P_Name = global_stack.qualityChanges.getMetaData().get("name", "")
        stream.write("<tr>")
        stream.write("<td class='ok' style='width:50%;padding-left:25'>Profile</td>")
        stream.write("<td class='ok' colspan=2>" + str(P_Name) + "</td>")
        stream.write("</tr>\n")
        #   Quality
        Q_Name = global_stack.quality.getMetaData().get("name", "")
        stream.write("<tr>")
        stream.write("<td class='ok' style='width:50%;padding-left:25'>Quality</td>")
        stream.write("<td class='ok' colspan=2>" + str(Q_Name) + "</td>")
        stream.write("</tr>\n")
        #   Material
        # M_Name = extruder.material.getMetaData().get("material", "")
        extruders = list(global_stack.extruders.values())
        M_Name = extruders[0].material.getMetaData().get("material", "")
        stream.write("<tr>")
        stream.write("<td class='ok' style='width:50%;padding-left:25'>Material</td>")
        stream.write("<td class='ok' colspan=2>" + str(M_Name) + "</td>")
        stream.write("</tr>\n")
        
        # Define every section to get the same order as in the Cura Interface
        self._doTree(global_stack,"resolution",stream,0)
        self._doTree(global_stack,"shell",stream,0)
        self._doTree(global_stack,"infill",stream,0)
        self._doTree(global_stack,"material",stream,0)
        self._doTree(global_stack,"speed",stream,0)
        self._doTree(global_stack,"travel",stream,0)
        # If single extruder doesn't export the data
        extruder_count=stack.getProperty("machine_extruder_count", "value")
        if extruder_count>1 :
            self._doTree(global_stack,"dual",stream,0)
            
        self._doTree(global_stack,"cooling",stream,0)
        self._doTree(global_stack,"support",stream,0)
        self._doTree(global_stack,"platform_adhesion",stream,0)
        self._doTree(global_stack,"meshfix",stream,0)
        self._doTree(global_stack,"blackmagic",stream,0)
        self._doTree(global_stack,"experimental",stream,0)
        self._doTree(global_stack,"machine_settings",stream,0)

        # This Method is smarter but unfortunatly settings are not in the same ordrer as the Cura interface
        # for key in global_stack.getAllKeys():
        #     if global_stack.getProperty(key,"enabled") == True:
        #         if global_stack.getProperty(key,"type") == "category":
        #             self._doTree(global_stack,key,stream,0)

        stream.write("</table>")
        return True

    def _doTree(self,stack,key,stream,depth):   
        #output node
        if stack.getProperty(key,"type") == "category":
            stream.write("<tr>")
            stream.write("<td class=category colspan=3>" + str(stack.getProperty(key,"label")) + "</td>")
            #stream.write("<td class=category>" + str(key) + "</td>")
            stream.write("</tr>\n")
        else:
            style = "ok"    
            if stack.getProperty(key,"enabled") == False:
                style = "off"
                stream.write("<tr class=disabled>")
            else:
                stream.write("<tr>")
            
            definition_key=key + " label" 
            # untranslated_label=stack.getProperty(key,"label").capitalize()
            untranslated_label=stack.getProperty(key,"label")
            # translated_label=catalog.i18nc(definition_key, untranslated_label)  
            translated_label=catalog.i18nc("@label", untranslated_label)
            
            # translated_label=catalog.i18nc("@label", key)
            # translated_label=catalog.i18n(untranslated_label)
            
            # catalog.i18nc("@tooltip", "Outer Wall") -> OK
            # catalog.i18nc("@label", "Outer Wall") -> KO
            stream.write("<td class="+style+" style='width:50%;padding-left:"+str(depth*25)+"'>" + str(translated_label) + "</td>")
            GetType=stack.getProperty(key,"type")
            GetVal=stack.getProperty(key,"value")
            if str(GetType)=='float':
                GelValStr="{:.2f}".format(GetVal).replace(".00", "")  # Formatage
            else:
                GelValStr=str(GetVal)
                
            stream.write("<td class='"+style+" valueCol'>" + GelValStr + "</td>")
            stream.write("<td class="+style+" >" + str(stack.getProperty(key,"unit")) + "</td>")
            
            stream.write("</tr>\n")

        #look for children
        if len(stack.getSettingDefinition(key).children) > 0:
            for i in stack.getSettingDefinition(key).children:       
                self._doTree(stack,i.key,stream,depth+1)
                    
                   
