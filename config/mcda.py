# This page contains fixed values for the MCDA project like project details, landing page details,
# color palette, chart_colors, theme_css :

from core.themes import project_theme_css

#----------------------Project specific branding-------------------------------------------------------------------------------

project_name = "Health Economics Unit's Prioritisation Platform"
#---------------------------------------------------------------------------------------------------------------------
project_subtitle = "Multi-Criteria Decision Analysis (MCDA)"
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

#---------------------------------------------------------------------------------------------------------------------
example_title = "Placeholder: Example scenario that will load by default to help the users understand how it works"
#--------------------------------------------------------------------------------------------------------------------
note_text = ("ℹ️ Note: Complete the stages below in sequence, as each stage builds on the information collected in the previous step.")


#---------------------------------------------------------------------------------------------------------------------
#-------------------------Project specific pages----------------------------------------------------------------------

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

#---------------------Project specific criteria ------------------------------------------------------------------------------------

default_criteria = [
    {
        "id": "health_benefits",
        "name": "Health Benefits",
        "icon": "❤️"
    },
    {
        "id": "health_inequalities",
        "name": "Impact on Health Inequalities",
        "icon": "⚖️"
    },
    {
        "id": "safety",
        "name": "Safety",
        "icon": "🛡️"
    },
    {
        "id": "patient_experience",
        "name": "Patient Experience",
        "icon": "😊"
    }

]

#--------------------------------Project Aesthetics------------------------------------------------------------------
#------------------------Color palette-------------------------------------------------------------------------------

palette = {
    "primary":      "#213B7D",          #main - use for banner, navigation active state, primary buttons, cards and charts
    "secondary":    "#4085C4",          #use for landing page backgrounds, information cards etc
    "accent":       "#59C0E9",          #for borders, hover etc
    "background":   "#F7FAFC",          #page background, info panels etc
    "border":       "#D6E3F0",
    "text":         "#234B4B",          #1F2937   234B4B
    "white":        "#FFFFFF"
}

theme_css = project_theme_css(palette)


#-------------------------Chart colors--------------------------------------------------------------------------------

chart_colours = [

    "#24B1A8",   # Best outcome
    "#59C0E9",   # Medium-low
    "#4085C4",   # Medium
    "#213B7D",   # Medium-high
    "#EAEBEB"    # Missing
]
