import hou
import re


# CONFIG

# Naming rules associated with automatic node colors
COLOR_RULES = {
    "asset":  (0.5, 0.5, 0.5),
    "prep":   (0.584, 0.776, 1),
    "sim":    (0.98, 0.275, 0.275),
    "render": (0.145, 0.667, 0.557),
}


# COLOR LOGIC

def apply_color_from_name(node):
    """
    Applies a node color based on naming conventions.

    Only nodes directly under /obj are affected.

    Matching rules require the keyword to be isolated
    using underscores or string boundaries:
        asset_
        _asset
        _asset_
    """

    # Restrict color logic to top-level /obj nodes
    if node.parent().path() != "/obj":
        return

    # Normalize node name for case-insensitive matching
    name = node.name().lower()

    # Evaluate all configured naming rules
    for keyword, rgb in COLOR_RULES.items():

        # Match isolated keywords only
        pattern = rf"(^|_){keyword}(_|$)"

        # Apply color when naming rule matches
        if re.search(pattern, name):

            node.setColor(hou.Color(rgb))
            return


# CALLBACKS

def on_name_changed(node, event_type, **kwargs):
    """
    Triggered whenever a node is renamed.
    """

    apply_color_from_name(node)


def install_on_node(node):
    """
    Registers rename callbacks on a single node.
    """

    try:

        # Listen for node rename events
        node.addEventCallback(
            [hou.nodeEventType.NameChanged],
            on_name_changed
        )

    except:
        pass


def on_child_created(event_type, **kwargs):
    """
    Triggered whenever a new node is created under /obj.
    Automatically installs rename callbacks on the new node.
    """

    # Retrieve newly created node from callback payload
    child_node = kwargs.get("child_node")

    if child_node:
        install_on_node(child_node)


# SETUP

def setup():
    """
    Installs automatic rename callbacks for all current
    and future nodes inside /obj.
    """

    # Access top-level object context
    obj = hou.node("/obj")

    # Install callbacks on existing nodes
    for node in obj.children():
        install_on_node(node)

    # Listen for future node creations
    obj.addEventCallback(
        [hou.nodeEventType.ChildCreated],
        on_child_created
    )


# Delay setup execution until Houdini UI is fully initialized
hou.ui.addEventLoopCallback(setup)
