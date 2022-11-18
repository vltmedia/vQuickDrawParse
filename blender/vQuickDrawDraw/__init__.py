

"""
# Contributor(s): Justin Jaro (Justin@VLTMedia.com)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
Import a Grasshopper Point Cloud CSV file formatted as:
TIMESTAMP,ORIGIN_X,ORIGIN_Y,ORIGIN_Z,XAXIS_X,XAXIS_Y,XAXIS_Z,YAXIS_X,YAXIS_Y,YAXIS_Z,STATE
ORIGIN_X,ORIGIN_Y,ORIGIN_Z = Vecator3(x,y,z) Object Position
Can import as a point cloud with attributes for GeoNodes processing, and as an animated Cube per point.
"""
import sys, os
sys.path.append(os.path.dirname(__file__))

# from operators.VLTPipelineImportOp import registerVLTPipelineImportOp, unregisterVLTPipelineImportOp
from api.ops.vQuickDrawDrawOp import registervQuickDrawDrawOp, unregistervQuickDrawDrawOp
from api.panels.vQuickDrawDrawPanel import register as registervQuickDrawDrawPanel, unregister as unregistervQuickDrawDrawPanel

import bpy

bl_info = {
        "name": "vQuickDraw",
        "description": "Process a .ndjson file from Google's Quick Draw dataset into multiple curves",
        "author": "Justin Jaro",
        "version": (1, 0),
        "blender": (2, 80, 0),
        "location": "Tools > vQuickDraw",
        "warning": "", # used for warning icon and text in add-ons panel
        "wiki_url": "http://vltmedia.com",
        "tracker_url": "http://vltmedia.com",
        "support": "COMMUNITY",
        "category": "IO"
        }



def register():
    
    # for class_ in [Folder, Marker, PiplineProjectInfo]:
    registervQuickDrawDrawPanel()
    registervQuickDrawDrawOp()
        


def unregister():
    
    unregistervQuickDrawDrawOp()
    unregistervQuickDrawDrawPanel()

if __name__ == "__main__":
    register()