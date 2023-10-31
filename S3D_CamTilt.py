bl_info = {
    "name": "S3D_CamTilt",
    "blender": (3, 60, 0),
    "author": "Silvie3D",
    "version": (1, 2, 1),
    "location": "Output Properties > Format > Orientation",
    "description": "Swap X and Y render resolutions and set portrait or landscape orientations.",
    "category": "Render",
}

import bpy

class SwapRenderResolutionOperator(bpy.types.Operator):
    bl_idname = "render.swap_resolution"
    bl_label = ""
    bl_icon = 'FILE_REFRESH'  # Set the icon to 'FILE_REFRESH'
    bl_options = {'REGISTER', 'UNDO'}
    
    maintain_aspect_ratio: bpy.props.BoolProperty(
        name="Maintain Aspect Ratio",
        default=True,
        description="Maintain the aspect ratio when swapping resolutions."
    )
    
    @classmethod
    def poll(cls, context):
        # Check if X and Y resolutions are not the same to enable the button
        return context.scene.render.resolution_x != context.scene.render.resolution_y
    
    def execute(self, context):
        render = bpy.context.scene.render
        x_resolution = render.resolution_x
        render.resolution_x = render.resolution_y
        render.resolution_y = x_resolution
        if self.maintain_aspect_ratio:
            render.pixel_aspect_x, render.pixel_aspect_y = render.pixel_aspect_y, render.pixel_aspect_x
        return {'FINISHED'}

class SetPortraitResolutionOperator(bpy.types.Operator):
    bl_idname = "render.set_portrait_resolution"
    bl_label = "Portrait"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        # Check if X resolution is greater than Y resolution to enable the button
        return context.scene.render.resolution_x > context.scene.render.resolution_y
    
    def execute(self, context):
        render = bpy.context.scene.render
        x_resolution = render.resolution_x
        render.resolution_x = render.resolution_y
        render.resolution_y = x_resolution
        return {'FINISHED'}

class SetLandscapeResolutionOperator(bpy.types.Operator):
    bl_idname = "render.set_landscape_resolution"
    bl_label = "Landscape"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        # Check if Y resolution is greater than X resolution to enable the button
        return context.scene.render.resolution_y > context.scene.render.resolution_x
    
    def execute(self, context):
        render = bpy.context.scene.render
        x_resolution = render.resolution_x
        render.resolution_x = render.resolution_y
        render.resolution_y = x_resolution
        return {'FINISHED'}

def draw_func(self, context):
    layout = self.layout
    
    # Add a header with "Orientation:"
    layout.label(text="Orientation:")
    
    col = layout.column()
    
    row = col.row(align=True)
    # The "Swap Resolution" button with the emboss effect
    row.operator("render.swap_resolution", icon='FILE_REFRESH')
    
    # Check if X and Y resolutions are not the same
    if context.scene.render.resolution_x != context.scene.render.resolution_y:
        row.operator("render.set_portrait_resolution")
        row.operator("render.set_landscape_resolution")

def register():
    bpy.utils.register_class(SwapRenderResolutionOperator)
    bpy.utils.register_class(SetPortraitResolutionOperator)
    bpy.utils.register_class(SetLandscapeResolutionOperator)
    bpy.types.RENDER_PT_format.append(draw_func)  # Update the panel name here

def unregister():
    bpy.utils.unregister_class(SwapRenderResolutionOperator)
    bpy.utils.unregister_class(SetPortraitResolutionOperator)
    bpy.utils.unregister_class(SetLandscapeResolutionOperator)
    bpy.types.RENDER_PT_format.remove(draw_func)  # Update the panel name here

if __name__ == "__main__":
    register()
