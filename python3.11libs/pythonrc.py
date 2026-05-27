import hou
import re

# =========================================================
# CONFIG
# =========================================================

COLOR_RULES = {
    "asset":  (0.5, 0.5, 0.5),
    "prep":   (0.584, 0.776, 1),
    "sim":    (0.98, 0.275, 0.275),
    "render": (0.145, 0.667, 0.557),
}

# =========================================================
# COLOR LOGIC
# =========================================================

def apply_color_from_name(node):

    # Solo nodos directamente dentro de /obj
    if node.parent().path() != "/obj":
        return

    name = node.name().lower()

    for keyword, rgb in COLOR_RULES.items():

        pattern = rf"(^|_){keyword}(_|$)"

        if re.search(pattern, name):

            node.setColor(hou.Color(rgb))
            return

# =========================================================
# CALLBACKS
# =========================================================

def on_name_changed(node, event_type, **kwargs):
    apply_color_from_name(node)

def install_on_node(node):

    try:
        node.addEventCallback(
            [hou.nodeEventType.NameChanged],
            on_name_changed
        )
    except:
        pass

def on_child_created(event_type, **kwargs):

    child_node = kwargs.get("child_node")

    if child_node:
        install_on_node(child_node)

# =========================================================
# SETUP
# =========================================================

def setup():

    obj = hou.node("/obj")

    # instalar callbacks en nodos existentes
    for node in obj.children():
        install_on_node(node)

    # instalar callbacks en nuevos nodos
    obj.addEventCallback(
        [hou.nodeEventType.ChildCreated],
        on_child_created
    )

hou.ui.addEventLoopCallback(setup)