# This page contains fixed values for the HSE project like project details, landing page details, color palette, chart_colors, theme_css :

from core.themes import project_theme_css

#---------------------------------------------------------------------------------------------------------------------
#----------------------Project specific branding-------------------------------------------------------------------------------

project_name = "Health Service Executive's Prioritisation Platform"
#--------------------------------------------------------------------------------------------------
project_subtitle = "MCDA - Multi-Criteria Decision Analysis"
#--------------------------------------------------------------------------------------------------
project_footername = "Health Service Executive (HSE)"
#--------------------------------------------------------------------------------------------------
project_logo = "hse_logo_white.png"


#---------------------------------------------------------------------------------------------------------------------
#------------------------Project specific landing page----------------------------------------------------------------

introduction_title = "Introduction"
#---------------------------------------------------------------------------------------------------------------------

introduction_text = (
            "This application is a decision-support tool that uses criteria to compare, score, "
            "and rank health interventions in a way that is transparent and guided by local stakeholders "
            "in order to prioritise interventions that are value-based and appropriate for the context "
            "within which they are implemented."
)
#--------------------------------------------------------------------------------------------------
how_to_title = "How to use this application"
#--------------------------------------------------------------------------------------------------
how_to_text = ("The Strategic Prioritisation Platform guides users through the "
               "six key stages of Multi-Criteria Decision Analysis (MCDA): "
               "Decision, Options, Criteria, Scores, Weighting, and Results. "
               "Complete each stage in the below sequence to build a transparent, "
               "evidence-based assessment and support robust healthcare decision making.")
#--------------------------------------------------------------------------------------------------------------------
example_title = "Placeholder: Example scenario that will load by default to help the users understand how it works"

#--------------------------------------------------------------------------------------------------------------------

note_text = ("ℹ️ Note: Complete the stages below in sequence, as each stage builds on the information "
             "collected in the previous step.")




#---------------------------------------------------------------------------------------------------------------------
#-------------------------Project specific pages----------------------------------------------------------------------

#---------------------Landing page------------------------------------------------------------------------------------

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

palette = {
    "primary": "#005A4F",    #main hse teal - use for banner, navigation active state, primary buttons, cards and charts
    "secondary": "#89B4AE",  #sage green - use for landing page backgrounds, information cards etc
    "accent": "#BFD7D3",     #light teal for borders, hover etc
    "background": "#F3F5F4", #page background, info panels etc
    "border": "#C9DEDA",
    "text": "#234B4B",
    "white": "#FFFFFF"
}

theme_css = project_theme_css(palette)


#-------------------------Chart colors--------------------------------------------------------------------------------

chart_colours = [

    "#2FA6A8",   # Teal
    "#F0A52B",   # Mustard
    "#E47B2C",   # Orange
    "#1F4E99"    # HSE blue
]
