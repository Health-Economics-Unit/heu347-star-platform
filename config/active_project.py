# This page contains values for the active project:

ACTIVE_PROJECT = "hse"

#--------------------------------------------------------------------------------------------------
if ACTIVE_PROJECT == "hse":
    from config.hse import *

elif ACTIVE_PROJECT == "mcda":
    from config.mcda import *

elif ACTIVE_PROJECT == "star":
    from config.star import *

else:
    raise ValueError(
        f"Unknown project configuration: {ACTIVE_PROJECT}"
    )