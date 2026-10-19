# This page contains fixed values for the STAR project like project details, landing page details, color palette, chart_colors, theme_css ::

#----------------------Project specific branding-------------------------------------------------------------------------------

project_name = "Health Economics Unit's Prioritisation Platform"
#---------------------------------------------------------------------------------------------------------------------
project_subtitle = "Socio-Technical Allocation of Resource (STAR)"
#---------------------------------------------------------------------------------------------------------------------
project_footername = "Health Economics Unit"
#---------------------------------------------------------------------------------------------------------------------
project_logo = "heu_logo.jpg"


#---------------------------------------------------------------------------------------------------------------------
#------------------------Project specific landing page----------------------------------------------------------------

introduction_title = "Introduction"
#---------------------------------------------------------------------------------------------------------------------
introduction_text = (
            "This application has been designed to support evidence-based decision making through "
            "multiple criteria decision analysis (MCDA). MCDA provides a structured and transparent "
            "approach for evaluating options against multiple criteria, helping stakeholders compare "
            "alternatives, understand trade-offs and reach consensus with confidence. "
            "At the Health Economics Unit, we are passionate about the ability of MCDA to improve "
            "decision making in healthcare."
)
#---------------------------------------------------------------------------------------------------------------------
how_to_title = "How to use this application"
#---------------------------------------------------------------------------------------------------------------------
how_to_text = ("The Strategic Prioritisation Platform guides users through the "
               "six key stages of Multi-Criteria Decision Analysis (MCDA): "
               "Decision, Options, Criteria, Scores, Weighting, and Results. "
               "Complete each stage in the below sequence to build a transparent, "
               "evidence-based assessment and support robust healthcare decision making.")
#--------------------------------------------------------------------------------------------------------------------
example_title = "Placeholder: Example scenario that will load by default to help the users understand how it works"
#--------------------------------------------------------------------------------------------------------------------
note_text = ("Note: Complete the stages below in sequence, as each stage builds on the information collected in the previous step.")


#---------------------------------------------------------------------------------------------------------------------
#-------------------------Project specific pages----------------------------------------------------------------------

# pages = [
#     "landing",
#     "decision",
#     "options",
#     "criteria",
#     "scores",
#     "weighting",
#     "results"
# ]

#---------------------Landing page----------------------------------------------------------------

navigation_cards = [

    {
        "id": "go_decision", "title": "🎯 Decision", "description": "Define objectives"
    },

    {
        "id": "go_options", "title": "📋 Options", "description": "Select interventions"
    },

    {
        "id": "go_criteria", "title": "📌 Criteria", "description": "Choose criteria"
    },

    {
        "id": "go_weighting", "title": "🎚️ Weighting", "description": "Assign weights"
    },

    {
        "id": "go_scores", "title": "📝 Scores", "description": "Score options"
    },

    {
        "id": "go_results", "title": "📊 Results", "description": "Review recommendations"
    }

]


#--------------------------------Project Aesthetics------------------------------------------------------------------
#------------------------Color palette-------------------------------------------------------------------------------

heu_palette = {
    "teal":         "#24B1A8",      # best_outcome
    "light blue":   "#59C0E9",      # medium_low
    "blue":         "#4085C4",      # medium
    "dark blue":    "#213B7D",      # medium high
    "light grey":   "#EAEBEB"       # missing
}

nhs_palette = {
    "nhs_blue":     "#005EB8"
}

#-------------------------Chart colors--------------------------------------------------------------------------------


#-------------------------CSS theme-----------------------------------------------------------------------------------

theme_css = """


"""