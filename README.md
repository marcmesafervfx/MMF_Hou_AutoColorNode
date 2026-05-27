# 🚀 Automatic Node Color By Naming Convention (Houdini Tool)

This tool automatically **assigns colors to Houdini nodes based on their naming convention**. It listens to node creation and renaming events inside the `/obj` context and applies a consistent visual coding system using keywords embedded in node names.


## 📦 What does this tool do?

* Monitors node creation inside `/obj`
* Attaches a callback to detect when a node is renamed
* Checks the node name for specific keywords using underscore-based matching
* Applies a predefined color depending on the detected keyword:
  * `asset` → gray
  * `prep` → light blue
  * `sim` → red
  * `render` → green
* Only triggers when the name changes (not on manual color edits)
* Ensures keywords are detected only when isolated (e.g. `_sim_`, `sim_fx`, `fx_sim_v001`)


## ✨ Features

* Automatic color assignment based on naming rules
* Works only inside `/obj` context
* Safe keyword matching using underscore boundaries
* Supports existing and newly created nodes
* Lightweight event-driven system (no constant polling)


## 💡 Recommended usage

* Ideal for production pipelines with strict naming conventions
* Helps visually organize large networks in `/obj`
* Can be extended with additional naming rules for studio standards


## ⚠️ Notes & limitations

* Only affects nodes inside `/obj`
* Requires Houdini session runtime (callbacks are not saved in the .hip file)
* Does not persist automatically unless loaded via `pythonrc.py` or `456.py`
* If naming conventions are inconsistent, colors will not be applied
