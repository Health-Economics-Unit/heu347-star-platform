# This page contains fixed values for the HSE project:

#--------------------------------------------------------------------------------------------------
project_name = "The Health and Safety Executive's Prioritisation Platform"
#--------------------------------------------------------------------------------------------------
project_subtitle = "Multi-Criteria Decision Analysis (MCDA)"
#--------------------------------------------------------------------------------------------------
project_footername = "The Health and Safety Executive (HSE)"
#--------------------------------------------------------------------------------------------------

pages = [
    "landing",
    "decision",
    "options",
    "criteria",
    "scores",
    "weighting",
    "results"
]
#--------------------------------------------------------------------------------------------------

# decision_types = [
#     "Resource Allocation",
#     "Service Redesign",
#     "Workforce Planning"
# ]
#--------------------------------------------------------------------------------------------------
# default_criteria = [
#     "Clinical Outcomes",
#     "Patient Experience",
#     "Deliverability"
# ]
#--------------------------------------------------------------------------------------------------

default_weights = {
    "Clinical Impact": 35,
    "Cost Saving": 20
}
#--------------------------------------------------------------------------------------------------

heu_palette = {
    "teal":         "#24B1A8",      # best_outcome
    "light blue":   "#59C0E9",      # medium_low
    "blue":         "#4085C4",      # medium
    "dark blue":    "#213B7D",      # medium high
    "light grey":   "#EAEBEB"       # missing
}
#--------------------------------------------------------------------------------------------------

nhs_palette = {
    "nhs_blue":     "#005EB8"
}

#--------------------------------------------------------------------------------------------------