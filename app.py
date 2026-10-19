"""
HEU Strategic Prioritisation Platform
The Socio-Technical Allocation of Resource (STAR)

# This page contains main application entry point and application orchestration

shiny run --reload app.py - run this in terminal to see the app
http://127.0.0.1:8000/ this is the app link
"""

from shiny import App, ui, render, reactive
from modules.landingpage import landing_page        #landing_page is the variable in modules.landingpage
from modules.decision import decision_page          #likewise for all the pages
from modules.options import options_page
from modules.criteria import criteria_page
from modules.scores import scores_page
from modules.weighting import weighting_page
from modules.results import results_page
from modules.components import page_header,app_banner, app_footer
from uuid import uuid4
from calculations.weights_calc import normalise_weights
from calculations.results_calc import calculate_results
from core.themes import light_theme, dark_theme
from config.active_project import *
from pathlib import Path
from core.charts import create_results_chart
from core.validators import (validate_decision, validate_options, validate_criteria)

#------------------------------------------------------------------------------------------------

app_ui = ui.page_fluid(

    ui.div(
        ui.tags.style(light_theme + dark_theme + theme_css),
        ui.tags.script("""
            Shiny.addCustomMessageHandler(
                "theme_toggle",
                function(mode){
            
                    console.log("Theme received:", mode);

                    if(mode === "dark"){
                        document.body.classList.add("dark-mode");
                    }
                    else{
                        document.body.classList.remove("dark-mode");
                    }
                }
            );
        """),

#-------------------------------------------------------------------------------------------------------------------
        page_header(),                                                  #header for all pages is in components file
#-------------------------------------------------------------------------------------------------------------------
        app_banner(),                                                   #title for projects
#-------------------------------------------------------------------------------------------------------------------
    #navigation cards

        ui.div(
        ui.navset_hidden(
        ui.nav_panel("landing", landing_page),
            ui.nav_panel("decision", decision_page),
            ui.nav_panel("options", options_page),
            ui.nav_panel("criteria", criteria_page),
            ui.nav_panel("weighting", weighting_page),
            ui.nav_panel("scores", scores_page),
            ui.nav_panel("results", results_page),

            id="main_nav"
        ),

        style="flex-grow:1;"
    ),
#------------------------------------------------------------------------------------------------

        app_footer(),                                                   #footer on all pages

#--------layout style of the page----------------------------------------------------------------

        style="""
            min-height:100vh;               /* making the page as the height of the browser window */
            display:flex;                   /* arrange all child elements using Flexbox */
            flex-direction:column;          /* stack everything vertically */
        """

    )

)

#------Application logic function-----------------------------------------------------------------

def server(input, output, session):

#-----Home navigation / landing page--------------------------------------------------------------

    @reactive.effect
    @reactive.event(input.go_home)
    def goto_landing():
        ui.update_navset(
            "main_nav",
            selected="landing"
        )

#-----Theme toggle------------------------------------------------------------------------------

    dark_mode = reactive.value(False)

    @render.ui
    def theme_button():

        if dark_mode():
            return ui.input_action_button(
                "toggle_theme",
                "☀️ Light Mode"
            )

        return ui.input_action_button(
            "toggle_theme",
            "🌙 Dark Mode"
        )


    @reactive.effect
    @reactive.event(input.toggle_theme)
    async def toggle_app_theme():

        dark_mode.set(not dark_mode())

        if dark_mode():
            await session.send_custom_message("theme_toggle", "dark")
            #ui.notification_show("Dark mode enabled")

        else:
            await session.send_custom_message("theme_toggle", "light")
            #ui.notification_show("Light mode enabled")

#-----Navigation cards-------------------------------------------------------------------------

    #actions of nav_cards
    @reactive.effect
    @reactive.event(input.go_decision)
    def goto_decision():
        ui.update_navset(
            "main_nav",
            selected="decision"
        )

    @reactive.effect
    @reactive.event(input.go_options)
    def goto_options():

        ui.update_navset(
            "main_nav",
            selected="options"
        )

    @reactive.effect
    @reactive.event(input.go_criteria)
    def goto_criteria():
        ui.update_navset(
            "main_nav",
            selected="criteria"
        )


    @reactive.effect
    @reactive.event(input.go_weighting)
    def goto_weighting():
        ui.update_navset(
            "main_nav",
            selected="weighting"
        )

    @reactive.effect
    @reactive.event(input.go_scores)
    def goto_scores():
        ui.update_navset(
            "main_nav",
            selected="scores"
        )


    @reactive.effect
    @reactive.event(input.go_results)
    def goto_results():
        ui.update_navset(
            "main_nav",
            selected="results"
        )


#-----Application state & validation-------------------------------------------------------------------------------------

    decision_context = reactive.value({})           #stores everything selected on Decision page
    decision_type_state = reactive.value(None)      #stores currently selected decision type card

    options_list = reactive.value([])               #stores all options added manually on the Options page

    criteria_list = reactive.value([])              #stores criteria added manually on criteria page

    weights_state = reactive.value({})

    scores_state = reactive.value({})

#-------------------------------------------------------------------------------------------------------------
#---------Decision page logic---------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------

    # Decision type selection

    @reactive.effect
    @reactive.event(input.program_prioritisation)
    def select_program_prioritisation():
        decision_type_state.set(
            "Program Prioritisation"
        )

    @reactive.effect
    @reactive.event(input.resource_allocation)
    def select_resource_allocation():
        decision_type_state.set(
            "Resource Allocation"
        )

    @reactive.effect
    @reactive.event(input.priority_setting)
    def select_priority_setting():
        decision_type_state.set(
            "Priority Setting"
        )

    @reactive.effect
    @reactive.event(input.service_configuration)
    def select_service_configuration():
        decision_type_state.set(
            "Service Configuration"
        )

    @reactive.effect
    @reactive.event(input.operational_prioritisation)
    def select_operational_prioritisation():
        decision_type_state.set(
            "Operational Prioritisation"
        )

    #-----------------Display selected decision type-------------------------------------------

    @render.ui
    def selected_decision_type():

        selected_type = decision_type_state()

        if selected_type is None:
            return ui.p(
                "No decision type selected."
            )

        return ui.div(
            ui.strong("✓ Selected: "),
            selected_type,
            style="""
                margin-top:10px;
                padding:10px;
                border:1px solid #24B1A8;
                border-radius:6px;
            """
        )

#------------------captures the decision record-----------------------------------------------

    def build_decision_record():

        return {
            "decision_title": input.decision_title().strip(),
            "decision_description": input.decision_description().strip(),
            "decision_type": decision_type_state()
        }

#-----------------------Save Decision---------------------------------------------------------

    @reactive.effect
    @reactive.event(input.save_decision)
    def save_decision():

        errors = validate_decision(input.decision_description(), decision_type_state())

        if errors:
            ui.notification_show("\n".join(errors), type="error", duration=3)
            return

        decision_context.set(build_decision_record())

        print("Saved decision:", decision_context())        #prints to the terminal

        ui.notification_show("Decision saved",          #popup notification
            type="message",
            duration=3
        )

    # Save Decision and continue to Options page-------------------------------------------------

    @reactive.effect
    @reactive.event(input.save_continue_decision)
    def save_continue_decision():

        errors = validate_decision(input.decision_description(), decision_type_state())

        if errors:
            ui.notification_show("\n".join(errors), type="error", duration=3)
            return

        decision_context.set(
            build_decision_record()
        )

        print("Saved decision:", decision_context())        #prints to the terminal

        ui.notification_show(                               #popup notification
            "Decision saved",
            type="message",
            duration=2
        )

        ui.update_navset(
            "main_nav",
            selected="options"
        )


#--------------------------------------Options card----------------------------------------------------------
#-----------Option type selection----------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------

    @reactive.effect
    @reactive.event(input.add_option)

    def add_option():
        option_name = input.option_name().strip()

        if not option_name:
            ui.notification_show("Option name is required.",
                type="warning",
                duration=3
            )

            return

        current_options = options_list().copy()

        # Prevent duplicate option names------------------------------------------------------------
        existing_names = [option["name"].lower()
            for option in current_options
        ]

        if option_name.lower() in existing_names:
            ui.notification_show("This option has already been added.",
                type="warning",
                duration=3
            )

            return

        current_options.append(
            {
                "id": uuid4().hex,
                "name": option_name
            }
        )

        options_list.set(current_options)

        # Clear the input after adding
        ui.update_text("option_name",value="")

        ui.notification_show("Option added.",
            type="message",
            duration=2
        )

    # Display options-----------------------------------------------------------------------------

    @render.ui
    def options_table():
        current_options = options_list()

        if not current_options:
            return ui.p("No options added yet.")

        return ui.div(
            *[
                ui.div(
                    ui.span(option["name"],
                        style="""
                                font-weight:500;
                            """
                    ),

                    ui.input_action_button(
                        f"delete_option_{option['id']}",
                        "🗑 Delete",
                        class_="btn-outline-danger btn-sm"
                    ),

                    style="""
                            display:flex;
                            justify-content:space-between;
                            align-items:center;
                            margin-bottom:10px;
                            padding:10px;
                            border:1px solid #ddd;
                            border-radius:6px;
                        """
                )

                for option in current_options
            ]
        )

    # delete button for options---------------------------------------------------------

    @reactive.effect
    def delete_option():
        current_options = options_list()

        for option in current_options:

            delete_button_id = (
                f"delete_option_{option['id']}"
            )

            try:
                delete_clicks = input[delete_button_id]()

            except KeyError:
                continue

            if delete_clicks > 0:
                updated_options = [
                    item
                    for item in current_options
                    if item["id"] != option["id"]
                ]

                options_list.set(updated_options)

                ui.notification_show(
                    f"'{option['name']}' removed.",
                    type="message",
                    duration=2
                )

                break

    # Save Options---------------------------------------------------------------------------

    @reactive.effect
    @reactive.event(input.save_options)
    def save_options():

        errors = validate_options(options_list())

        if errors:
            ui.notification_show(
                "\n".join(errors),
                type="error",
                duration=3
            )

            return

        print("Saved options:",options_list())

        ui.notification_show(
            "Options saved",
            type="message",
            duration=3
        )


    # Save Options and continue to Criteria page ---------------------------------------

    @reactive.effect
    @reactive.event(input.save_continue_options)
    def save_continue_options():

        errors = validate_options(options_list())

        if errors:

            ui.notification_show("\n".join(errors),
                type="error",
                duration=3
            )

            return

        print("Saved options:",options_list())

        ui.notification_show(
            "Options saved",
            type="message",
            duration=2
        )

        ui.update_navset(
            "main_nav",
            selected="criteria"
        )

    #-----------Previous page navigation to decision page---------------------------

    @reactive.effect
    @reactive.event(input.back_to_decision)
    def back_to_decision():
        ui.update_navset(
            "main_nav",
            selected="decision"
        )


#--------------------------------------Criteria card---------------------------------------------------------
#-----------Criteria selection-------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------

# Add criterion helper ------------------------------------------------------------------

    def add_criteria(criteria_name):
        criteria_name = criteria_name.strip()

        if not criteria_name:
            ui.notification_show(
                "Criteria name is required.",
                type="warning",
                duration=3
            )

            return False

        current_criteria = criteria_list().copy()

        existing_names = [
            criteria["name"].lower()
            for criteria in current_criteria
        ]

        if criteria_name.lower() in existing_names:
            ui.notification_show(
                f"'{criteria_name}' has already been selected.",
                type="warning",
                duration=3
            )

            return False

        current_criteria.append(
            {
                "id": uuid4().hex,
                "name": criteria_name
            }
        )

        criteria_list.set(current_criteria)

        return True


    #------------------Predefined Criteria Cards-----------------------------------------------

    @reactive.effect
    @reactive.event(input.add_health_benefit)
    def add_health_benefit():
        if add_criteria("Health Benefits"):
            ui.notification_show(
                "Health Benefits added.",
                type="message",
                duration=2
            )


    @reactive.effect
    @reactive.event(input.add_health_inequalities)
    def add_health_inequalities():
        if add_criteria("Health Inequalities"):
            ui.notification_show(
                "Health Inequalities added.",
                type="message",
                duration=2
            )


    @reactive.effect
    @reactive.event(input.add_safety)
    def add_safety():
        if add_criteria("Safety"):
            ui.notification_show(
                "Safety added.",
                type="message",
                duration=2
            )


    @reactive.effect
    @reactive.event(input.add_patient_experience)
    def add_patient_experience():
        if add_criteria("Patient Experience"):
            ui.notification_show(
                "Patient Experience added.",
                type="message",
                duration=2
            )


    @reactive.effect
    @reactive.event(input.add_cost)
    def add_cost():
        if add_criteria("Cost"):
            ui.notification_show(
                "Cost added.",
                type="message",
                duration=2
            )


    @reactive.effect
    @reactive.event(input.add_feasibility)
    def add_feasibility():
        if add_criteria("Feasibility"):
            ui.notification_show(
                "Feasibility added.",
                type="message",
                duration=2
            )

    #-----Add custom criterion------------------------------------------------------------------

    @reactive.effect
    @reactive.event(input.add_custom_criteria)
    def add_custom_criteria():

        criteria_name = input.custom_criteria().strip()

        criteria_added = add_criteria(
            criteria_name
        )

        if not criteria_added:
            return

        # Clear the textbox after adding
        ui.update_text(
            "custom_criteria",
            value=""
        )

        ui.notification_show(
            "Custom criteria added.",
            type="message",
            duration=2
        )

    #----------Display selected criteria-----------------------------------------------------

    @render.ui
    def criteria_table():
        current_criteria = criteria_list()

        if not current_criteria:
            return ui.p(
                "No criteria selected yet."
            )

        return ui.div(

            *[
                ui.div(
                    ui.span(
                        f"✅ {criteria['name']}",
                        style="""
                                font-weight:500;
                            """
                    ),

                    ui.input_action_button(
                        f"delete_criteria_{criteria['id']}",
                        "🗑 Delete",
                        class_="btn-outline-danger btn-sm",
                        title=f"Remove {criteria['name']}"
                    ),

                    style="""
                            display:flex;
                            justify-content:space-between;
                            align-items:center;
                            margin-bottom:10px;
                            padding:10px 12px;
                            border:1px solid #24B1A8;
                            border-radius:8px;
                        """
                )

                for criteria in current_criteria
            ]
        )

#--------------------delete button for criteria-------------------------------------------------------

    @reactive.effect
    def delete_criteria():
        current_criteria = criteria_list()

        for criteria in current_criteria:

            delete_button_id = (
                f"delete_criteria_{criteria['id']}"
            )

            try:
                delete_clicks = input[delete_button_id]()

            except KeyError:
                continue

            if delete_clicks > 0:
                updated_criteria = [
                    item
                    for item in current_criteria
                    if item["id"] != criteria["id"]
                ]

                criteria_list.set(updated_criteria)

                ui.notification_show(
                    f"'{criteria['name']}' removed.",
                    type="message",
                    duration=2
                )

                break


#---------------Save Criteria--------------------------------------------------------------------

    @reactive.effect
    @reactive.event(input.save_criteria)
    def save_criteria():

        errors = validate_criteria(criteria_list())

        if errors:
            ui.notification_show(
                "\n".join(errors),
                type="error",
                duration=3
            )

            return

        print("Saved criteria:", criteria_list())

        ui.notification_show(
            "Criteria saved",
            type="message",
            duration=3
        )


    #--------------Save Criteria and continue to Weighting page ----------------------------------

    @reactive.effect
    @reactive.event(input.save_continue_criteria)
    def save_continue_criteria():

        errors = validate_criteria(criteria_list())

        if errors:
            ui.notification_show("\n".join(errors), type="error", duration=3)

            return

        print("Saved criteria:", criteria_list())

        ui.notification_show("Criteria saved", type="message", duration=2)

        ui.update_navset(
            "main_nav",
            selected="weighting"
        )

    # -----------Previous page navigation to options page---------------------------------------------------

    @reactive.effect
    @reactive.event(input.back_to_options)
    def back_to_option():
        ui.update_navset(
            "main_nav",
            selected="options"
        )


#--------------------------------------Weighting card--------------------------------------------------------
#-----------Weights------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------

    #Generate the controls from criteria_list

    @render.ui
    def weighting_controls():
        current_criteria = criteria_list()
        saved_weights = weights_state()

        if not current_criteria:
            return ui.div(

                ui.p(
                    "No criteria are available. Return to the Criteria "
                    "page and select or add at least one criterion."
                ),

                class_="alert alert-warning"
            )

        return ui.div(
            *[
                ui.card(ui.h5(criterion["name"]),

                    ui.layout_columns(

                        ui.input_slider(
                            f"weight_slider_{criterion['id']}","Weight", min=0, max=100,
                            value=saved_weights.get(criterion["id"],{}).get("raw_weight",0),step=1,ticks=False
                        ),

                        ui.input_numeric(
                            f"weight_number_{criterion['id']}","Enter value",
                            value=saved_weights.get(criterion["id"],{}).get("raw_weight",0),
                            min=0,max=100,step=1),col_widths=(9, 3)
                    ),

                    style="""
                            margin-bottom:12px;
                        """
                )

                for criterion in current_criteria
            ]
        )


#----------------Stores the most recently observed value for each criterion------------------------

    last_weight_values = {}

    @reactive.effect
    def synchronise_weight_controls():
        current_criteria = criteria_list()

        for criterion in current_criteria:

            criterion_id = criterion["id"]

            slider_id = (
                f"weight_slider_{criterion_id}"
            )

            number_id = (
                f"weight_number_{criterion_id}"
            )

            try:
                slider_value = input[slider_id]()
                number_value = input[number_id]()

            except KeyError:
                continue

            if slider_value is None or number_value is None:
                continue

            previous_value = last_weight_values.get(
                criterion_id,
                0
            )

#------------Numeric box changed-------------------------------------------------------------

            if number_value != previous_value:

                corrected_value = max(
                    0,
                    min(100, int(number_value))
                )

                last_weight_values[criterion_id] = (
                    corrected_value
                )

                ui.update_numeric(
                    number_id,
                    value=corrected_value
                )

                ui.update_slider(
                    slider_id,
                    value=corrected_value
                )

#-----------Slider changed------------------------------------------------------------------

            elif slider_value != previous_value:

                corrected_value = max(0,min(100, int(slider_value)))

                last_weight_values[criterion_id] = (corrected_value)

                ui.update_numeric(number_id, value=corrected_value)

#-----------------------------------------------------------------------------------------------

    def build_weights_record():
        weights = {}

        for criterion in criteria_list():

            criterion_id = criterion["id"]

            try:
                weight = input[
                    f"weight_number_{criterion_id}"
                ]()

            except KeyError:
                weight = 0

            if weight is None:
                weight = 0

            weights[criterion_id] = {
                "criterion": criterion["name"],
                "raw_weight": max(
                    0,
                    min(100, int(weight))
                )
            }

        return weights

#------------------Weights summary------------------------------------------------------------------

    @render.ui
    def weighting_summary():
        current_criteria = criteria_list()

        if not current_criteria:
            return ui.p("No criteria selected yet.")

        raw_weights = {}

        for criterion in current_criteria:

            criterion_id = criterion["id"]

            try:
                weight = input[f"weight_number_{criterion_id}"
                ]()

            except KeyError:
                weight = 0

            if weight is None:
                weight = 0

            raw_weights[criterion_id] = {"criterion": criterion["name"],
                "raw_weight": weight
            }

        total_weight = sum(item["raw_weight"]
            for item in raw_weights.values()
        )

        if total_weight == 0:
            return ui.p("Adjust the weights to see the summary."
            )

        return ui.div(

            ui.div(

                ui.strong("Criterion"),
                ui.strong("Swing Weight"),
                ui.strong("Normalised Weight"),

                style="""
                        display:grid;
                        grid-template-columns: 2fr 1fr 1fr;
                        font-weight:bold;
                        margin-bottom:10px;
                    """
            ),

            *[

                ui.div(

                    ui.span(
                        item["criterion"]
                    ),

                    ui.span(
                        str(item["raw_weight"])
                    ),

                    ui.span(
                        f"{item['raw_weight'] / total_weight:.1%}"
                    ),

                    style="""
                            display:grid;
                            grid-template-columns: 2fr 1fr 1fr;
                            padding:8px 0;
                            border-bottom:1px solid #eee;
                        """
                )

                for item in raw_weights.values()

            ],

            ui.hr(),

            ui.div(

                ui.strong("Total"),

                ui.strong(
                    str(total_weight)
                ),

                ui.strong("100%"),

                style="""
                        display:grid;
                        grid-template-columns: 2fr 1fr 1fr;
                    """
            )
        )

#-----------------Save Weights---------------------------------------------------------------------

    @reactive.effect
    @reactive.event(input.save_weights)
    def save_weights():
        weights = {}

        for criterion in criteria_list():

            criterion_id = criterion["id"]

            weight = input[f"weight_number_{criterion_id}"
            ]()

            if weight is None:
                weight = 0

            weights[criterion_id] = {

                "criterion": criterion["name"],

                "raw_weight": max(0,min(100, int(weight))
                )
            }

        normalised = normalise_weights(weights)
        weights_state.set(normalised)

        print("Weighting Summary:")
        for item in normalised.values():
            print(
                f"{item['criterion']}: "
                f"Raw={item['raw_weight']}, "
                f"Normalised={item['normalised_weight']:.1%}"
            )


        ui.notification_show("Weights saved", type="message", duration=3)

#-----------------Save weights and continue---------------------------------------------------------------------

    @reactive.effect
    @reactive.event(input.save_continue_weights)
    def save_continue_weights():
        weights = {}

        for criterion in criteria_list():

            criterion_id = criterion["id"]

            weight = input[f"weight_number_{criterion_id}"
            ]()

            if weight is None:
                weight = 0

            weights[criterion_id] = {

                "criterion": criterion["name"],

                "raw_weight": max(0,min(100, int(weight))
                )
            }

        normalised = normalise_weights(weights)
        weights_state.set(normalised)       #saving the normalised weight

        print("Weighting Summary:")
        for item in normalised.values():
            print(
                f"{item['criterion']}: "
                f"Raw={item['raw_weight']}, "
                f"Normalised={item['normalised_weight']:.1%}"
            )

        ui.notification_show("Weights saved", type="message", duration=3)


        ui.update_navset(
            "main_nav",
            selected="scores"
        )

#-----------Previous page navigation to criteria page-------------------------------------------------------

    @reactive.effect
    @reactive.event(input.back_to_criteria)
    def back_to_criteria():
        ui.update_navset(
            "main_nav",
            selected="criteria"
        )

#-----------------------------------------------------------------------------------------------------------
#--------------------------------------Scores card----------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
    @render.ui
    def scores_matrix():

        current_options = options_list()
        current_criteria = criteria_list()

        if not current_options or not current_criteria:

            return ui.p(
                "Add options and criteria before scoring."
            )

        matrix_rows = []

        # Header row-------------------------------------------
        matrix_rows.append(

            ui.div(

                ui.div(
                    ui.strong("Option")
                ),

                *[
                    ui.div(
                        ui.strong(
                            criterion["name"]
                        )
                    )

                    for criterion in current_criteria
                ],

                style="""
                    display:grid;
                    grid-template-columns:repeat(
                        %s,1fr
                    );
                    gap:10px;
                    font-weight:bold;
                    margin-bottom:10px;
                """ % (len(current_criteria) + 1)
            )
        )

        # Option rows-------------------------------------------
        for option in current_options:

            matrix_rows.append(

                ui.div(

                    ui.div(
                        option["name"]
                    ),

                    *[

                        ui.input_numeric(

                            f"score_"
                            f"{option['id']}_"
                            f"{criterion['id']}",

                            None,

                            value=0,

                            min=0,

                            max=100,

                            step=1

                        )

                        for criterion
                        in current_criteria

                    ],

                    style="""
                        display:grid;
                        grid-template-columns:repeat(
                            %s,1fr
                        );
                        gap:10px;
                        margin-bottom:10px;
                    """ % (len(current_criteria) + 1)
                )
            )

        return ui.div(*matrix_rows)

#-----------Collect scores from the matrix-------------------------------------------------------------------

    def build_scores_record():

        scores = {}

        for option in options_list():

            option_id = option["id"]

            scores[option_id] = {
                "option": option["name"],
                "criteria_scores": {}
            }

            for criterion in criteria_list():
                criterion_id = criterion["id"]

                try:
                    score = input[
                        f"score_{option_id}_{criterion_id}"
                    ]()

                except KeyError:

                    score = 0

                if score is None: score = 0

                scores[option_id][
                    "criteria_scores"
                ][criterion_id] = {

                    "criterion": criterion["name"],

                    "score": max(
                        0,
                        min(100, int(score))
                    )
                }

        return scores

#-----------Save scores-------------------------------------------------------------------------------------

    @reactive.effect
    @reactive.event(input.save_scores)

    def save_scores():
        scores = build_scores_record()

        scores_state.set(scores)

        print("\nScores Summary:")

        for option in scores.values():

            print(
                f"\n{option['option']}"
            )

            for item in option[
                "criteria_scores"
            ].values():
                print(
                    f"{item['criterion']}: "
                    f"{item['score']}"
                )

        ui.notification_show(
            "Scores saved",
            type="message",
            duration=3
        )

#-----------Save scores and continue------------------------------------------------------------------------

    @reactive.effect
    @reactive.event(input.save_continue_scores)
    def save_continue_scores():

        scores = build_scores_record()

        scores_state.set(scores)

        ui.notification_show(
            "Scores saved",
            type="message",
            duration=2
        )

        ui.update_navset(
            "main_nav",
            selected="results"
        )

#-----------Previous page navigation to weighting page-------------------------------------------------------

    @reactive.effect
    @reactive.event(input.back_to_weighting)
    def back_to_weights():
        ui.update_navset(
            "main_nav",
            selected="weighting"
        )


# -----------------------------------------------------------------------------------------------------------
# --------------------------------------Results card----------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------
    def get_results():

        scores = scores_state()

        weights = weights_state()

        if not scores or not weights: return []

        return calculate_results(scores,weights)

#------ Results summary --------------------------------------------------------------------------------------

    @render.ui
    def results_summary():

        results = get_results()

        if not results:

            return ui.p(
                "No results available."
            )

        top_option = results[0]

        return ui.div(

            ui.h4(ui.strong("Most Preferred Option")),

            ui.p(
                top_option["option"]
            ),

            ui.p(
                f"Benefit Score: "
                f"{top_option['benefit_score']}"
            ),

            ui.p(
                f"Rank: "
                f"{top_option['rank']}"
            )
        )

#------ Decision Matrix --------------------------------------------------------------------------------------

    @render.ui
    def decision_matrix():

        results = get_results()

        if not results:

            return ui.p(
                "No results available. Complete the Options, Criteria, "
                "Weighting and Scores pages first."
            )

        # Get criterion names from the first result
        criteria_names = list(
            results[0]["weighted_scores"].keys()
        )

        matrix_rows = []

        # Header row
        matrix_rows.append(

            ui.div(

                ui.div(ui.strong("Option")),

                *[
                    ui.div(
                        ui.strong(name)
                    )
                    for name in criteria_names
                ],

                ui.div(
                    ui.strong("Benefit Score")
                ),

                ui.div(
                    ui.strong("Rank")
                ),

                style=f"""
                    display:grid;
                    grid-template-columns:
                        repeat({len(criteria_names) + 3}, 1fr);
                    gap:10px;
                    padding:10px;
                    font-weight:bold;
                    border-bottom:2px solid #ddd;
                    margin-bottom:10px;
                """
            )
        )

        # Data rows
        for result in results:

            matrix_rows.append(

                ui.div(

                    ui.div(
                        result["option"]
                    ),

                    *[
                        ui.div(
                            f"{score:.2f}"
                        )

                        for score in result[
                            "weighted_scores"
                        ].values()
                    ],

                    ui.div(
                        f"{result['benefit_score']:.2f}"
                    ),

                    ui.div(
                        str(result["rank"])
                    ),

                    style=f"""
                        display:grid;
                        grid-template-columns:
                            repeat({len(criteria_names) + 3}, 1fr);
                        gap:10px;
                        padding:10px;
                        border-bottom:1px solid #eee;
                    """
                )
            )

        return ui.div(

            *matrix_rows

        )

#--------Chart visualisation---------------------------------------------------------------------

    @render.plot
    def results_chart():

        results = get_results()

        print(results)

        return create_results_chart(
            results,
            chart_colours
        )

#------------------------------------------------------------------------------------------------------------
app = App(app_ui, server, static_assets=Path(__file__).parent / "assets")
