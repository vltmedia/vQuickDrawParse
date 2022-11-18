

import  os, time
import bpy
from bpy.props import StringProperty, BoolProperty, EnumProperty, FloatProperty, IntProperty

import sys
src = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(src)
from vQuickDrawImage import vQuickDrawImage

#in order to make a button do custom behavior we need to register and make an operator, a basic
#custom operator that does not take any property and just runs is easily made like so        
class vQuickDrawDrawImagesOperator(bpy.types.Operator):
    #the id variable by which we can invoke the operator in blender
    #usually its good practice to have SOMETHING.other_thing as style so we can group
    #many id's together by SOMETHING and we have less chance of overriding existing op's
    bl_idname = 'vquickdraw.drawimages'
    #this is the label that essentially is the text displayed on the button
    bl_label = 'Draw Images'
    #these are the options for the operator, this one makes it not appear
    #in the search bar and only accessible by script, useful
    #NOTE: it's a list of strings in {} braces, see blender documentation on types.operator
    bl_options = {'REGISTER'}
    #this is needed to check if the operator can be executed/invoked
    #in the current context, useful for some but not for this example    
    # @classmethod
    # def poll(cls, context):
    #     #check the context here
    #     return context.object is not None
    #this is the cream of the entire operator class, this one's the function that gets
    #executed when the button is pressed
    def execute(self, context):
        #just do the logic here
        filepath = context.scene.vQuickDraw_props.filepath
        count = context.scene.vQuickDraw_props.draw_count
        vQuickDrawImage_ = vQuickDrawImage(filepath, count)
        points = vQuickDrawImage_.getVertices(0)
        v = 0
        vQuickDrawImage_.drawBlenderCurves(count, os.path.basename(os.path.splitext(filepath)[0]))
        #this is a report, it pops up in the area defined in the word
        #in curly braces {} which is the first argument, second is the actual displayed text
        self.report({'INFO'}, "Images have been drawn!")
        #return value tells blender wether the operation finished sueccessfully
        #needs to be in curly braces also {}
        return {'FINISHED'}
    
    

# Register and add to the "file selector" menu (required to use F3 search "Text Import Operator" for quick access).
def registervQuickDrawDrawOp():
    
    bpy.utils.register_class(vQuickDrawDrawImagesOperator)


def unregistervQuickDrawDrawOp():
    bpy.utils.unregister_class(vQuickDrawDrawImagesOperator)


