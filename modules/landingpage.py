from shiny import ui
from modules.components import nav_card, app_banner
from core.styles import nav_card_style


landing_page = ui.div(

    nav_card_style,                                                 #In core.styles

#------Introduction---------------------------------------------------------------------------------------------------------

    ui.card(
        ui.h5(ui.strong("Introduction")),
        ui.p("This application has been designed to support evidence-based decision making through multiple criteria decision analysis (MCDA)."
             " MCDA provides a structured and transparent approach for evaluating options against multiple criteria, helping stakeholders compare alternatives, understand trade-offs and reach consensus with confidence."
             " At the Health Economics Unit, we are passionate about the ability of MCDA to improve decision making in healthcare.",

             style="""
                text-align:justify;
                #line-height: 1.6;
             """
             ),

#------How to use the application-------------------------------------------------------------------------------------------

        ui.h6(ui.strong("How to use this application")),
        ui.p("The Strategic Prioritisation Platform guides users through the six key stages of Multi-Criteria Decision Analysis (MCDA): Decision, Options, Criteria, Scores, Weighting, and Results. Complete each stage in the below sequence to build a transparent, evidence-based assessment and support robust healthcare decision making."),

            style="""
                text-align:justify;
                #line-height: 1.6;
            """
    ),

#------Placeholder for visual-----------------------------------------------------------------------------------------------

    ui.card(
        ui.h5("Placeholder: Example scenario that will load by default to help the users understand how it works")
    ),
#------Note-----------------------------------------------------------------------------------------------------------------

ui.h6(ui.strong("Note: Complete the stages below in sequence, as each stage builds on the information collected in the previous step.")),
ui.br(),

#------Cards layout---------------------------------------------------------------------------------------------------------

    ui.layout_columns(
        nav_card("go_decision","🎯 Decision", "Define objectives"),
        nav_card("go_options","📋 Options", "Select interventions"),
        nav_card("go_criteria","📌 Criteria", "Choose criteria"),
        nav_card("go_weighting","🎚️ Weighting", "Assign weights"),
        nav_card("go_scores","📝 Scores", "Score options"),
        nav_card("go_results","📊 Results", "Review recommendations")
    ),

#------Placeholder for visual-----------------------------------------------------------------------------------------------

    #ui.card(ui.h5("Placeholder: Another visualisation if we need"))
),