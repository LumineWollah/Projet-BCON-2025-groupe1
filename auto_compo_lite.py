import bpy

def organize_nodes(tree, nodes):
    x_start = -400
    y_start = 0
    x_gap = 220
    y_gap = -180

    layout = {
        "Render Layers": (x_start, y_start),
        "Glare": (x_start + x_gap, y_start),
        "Ellipse Mask": (x_start + x_gap - 160, y_start + y_gap),  
        "Blur": (x_start + 2 * x_gap, y_start + y_gap),
        "Invert": (x_start + 3 * x_gap, y_start + y_gap),
        "Mix": (x_start + 2 * x_gap, y_start),
        "Color Balance": (x_start + 3 * x_gap, y_start),
        "Composite": (x_start + 4 * x_gap + 240, y_start),          
        "Viewer": (x_start + 4 * x_gap + 240, y_start + y_gap),     
    }

    for node in nodes:
        if node.name in layout:
            node.location = layout[node.name]

class AUTO_COMPO_OT_setup_nodes(bpy.types.Operator):
    bl_idname = "auto_compo.setup_nodes"
    bl_label = "Apply Auto Compo"
    bl_description = "Automatically set up glare, vignette and color correction in compositor"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        scene.use_nodes = True
        tree = scene.node_tree
        tree.nodes.clear()

        # Activation du Backdrop dans le Compositor
        for area in context.screen.areas:
            if area.type == 'NODE_EDITOR':
                for space in area.spaces:
                    if space.type == 'NODE_EDITOR' and space.tree_type == 'CompositorNodeTree':
                        space.show_backdrop = True

        # Création des nodes
        rl = tree.nodes.new(type='CompositorNodeRLayers')
        rl.name = "Render Layers"

        glare = tree.nodes.new(type='CompositorNodeGlare')
        glare.glare_type = 'FOG_GLOW'
        glare.threshold = 0.5
        glare.size = 6
        glare.name = "Glare"

        mask = tree.nodes.new(type='CompositorNodeEllipseMask')
        mask.width = 0.8
        mask.height = 0.8
        mask.name = "Ellipse Mask"

        blur = tree.nodes.new(type='CompositorNodeBlur')
        blur.size_x = 300
        blur.size_y = 300
        blur.use_relative = False
        blur.name = "Blur"

        invert = tree.nodes.new(type='CompositorNodeInvert')
        invert.name = "Invert"

        mix = tree.nodes.new(type='CompositorNodeMixRGB')
        mix.blend_type = 'MULTIPLY'
        mix.inputs[0].default_value = 1.0
        mix.name = "Mix"

        color = tree.nodes.new(type='CompositorNodeColorBalance')
        color.name = "Color Balance"

        comp = tree.nodes.new(type='CompositorNodeComposite')
        comp.name = "Composite"

        viewer = tree.nodes.new(type='CompositorNodeViewer')
        viewer.name = "Viewer"

        # Frame pour le groupe vignette
        frame = tree.nodes.new(type='NodeFrame')
        frame.label = "Vignette Group"
        frame.use_custom_color = True
        frame.color = (0.8, 0.3, 0.1)
        frame.location = (-150, -220)
        frame.width = 380
        frame.height = 280

        # Parentage des nodes dans le frame
        for n in [glare, mask, blur, invert]:
            n.parent = frame

        # Connexions
        links = tree.links
        links.new(rl.outputs['Image'], glare.inputs['Image'])
        links.new(mask.outputs['Mask'], blur.inputs['Image'])
        links.new(blur.outputs['Image'], invert.inputs['Color'])
        links.new(glare.outputs['Image'], mix.inputs[1])
        links.new(invert.outputs['Color'], mix.inputs[2])
        links.new(mix.outputs['Image'], color.inputs['Image'])
        links.new(color.outputs['Image'], comp.inputs['Image'])
        links.new(color.outputs['Image'], viewer.inputs['Image'])

        # Organisation des nodes
        organize_nodes(tree, tree.nodes)

        return {'FINISHED'}


class AUTO_COMPO_PT_main_panel(bpy.types.Panel):
    bl_label = "Auto Compo Lite"
    bl_idname = "AUTO_COMPO_PT_main_panel"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Auto Compo"

    @classmethod
    def poll(cls, context):
        space = context.space_data
        return space.tree_type == 'CompositorNodeTree'

    def draw(self, context):
        layout = self.layout
        layout.label(text="Auto Setup:")
        layout.operator("auto_compo.setup_nodes", icon="NODETREE")


classes = [AUTO_COMPO_OT_setup_nodes, AUTO_COMPO_PT_main_panel]

def register():
    try:
        unregister()
    except:
        pass
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
