import bpy
import requests

# Server URL
SERVER_URL = "http://127.0.0.1:5000"

# UI Panel
class DCCPluginPanel(bpy.types.Panel):
    bl_label = "DCC Plugin"
    bl_idname = "OBJECT_PT_dcc_plugin"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "DCC Plugin"

    def draw(self, context):
        layout = self.layout
        obj = context.object

        # Object Selection
        layout.prop(context.scene, "dcc_plugin_object", text="Object")

        # Transform Controls
        if obj:
            layout.prop(obj, "location", text="Position")
            layout.prop(obj, "rotation_euler", text="Rotation")
            layout.prop(obj, "scale", text="Scale")

        # Endpoint Dropdown
        layout.prop(context.scene, "dcc_plugin_endpoint", text="Endpoint")

        # Submit Button
        layout.operator("dcc_plugin.submit", text="Submit")

# Submit Operator
class DCCPluginSubmit(bpy.types.Operator):
    bl_idname = "dcc_plugin.submit"
    bl_label = "Submit Data"

    def execute(self, context):
        obj = context.scene.dcc_plugin_object
        endpoint = context.scene.dcc_plugin_endpoint

        if obj:
            # Prepare transform data
            data = {
                "position": list(obj.location),
                "rotation": list(obj.rotation_euler),
                "scale": list(obj.scale)
            }

            # Send data to server
            try:
                response = requests.post(f"{SERVER_URL}/{endpoint}", json=data)
                if response.status_code == 200:
                    print("Data sent successfully!")
                else:
                    print(f"Error: {response.status_code}")
            except Exception as e:
                print(f"Failed to send data: {e}")
        else:
            print("No object selected.")

        return {'FINISHED'}

# Register Classes
def register():
    bpy.utils.register_class(DCCPluginPanel)
    bpy.utils.register_class(DCCPluginSubmit)
    bpy.types.Scene.dcc_plugin_object = bpy.props.PointerProperty(type=bpy.types.Object)
    bpy.types.Scene.dcc_plugin_endpoint = bpy.props.EnumProperty(
        items=[
            ("transform", "Transform", "Send all transforms"),
            ("translation", "Translation", "Send only position"),
            ("rotation", "Rotation", "Send only rotation"),
            ("scale", "Scale", "Send only scale")
        ],
        name="Endpoint"
    )

def unregister():
    bpy.utils.unregister_class(DCCPluginPanel)
    bpy.utils.unregister_class(DCCPluginSubmit)
    del bpy.types.Scene.dcc_plugin_object
    del bpy.types.Scene.dcc_plugin_endpoint

if __name__ == "__main__":
    register()