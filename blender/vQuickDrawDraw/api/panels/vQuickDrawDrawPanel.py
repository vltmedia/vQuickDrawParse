
import  os, time
import bpy
from bpy.props import StringProperty, BoolProperty, EnumProperty, FloatProperty, IntProperty

import sys
src = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(src)
from vQuickDrawImage import vQuickDrawImage


class vQuickDrawDrawPropertyGroup(bpy.types.PropertyGroup):
    #NOTE: read documentation about 'props' to see them and their keyword arguments
    #builtin float (variable)property that blender understands

    filepath: bpy.props.StringProperty(
        name="File Path",
        
        default="C:/temp/bee.ndjson",
        maxlen=255,  # Max internal buffer length, longer would be clamped.
        subtype='FILE_PATH'
    )

    
    draw_count: bpy.props.IntProperty(
        name="Draw Count",
        description="How many drawings to draw",
        default=1,
    )
#create a panel (class) by deriving from the bpy Panel, this be the UI
class vQuickDrawDrawPanel(bpy.types.Panel):
    #variable for determining which view this panel will be in
    bl_idname = "PANEL_PT_vquickdrawdrawpanel"
    bl_space_type = 'VIEW_3D'
    #this variable tells us where in that view it will be drawn
    bl_region_type = 'UI'
    #this variable is a label/name that is displayed to the user
    bl_label = 'VQuickDraw: Draw'
    #this context variable tells when it will be displayed, edit mode, object mode etc
    bl_context = 'objectmode'
    #category is esentially the main UI element, the panels inside it are
    #collapsible dropdown menus drawn under a category
    #you can add your own name, or an existing one and it will be drawn accordingly
    bl_category = 'VQuickDraw'
    
    #now we define a draw method, in it we can tell what elements we want to draw
    #in this new space we created, buttons, toggles etc.
    def draw(self, context):
        #shorten the self.layout to just layout for convenience
        layout = self.layout
        #add a button to it, which is called an operator, its a little tricky to do it but...
        #first argument is a string with the operator name to be invoked
        #in example 'bpy.ops.mesh.primitive_cube_add()' is the function we want to invoke
        #so we invoke it by name 'mesh.primitive_cube_add'
        #then the rest are keyword arguments based on documentation
        #NOTE: for custom operations, you need to define and register an operator with
        #custom name, and then call it by that custom name as we did here
        #add a toggle
        layout.prop(context.scene.vQuickDraw_props, 'filepath')
        #add an int slider
        layout.prop(context.scene.vQuickDraw_props, 'draw_count')
        layout.operator('vquickdraw.drawimages', text = 'Draw Images')
        
        #NOTE: for more layout things see the types.UILayout in the documentation
        

    
    
#this function is called on plugin loading(installing), adding class definitions into blender
#to be used, drawed and called
def register():
    #register property group class
    bpy.utils.register_class(vQuickDrawDrawPropertyGroup)
    #this one especially, it adds the property group class to the scene context (instantiates it)
    bpy.types.Scene.vQuickDraw_props = bpy.props.PointerProperty(type=vQuickDrawDrawPropertyGroup)
    #register the classes with the correct function
    bpy.utils.register_class(vQuickDrawDrawPanel)


#same as register but backwards, deleting references
def unregister():
    #delete the custom property pointer
    #NOTE: this is different from its accessor, as that is a read/write only
    #to delete this we have to delete its pointer, just like how we added it
    del bpy.types.Scene.vQuickDraw_props 
    #now we can continue to unregister classes normally
    bpy.utils.unregister_class(vQuickDrawDrawPropertyGroup)
    bpy.utils.unregister_class(vQuickDrawDrawPanel)     

#NOTE: during testing if this addon was installed from a file then that current version
#of that file will be copied over to the blender addons directory
#if you want to see what changes occour you HAVE TO REINSTALL from the new file for it to register
    
#a quick line to autorun the script from the text editor when we hit 'run script'
if __name__ == '__main__':
    register()