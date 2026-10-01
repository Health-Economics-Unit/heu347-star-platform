from shiny import ui
from modules.components import decision_card

decision_page = ui.div(

     ui.h2("🎯 Decision"),
     ui.br(),
     ui.p(
          "Define the decision context before building your prioritisation model. Different types of decisions "
          "require different evidence, criteria, and stakeholder input. Select the decision type that best "
          "reflects your scenario from the options below. If none are suitable, select 'Other'. "
          "The categories are based on common applications of MCDA reported in the literature "
          "(Gongora-Salazar et al., 2023)."
     ),

#-------------------Decision overview---------------------------------------------------------

    ui.card(

        ui.card_header("1. Decision Context"),

        ui.layout_columns(

            ui.input_text_area(
                "decision_title",
                "Decision title",
                rows=6,
                placeholder="Cancer Service Prioritisation 2027/28"
            ),

            ui.input_text_area(
                "decision_description",
                "Decision description/objectives *",
                rows=6,
                placeholder=(
                    "Provide a brief description of the decision "
                    "that needs to be made."
                )
            ),

            col_widths=(3, 9)
        )
    ),


#----------------------Decision type---------------------------------------------------------


    ui.card(
        ui.card_header("2. Decision type"),

        ui.p(
            "Select the option that best describes the decision type. "
            "Only one decision type can be selected."
        ),

        ui.layout_columns(

            decision_card(
                "resource_allocation",
                "💰 Resource Allocation",
                "Prioritise services or interventions within a fixed budget."
            ),

            decision_card(
                "service_redesign",
                "🏥 Service Redesign",
                "Compare alternative service delivery models "
            ),

            decision_card(
                "workforce_planning",
                "👥 Workforce Planning",
                "Prioritise staffing and workforce initiatives."
            ),

            decision_card(
                "technology_adoption",
                "💻 Technology Adoption",
                "Evaluate new digital tools and technologies."
            ),

            decision_card(
                "other_decision",
                "📦 Other",
                "Define a custom decision context.",
            )
        ),

        ui.output_ui("selected_decision_type"),
    ),

#------------------Further Guidance ---------------------------------------------------------

ui.accordion(

    ui.accordion_panel(

        "📘 Further Guidance",

        ui.h6(ui.strong("Define the problem and scope")),

        ui.tags.ul(

            ui.tags.li(
                "What need are you trying to address?"
            ),

            ui.tags.li(
                "What is the policy context and what are the aims of the programme?"
            ),

            ui.tags.li(
                "What outcomes are you hoping to achieve?"
            ),

            ui.tags.li(
                "What is the relevant service, pathway, disease area or budget?"
            ),

            ui.tags.li(
                "Who is the target population?"
            ),
        ),

        ui.h6(ui.strong("Identify key stakeholders")),

        ui.tags.ul(

            ui.tags.li(
                "Who should be involved in the decision-making process?"
            ),

            ui.tags.li(
                "Consider clinicians, patients, managers, analysts, finance teams, local authorities and voluntary sector partners."
            ),

            ui.tags.li(
                "How will stakeholders contribute to the process?"
            ),

            ui.tags.li(
                "Would a stakeholder mapping exercise be helpful?"
            ),
        ),

        ui.h6(ui.strong("Plan implementation and governance")),

        ui.tags.ul(

            ui.tags.li(
                "Who will be responsible for taking the decision forward?"
            ),

            ui.tags.li(
                "Will the decision require formal approval?"
            ),

            ui.tags.li(
                "Is a business case required?"
            )
        )
    ),

    open=False
),

    ui.br(),

#--------------------Save and continue---------------------------------------------------------

    ui.div(
        ui.input_action_button(
            "save_decision",
            "💾 Save decision",
            class_="btn-outline-primary",
        ),

        ui.input_action_button(
            "save_continue_decision",
            "Save & Continue →",
            class_="btn-primary",
        ),

        style="""
            display:flex;
            justify-content:flex-end;
            gap:10px;
            margin-bottom:20px;
        """,
    ),
)