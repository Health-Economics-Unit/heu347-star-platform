# This page contains fixed values for the STAR project:

#--------------------------------------------------------------------------------------------------
project_name = "Health Economics Unit's Prioritisation Platform"
#--------------------------------------------------------------------------------------------------
project_subtitle = "Socio-Technical Allocation of Resource (STAR)"
#--------------------------------------------------------------------------------------------------
project_footername = "Health Economics Unit"
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