
# This constants page contains fixed values for the below:
# criteria names,
# default weights,
# heu colors,
# page names

#--------------------------------------------------------------------------------------------------
app_name = "Health Economics Unit's Prioritisation Platform"
#--------------------------------------------------------------------------------------------------
app_subtitle = "Socio-Technical Allocation of Resource (STAR)"
#--------------------------------------------------------------------------------------------------
app_footername = "Health Economics Unit"
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

default_criteria = [
    "Clinical Impact",
    "Cost Saving"
]
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