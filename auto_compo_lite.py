
import bpy
import json
import os

# === PROPRIÉTÉS ===


preset_items = [
    ("no_base.json", "No Compositing", ""),
    ("base_compo.json", "Base Compo", ""),
    ("film_look.json", "Film Look", ""),
    ("soft_glow.json", "Soft Glow", ""),
    ("color_pop.json", "Color Pop", ""),
    ("multi_source_compo.json", "Multi Source Compo", "")
]


bpy.types.Scene.auto_compo_json_path = bpy.props.StringProperty(
    name="JSON Path",
    subtype='FILE_PATH'
)

bpy.types.Scene.auto_compo_preset = bpy.props.EnumProperty(
    name="Preset",
    items=preset_items
)

# === FONCTIONS ===

def export_nodes_to_json(tree, filepath):
    data = {"nodes": [], "links": []}
    for node in tree.nodes:
        node_data = {
            "name": node.name,
            "type": node.bl_idname,
            "location": list(node.location),
            "properties": {}, 
            "label": node.label,
            "width": node.width,
            "height": node.height
        }
        for prop in node.bl_rna.properties:
            if not prop.is_readonly and prop.identifier not in {"location", "name", "label"}:
                try:
                    val = getattr(node, prop.identifier)
                    json.dumps(val) 
                    node_data["properties"][prop.identifier] = val
                except:
                    pass
        data["nodes"].append(node_data)

    for link in tree.links:
        data["links"].append({
            "from_node": link.from_node.name,
            "from_socket": link.from_socket.name,
            "to_node": link.to_node.name,
            "to_socket": link.to_socket.name
        })

    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)

def import_nodes_from_json(tree, filepath):
    with open(filepath, "r") as f:
        data = json.load(f)

    tree.nodes.clear()
    tree.links.clear()
    nodes = {}

    for node_data in data["nodes"]:
        node = tree.nodes.new(type=node_data["type"])
        node.name = node_data["name"]
        node.location = node_data["location"]
        node.label = node_data.get("label", "")
        node.width = node_data.get("width", 140)
        node.height = node_data.get("height", 100)

        for key, val in node_data.get("properties", {}).items():
            try:
                setattr(node, key, val)
            except:
                pass

        nodes[node.name] = node

    for link_data in data["links"]:
        from_node = nodes.get(link_data["from_node"])
        to_node = nodes.get(link_data["to_node"])
        if from_node and to_node:
            from_socket = from_node.outputs.get(link_data["from_socket"])
            to_socket = to_node.inputs.get(link_data["to_socket"])
            if from_socket and to_socket:
                tree.links.new(from_socket, to_socket)

# === OPÉRATEURS ===

class AUTO_COMPO_OT_export_json(bpy.types.Operator):
    bl_idname = "auto_compo.export_json"
    bl_label = "Export Nodes to JSON"
    def execute(self, context):
        path = context.scene.auto_compo_json_path
        tree = context.scene.node_tree
        if not path or not tree:
            self.report({'ERROR'}, "Invalid path or no node tree")
            return {'CANCELLED'}
        export_nodes_to_json(tree, bpy.path.abspath(path))
        return {'FINISHED'}

class AUTO_COMPO_OT_import_json(bpy.types.Operator):
    bl_idname = "auto_compo.import_json"
    bl_label = "Import Nodes from JSON"
    def execute(self, context):
        path = context.scene.auto_compo_json_path
        tree = context.scene.node_tree
        if not path or not os.path.isfile(bpy.path.abspath(path)):
            self.report({'ERROR'}, "File not found")
            return {'CANCELLED'}
        import_nodes_from_json(tree, bpy.path.abspath(path))
        return {'FINISHED'}

class AUTO_COMPO_OT_load_preset(bpy.types.Operator):
    bl_idname = "auto_compo.load_preset"
    bl_label = "Load Selected Preset"
    def execute(self, context):
        scene = context.scene
        tree = scene.node_tree
        if tree is None:
            self.report({'ERROR'}, "No active compositing node tree found.")
            return {'CANCELLED'}
        preset_name = scene.auto_compo_preset
        preset_path = bpy.path.abspath(f"//presets/{preset_name}")
        if not os.path.isfile(preset_path):
            self.report({'ERROR'}, f"Preset file not found: {preset_path}")
            return {'CANCELLED'}
        import_nodes_from_json(tree, preset_path)
        return {'FINISHED'}

class AUTO_COMPO_OT_clear_nodes(bpy.types.Operator):
    bl_idname = "auto_compo.clear_nodes"
    bl_label = "Clear All Nodes"
    def execute(self, context):
        tree = context.scene.node_tree
        if tree:
            tree.nodes.clear()
            tree.links.clear()
            self.report({'INFO'}, "Cleared all nodes")
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "No active node tree")
            return {'CANCELLED'}

# === PANEL ===

class AUTO_COMPO_PT_main_panel(bpy.types.Panel):
    bl_label = "Auto Compo Lite"
    bl_idname = "AUTO_COMPO_PT_main_panel"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Auto Compo Lite'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.prop(scene, "auto_compo_json_path")
        layout.operator("auto_compo.export_json", icon="EXPORT")
        layout.operator("auto_compo.import_json", icon="IMPORT")

        layout.separator()
        layout.label(text="Presets:")
        layout.prop(scene, "auto_compo_preset")
        layout.operator("auto_compo.load_preset", icon="IMPORT")
        
        layout.separator()
        layout.operator("auto_compo.clear_nodes", icon="TRASH")

# === REGISTER ===

classes = [
    AUTO_COMPO_OT_export_json,
    AUTO_COMPO_OT_import_json,
    AUTO_COMPO_OT_load_preset,
    AUTO_COMPO_OT_clear_nodes,
    AUTO_COMPO_PT_main_panel
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.auto_compo_json_path
    del bpy.types.Scene.auto_compo_preset

if __name__ == "__main__":
    register()
