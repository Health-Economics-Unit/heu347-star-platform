# This page contains values for the active project:

active_project = "mcda"

#--------------------------------------------------------------------------------------------------
if active_project == "hse":
    from config.hse import *

elif active_project == "mcda":
    from config.mcda import *

elif active_project == "star":
    from config.star import *

else:
    raise ValueError(
        f"Unknown project configuration: {active_project}"
    )