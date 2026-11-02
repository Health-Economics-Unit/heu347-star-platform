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
from modules.star_cost import star_cost_page
from modules.results import results_page
from modules.components import page_header, app_banner, app_footer, results_nav_card
from uuid import uuid4
from calculations.weights_calc import normalise_weights
from calculations.mcda_results_calc import calculate_results
from core.themes import light_theme, dark_theme
from config.active_project import *
import json
from pathlib import Path
from datetime import datetime
from reports.pdf_report import generate_pdf_report
from core.charts import create_results_chart, create_efficiency_frontier
from core.validators import (validate_decision, validate_options, validate_criteria)
from calculations.star_results_calc import calculate_total_cost, calculate_star_results, calculate_efficiency_frontier
from shinywidgets import output_widget, render_widget

#------------------------------------------------------------------------------------------------

app_ui = ui.page_fluid(

    ui.div(

        ui.tags.style(
            light_theme + dark_theme + theme_css
        ),

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


            document.addEventListener(
                "click",
                function(event){

                    const loadButton =
                        event.target.closest("#open_load_project");

                    if(!loadButton){
                        return;
                    }

                    event.preventDefault();

                    const fileInput =
                        document.getElementById("load_project");

                    if(fileInput){

                        console.log(
                            "Opening Load Project file picker"
                        );

                        fileInput.click();
                    }
                    else{

                        console.error(
                            "load_project file input not found"
                        );
                    }
                }
            );
        """),

        # Hidden actual file picker
        ui.div(

            ui.input_file(
                "load_project",
                None,
                accept=[".json"],
                multiple=False
            ),

            style="""
                position:absolute;
                left:-10000px;
                top:auto;
                width:1px;
                height:1px;
                overflow:hidden;
            """
        ),

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
            ui.nav_panel("star_cost", star_cost_page),
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

#-------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------
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
#--------------------------landing header theme for load project--------------------------------
# Open project will  only be displayed only on the landing page

    @render.ui
    def header_load_project():

        if input.main_nav() != "landing":
            return ui.div()

        return ui.input_action_button(
            "open_load_project",
            "📂 Load Project",
            class_="btn-outline-primary"
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


#-----Application state declarations-------------------------------------------------------------------------------------

    decision_context = reactive.value({})           #stores everything selected on Decision page
    decision_type_state = reactive.value(None)      #stores currently selected decision type card

    options_list = reactive.value([])               #stores all options added manually on the Options page

    criteria_list = reactive.value([])              #stores criteria added manually on criteria page

    weights_state = reactive.value({})

    costs_state = reactive.value({})

    scores_state = reactive.value({})

#----------- Read the uploaded JSON and restore all reactive states-------------------------------------------

    @reactive.effect
    @reactive.event(input.load_project)
    def load_project():

        uploaded = input.load_project()

        if not uploaded:
            return

        file_path = uploaded[0]["datapath"]

        try:

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as f:

                project_data = json.load(f)

        except Exception as e:

            ui.notification_show(
                f"Unable to load project: {e}",
                type="error",
                duration=5
            )

            return

    #-----Restore decision-------------------------------------

        loaded_decision = project_data.get(
            "decision",
            {}
        )

        decision_context.set(
            loaded_decision
        )

        decision_type_state.set(
            project_data.get(
                "decision_type",
                loaded_decision.get("decision_type")
            )
        )

        ui.update_text(
            "decision_title",
            value=loaded_decision.get(
                "decision_title",
                ""
            )
        )

        ui.update_text_area(
            "decision_description",
            value=loaded_decision.get(
                "decision_description",
                ""
            )
        )

    #----------Restore Options------------------------------

        options_list.set(
            project_data.get(
                "options",
                []
            )
        )

    #----------Restore Criteria------------------------------

        criteria_list.set(
            project_data.get(
                "criteria",
                []
            )
        )

    #----------Restore Weights------------------------------

        weights_state.set(
            project_data.get(
                "weights",
                {}
            )
        )

    #----------Restore Costs------------------------------

        costs_state.set(
            project_data.get(
                "costs",
                {}
            )
        )

    #----------Restore scores------------------------------

        scores_state.set(
            project_data.get(
                "scores",
                {}
            )
        )

    #----------Stay on landing page after loading--------------

        ui.update_navset(
            "main_nav",
            selected="landing"
        )

        ui.notification_show(
            "Project loaded successfully.",
            type="message",
            duration=3
        )

#------ To build project record on every page save (export project)-------------------------------------

    def build_project_record():

        return {
            "decision": decision_context(),
            "decision_type": decision_type_state(),

            "options": options_list(),
            "criteria": criteria_list(),
            "weights": weights_state(),
            "costs": costs_state(),
            "scores": scores_state(),

            "saved_at": datetime.now().strftime(
                "%d/%m/%Y %H:%M:%S")
        }

#----------Download(JSON file) function for every page--------------------------------

    #-----------JSON download------------------

    def generate_project_json():
        return json.dumps(
            build_project_record(),
            indent=4
        )

    def project_filename():
        return (
            f"project_"
            f"{datetime.now():%Y%m%d_%H%M}.json"
        )

    @render.download(
        filename=project_filename,
        media_type="application/json"
    )
    def download_project_decision():
        yield generate_project_json()


    @render.download(
        filename=project_filename,
        media_type="application/json"
    )
    def download_project_options():
        yield generate_project_json()


    @render.download(
        filename=project_filename,
        media_type="application/json"
    )
    def download_project_criteria():
        yield generate_project_json()


    @render.download(
        filename=project_filename,
        media_type="application/json"
    )
    def download_project_weighting():
        yield generate_project_json()


    @render.download(
        filename=project_filename,
        media_type="application/json"
    )
    def download_project_costs():
        yield generate_project_json()


    @render.download(
        filename=project_filename,
        media_type="application/json"
    )
    def download_project_scores():
        yield generate_project_json()

#-------------------------------------------------------------------------------------------------------------
#---------Decision page logic---------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------

    # Decision type selection

    @reactive.effect
    @reactive.event(input.star_mcda)
    def select_star_mcda():
        decision_type_state.set(
            "STAR - MCDA"
        )

    @reactive.effect
    @reactive.event(input.mcda)
    def select_mcda():
        decision_type_state.set(
            "MCDA"
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

#-----logic for STAR-MCDA to display/hide cost button and add star_criteria_note------------------------

    @render.ui
    def cost_criteria_button():
        if decision_type_state() == "STAR - MCDA":
            return ui.div()

        return ui.input_action_button(
            "add_cost",
            "💷 Cost",
            class_="criterion-card"
        )

    @render.ui
    def star_criteria_note():
        if decision_type_state() == "STAR - MCDA":
            return ui.h6(
                ui.strong(
                    "ℹ️ Note: Please do not add cost as a criterion. "
                    "Cost is evaluated separately in the subsequent stage of the analysis."
                ),
                class_="note-text"
            )

        return ui.div()

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

    #-----Prevent duplicate option names------------------------------------------------------------

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

# ------------------Suggested Criteria Cards from active project----------------------------

    def register_default_criterion(criterion):

        button_id = f"add_{criterion['id']}"
        criterion_name = criterion["name"]

        @reactive.effect
        @reactive.event(input[button_id])

        def handle_default_criterion():

            if add_criteria(criterion_name):

                ui.notification_show(
                    f"{criterion_name} added.",
                    type="message",
                    duration=2
                )

    for criterion in default_criteria:

        register_default_criterion(criterion)

#----logic of displaying cost based on star_mcda/mcda decision type--------------------------

    @reactive.effect
    @reactive.event(input.add_cost)
    def add_cost():
        if decision_type_state() == "STAR - MCDA":
            ui.notification_show(
                "Cost should not be included as a criterion for STAR-MCDA. Cost is assessed separately in the Cost stage.",
                type="warning",
                duration=4
            )

            return

        if add_criteria("Cost"):
            ui.notification_show(
                "Cost added.",
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
                ui.strong("Weight"),
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
        weights_state.set(normalised)           #saving the normalised weight

        print("Weighting Summary:")
        for item in normalised.values():
            print(
                f"{item['criterion']}: "
                f"Raw={item['raw_weight']}, "
                f"Normalised={item['normalised_weight']:.1%}"
            )

        ui.notification_show("Weights saved", type="message", duration=3)

    #-----logic to redirect to star_cost page or scores page depending on the decision type-------------------------------

        if decision_type_state() == "STAR - MCDA":

            ui.update_navset(
                "main_nav",
                selected="star_cost"
            )

        else:

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
#--------------------------------------Costs card-----------------------------------------------------------
#------------------------------------------------------------------------------------------------------------

# -------Cost matrix-----------------------------------------------------------------------------------------

    @render.ui
    def star_cost_matrix():

        current_options = options_list()
        saved_costs = costs_state()

        if not current_options:
            return ui.p(
                "Add options before entering costs."
            )

        matrix_rows = [

            # Header row
            ui.div(

                ui.div(
                    ui.strong("Option")
                ),

                ui.div(
                    ui.strong("Cost per person (£)")
                ),

                ui.div(
                    ui.strong("Number of people impacted")
                ),

                ui.div(
                    ui.strong("Total cost (£)")
                ),

                style="""
                    display:grid;
                    grid-template-columns:2fr 1.5fr 1.5fr 1.5fr;
                    gap:10px;
                    font-weight:bold;
                    margin-bottom:10px;
                    padding:8px;
                    border-bottom:2px solid #ddd;
                """
            )
        ]

        for option in current_options:

            option_id = option["id"]

            saved_option = saved_costs.get(
                option_id,
                {}
            )

            saved_cost_per_person = saved_option.get(
                "cost_per_person",
                0
            )

            saved_people_receiving = saved_option.get(
                "people_receiving",
                0
            )

            saved_total_cost = saved_option.get(
                "total_cost",
                0
            )

            matrix_rows.append(

                ui.div(

                    # Option name
                    ui.div(
                        option["name"]
                    ),

                    # Cost per person
                    ui.div(

                        ui.span(
                            "£",
                            style="""
                                font-weight:bold;
                                margin-right:5px;
                            """
                        ),

                        ui.input_text(
                            f"cost_per_person_{option_id}",
                            label=None,
                            value=str(saved_cost_per_person),
                            placeholder = "Enter cost"

                        ),

                        style="""
                            display:flex;
                            align-items:center;
                        """
                    ),

                    # Number of people
                    ui.input_text(
                        f"people_receiving_{option_id}",
                        label=None,
                        value=str(saved_people_receiving),
                        placeholder="Enter number"
                    ),

                    # Total cost
                    ui.input_text(
                        f"total_cost_{option_id}",
                        label=None,
                        value=f"£{saved_total_cost:,.2f}"
                    ),

                    style="""
                        display:grid;
                        grid-template-columns:2fr 1.5fr 1.5fr 1.5fr;
                        gap:10px;
                        align-items:center;
                        margin-bottom:10px;
                        padding:8px;
                        border-bottom:1px solid #ddd;
                    """
                )
            )

        return ui.div(
            *matrix_rows
        )

    #----------validation------------------------------------------

    @reactive.effect
    def validate_cost_inputs():
        for option in options_list():

            option_id = option["id"]

            try:
                cost_value = input[
                    f"cost_per_person_{option_id}"
                ]()

                people_value = input[
                    f"people_receiving_{option_id}"
                ]()

            except KeyError:
                continue

            # ---------- Cost per person ----------

            if cost_value:

                try:
                    cost = float(cost_value)

                    if cost < 0:
                        ui.update_text(
                            f"cost_per_person_{option_id}",
                            value=""
                        )

                        ui.notification_show(
                            "Cost per person cannot be negative.",
                            type="error",
                            duration=3
                        )

                except ValueError:

                    ui.update_text(
                        f"cost_per_person_{option_id}",
                        value=""
                    )

                    ui.notification_show(
                        "Cost per person must contain numbers only.",
                        type="error",
                        duration=3
                    )

            # ---------- Number of people ----------------

            if people_value:

                try:

                    people = int(people_value)

                    if people < 0:
                        ui.update_text(
                            f"people_receiving_{option_id}",
                            value=""
                        )

                        ui.notification_show(
                            "Number of people cannot be negative.",
                            type="error",
                            duration=3
                        )

                except ValueError:

                    ui.update_text(
                        f"people_receiving_{option_id}",
                        value=""
                    )

                    ui.notification_show(
                        "Number of people must be a number.",
                        type="error",
                        duration=3
                    )



# -------Automatically calculate total cost as the user enters values----------------------------------------

    @reactive.effect
    def update_total_costs():

        current_options = options_list()

        for option in current_options:

            option_id = option["id"]

            try:
                cost_per_person = input[
                    f"cost_per_person_{option_id}"
                ]()

                people_receiving = input[
                    f"people_receiving_{option_id}"
                ]()

            except KeyError:
                continue

            total_cost = calculate_total_cost(
                cost_per_person,
                people_receiving
            )

            ui.update_text(
                f"total_cost_{option_id}",
                value=f"£{total_cost:,.2f}"
            )


# -------Build the cost record------------------------------------------------------------------------------

    def build_costs_record():

        costs = {}

        for option in options_list():

            option_id = option["id"]

            try:
                cost_per_person = input[
                    f"cost_per_person_{option_id}"
                ]()

                people_receiving = input[
                    f"people_receiving_{option_id}"
                ]()

            except KeyError:
                cost_per_person = 0
                people_receiving = 0

            cost_per_person = float(
                cost_per_person or 0
            )

            people_receiving = int(
                people_receiving or 0
            )

            total_cost = calculate_total_cost(
                cost_per_person,
                people_receiving
            )

            costs[option_id] = {
                "option": option["name"],
                "cost_per_person": cost_per_person,
                "people_receiving": people_receiving,
                "total_cost": total_cost
            }

        return costs


# -------Validate costs-------------------------------------------------------------------------------------

    def validate_cost_entries(costs):

        errors = []

        if not costs:
            return [
                "No options are available for cost entry."
            ]

        for cost in costs.values():

            if cost["cost_per_person"] <= 0:
                errors.append(
                    f"Enter a cost per person for "
                    f"'{cost['option']}'."
                )

            if cost["people_receiving"] <= 0:
                errors.append(
                    f"Enter the number of people for "
                    f"'{cost['option']}'."
                )

        return errors


# -------Save costs-----------------------------------------------------------------------------------------

    @reactive.effect
    @reactive.event(input.save_costs)
    def save_costs():

        costs = build_costs_record()
        errors = validate_cost_entries(costs)

        if errors:
            ui.notification_show(
                "\n".join(errors),
                type="error",
                duration=4
            )
            return

        costs_state.set(costs)

        print("\nSTAR Cost Summary:")

        for cost in costs.values():
            print(
                f"{cost['option']}: "
                f"£{cost['cost_per_person']:,.2f} per person x "
                f"{cost['people_receiving']:,} people = "
                f"£{cost['total_cost']:,.2f}"
            )

        ui.notification_show(
            "Costs saved.",
            type="message",
            duration=3
        )


# -------Save costs and continue to Scores------------------------------------------------------------------

    @reactive.effect
    @reactive.event(input.save_continue_costs)
    def save_continue_costs():

        costs = build_costs_record()
        errors = validate_cost_entries(costs)

        if errors:
            ui.notification_show(
                "\n".join(errors),
                type="error",
                duration=4
            )
            return

        costs_state.set(costs)

        print("\nSTAR Cost Summary:")

        for cost in costs.values():
            print(
                f"{cost['option']}: "
                f"£{cost['cost_per_person']:,.2f} per person x "
                f"{cost['people_receiving']:,} people = "
                f"£{cost['total_cost']:,.2f}"
            )

        ui.notification_show(
            "Costs saved.",
            type="message",
            duration=2
        )

        ui.update_navset(
            "main_nav",
            selected="scores"
        )


# -------Previous page navigation---------------------------------------------------------------------------

    @reactive.effect
    @reactive.event(input.back_to_weighting_from_cost)
    def back_to_weighting_from_cost():

        ui.update_navset(
            "main_nav",
            selected="weighting"
        )

#-----------------------------------------------------------------------------------------------------------
#--------------------------------------Scores card----------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
    @render.ui
    def scores_matrix():
        current_options = options_list()
        current_criteria = criteria_list()

        # Get previously saved/loaded scores
        saved_scores = scores_state()

        if not current_options or not current_criteria:
            return ui.p(
                "Add options and criteria before scoring."
            )

        matrix_rows = []

        # Header row
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

        # Option rows
        for option in current_options:
            option_id = option["id"]

            matrix_rows.append(

                ui.div(

                    ui.div(
                        option["name"]
                    ),

                    *[
                        # validation to accept the scores value from 0-100 only
                        ui.div(

                            ui.input_numeric(

                                f"score_{option_id}_{criterion['id']}",

                                None,

                                value=(
                                    saved_scores
                                    .get(option_id, {})
                                    .get("criteria_scores", {})
                                    .get(criterion["id"], {})
                                    .get("score", 0)
                                ),

                                min=0,
                                max=100,
                                step=1
                            ),

                            # oninput is while typing the scores in input box
                            oninput="""
                    const input = event.target;

                    if (input.type === 'number' && input.value !== '') {

                        if (Number(input.value) > 100) {
                            input.value = 100;
                            input.dispatchEvent(
                                new Event('change', { bubbles: true })
                            );
                        }

                        if (Number(input.value) < 0) {
                            input.value = 0;
                            input.dispatchEvent(
                                new Event('change', { bubbles: true })
                            );
                        }
                    }
                """
                        )

                        for criterion in current_criteria
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

        return ui.div(
            *matrix_rows
        )

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
        scores_state.set(scores)                #save for use within the project

        print("\n Scores saved:", scores_state())   #test

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

        scores_state.set(scores)                # save for use within the project
        print("Scores saved before continuing:", scores_state())    #test

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
            selected="star_cost"
        )
# -------- Restore/update score inputs from scores_state ---------------------

    @reactive.effect
    def restore_score_inputs():

        saved_scores = scores_state()

        if not saved_scores:
            return

        for option in options_list():

            option_id = option["id"]

            for criterion in criteria_list():

                criterion_id = criterion["id"]

                saved_score = (
                    saved_scores
                    .get(option_id, {})
                    .get("criteria_scores", {})
                    .get(criterion_id, {})
                    .get("score", 0)
                )

                input_id = (
                    f"score_{option_id}_{criterion_id}"
                )

                try:
                    input[input_id]()
                except KeyError:
                    continue

                ui.update_numeric(
                    input_id,
                    value=saved_score
                )

# -----------------------------------------------------------------------------------------------------------
# --------------------------------------Results card----------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------
    def get_results():

        scores = scores_state()

        weights = weights_state()

        if not scores or not weights: return []

        return calculate_results(scores,weights)

#------------How to interpret the results section on Results page-----------

    @render.ui
    def results_interpretation():

        # STAR-MCDA
        if decision_type_state() == "STAR - MCDA":

            return ui.tags.ul(

                ui.tags.li(
                    "Criteria columns display weighted scores "
                    "(normalised weight × score)."
                ),

                ui.tags.li(
                    "Benefit Score is the sum of all weighted criterion "
                    "scores for an intervention."
                ),

                ui.tags.li(
                    "Cost represents the total cost of delivering each "
                    "intervention."
                ),

                ui.tags.li(
                    "VFM Ratio represents the cost per unit of benefit. "
                    "A lower VFM Ratio indicates better value for money."
                ),

                ui.tags.li(
                    "Interventions are ranked by their VFM Ratio, with "
                    "the lowest cost per unit of benefit ranked first."
                )
            )

        # MCDA
        return ui.tags.ul(

            ui.tags.li(
                "Criteria columns display weighted scores "
                "(normalised weight × score)."
            ),

            ui.tags.li(
                "Benefit Score is the sum of all weighted criterion "
                "scores for an option."
            ),

            ui.tags.li(
                "Options are ranked according to their overall Benefit Score."
            ),

            ui.tags.li(
                "Higher Benefit Scores indicate stronger overall "
                "performance against the selected criteria."
            )
        )

#------ Results summary --------------------------------------------------------------------------------------

    @render.ui
    def results_summary():

        results = get_results()

        if not results:

            return ui.p(
                "No results available."
            )

        # STAR-MCDA
        if decision_type_state() == "STAR - MCDA":

            results = calculate_star_results(
                results,
                costs_state()
            )

            top_option = results[0]

            return ui.div(

                ui.h4(
                    ui.strong(
                        "Best Value for Money"
                    )
                ),

                ui.p(
                    top_option["option"]
                ),

                ui.p(
                    f"Benefit Score: "
                    f"{top_option['benefit_score']:.2f}"
                ),

                ui.p(
                    f"Total Cost: "
                    f"£{top_option['cost']:,.2f}"
                ),

                ui.p(
                    f"VFM Ratio: "
                    f"£{top_option['vfm_ratio']:,.2f} "
                    f"per benefit point"
                )
            )

        # MCDA
        top_option = results[0]

        return ui.div(

            ui.h4(
                ui.strong(
                    "Most Preferred Option"
                )
            ),

            ui.p(
                top_option["option"]
            ),

            ui.p(
                f"Benefit Score: "
                f"{top_option['benefit_score']:.2f}"
            )
        )

#------ Decision Matrix on Results page--------------------------------------------------------------------------------------
# ------ Decision Matrix ----------------------------------------------------------------------

    @render.ui
    def decision_matrix():

        results = get_results()

        print("OPTIONS LIST:", options_list())
        print("SCORES STATE:", scores_state())
        print("BASE RESULTS:", results)

        if not results:
            return ui.p(
                "No results available. Complete the Options, Criteria, "
                "Weighting and Scores pages first."
            )

        # Check whether this is STAR-MCDA

        is_star_mcda = (decision_type_state() == "STAR - MCDA")

        # If STAR-MCDA, add Cost and VFM calculations
        if is_star_mcda:
            print("COSTS STATE:", costs_state())
            results = calculate_star_results(results, costs_state())

            print("STAR RESULTS:", results)


        # Get criterion names from the first result-----------

        criteria_names = list(
            results[0]["weighted_scores"].keys()
        )

        # Number of columns
        # Common: Option + criteria + Benefit Score + Rank
        number_of_columns = len(criteria_names) + 3

        # STAR-MCDA adds Cost + VFM Ratio
        if is_star_mcda:
            number_of_columns += 2

        matrix_rows = []

        #-------------Header row---------------
        header_cells = [

            ui.div(
                ui.strong("Option")
            ),

            *[
                ui.div(
                    ui.strong(name)
                )
                for name in criteria_names
            ]
        ]

        #----------STAR-MCDA only-------------

        if is_star_mcda:
            header_cells.append(
                ui.div(ui.strong("Costs"))
            )

        # Common column
        header_cells.append(
            ui.div(
                ui.strong("Benefit Score")
            )
        )

        # STAR-MCDA only
        if is_star_mcda: header_cells.append(
                ui.div(ui.strong("VFM Ratio"))
            )

        # Common column
        header_cells.append(
            ui.div(ui.strong("Rank"))
        )

        matrix_rows.append(

            ui.div(

                *header_cells,

                style=f"""
                        display:grid;
                        grid-template-columns: repeat({number_of_columns}, 1fr);
                        gap:10px;
                        padding:10px;
                        font-weight:bold;
                        border-bottom:2px solid #ddd;
                        margin-bottom:10px;
                    """
            )
        )

        # Data rows---------------------------------

        for result in results:

            row_cells = [

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
                ]
            ]

            # STAR-MCDA only: Cost
            if is_star_mcda:
                row_cells.append(
                    ui.div(f"£{result['cost']:,.2f}")
                )

            # Common: Benefit Score
            row_cells.append(
                ui.div(f"{result['benefit_score']:.2f}")
            )

            # STAR-MCDA only: VFM Ratio
            if is_star_mcda:
                row_cells.append(
                    ui.div(f"{result['vfm_ratio']:.2f}")
                )

            # Common: Rank
            row_cells.append(
                ui.div(str(result["rank"]))
            )

            matrix_rows.append(

                ui.div(

                    *row_cells,

                    style=f"""
                            display:grid;
                            grid-template-columns: repeat({number_of_columns}, 1fr);
                            gap:10px;
                            padding:10px;
                            border-bottom:1px solid #eee;
                        """
                )
            )

        return ui.div(
            *matrix_rows
        )

#-----Visualisation description on Results page--------------------------------
    @render.ui
    def visualisation_description():

        # STAR-MCDA
        if decision_type_state() == "STAR - MCDA":

            return ui.p(
                "Each coloured area represents an intervention. "
                "Interventions are ordered by value for money and plotted "
                "cumulatively by cost and benefit. Interventions with a lower cost per unit "
                "of benefit indicates better value for money."
            )

        # MCDA
        return ui.p(
            "Each coloured segment represents the weighted contribution "
            "of a criterion to the overall benefit score. Larger bars "
            "indicate options with higher total benefit scores."
        )


#--------Chart visualisation---------------------------------------------------

    #Height of the chart on the results page is controlled here
    @render.ui
    def results_chart_container():

        #STAR-MCDA efficiency frontier chart
        if decision_type_state() == "STAR - MCDA":

            return ui.div(
                output_widget("efficiency_frontier_chart"),
                style="height:600px;"
            )

        #MCDA bar chart
        return ui.output_plot("mcda_results_chart",
            height="600px"
        )

# ---------MCDA bar chart -----------------------------------------

    @render.plot
    def mcda_results_chart():

        results = get_results()

        if not results: return None

        return create_results_chart(results, chart_colours)


# -------- STAR-MCDA efficiency frontier ----------------------

    @render_widget
    def efficiency_frontier_chart():

        results = get_results()

        if not results:

            return create_efficiency_frontier(
                [],
                chart_colours
            )

        print(
            "\nBASE RESULTS:",
            [result["option"] for result in results]
        )

        star_results = calculate_star_results(results, costs_state())
        print(
            "\nSTAR RESULTS:",
            [result["option"] for result in star_results]
        )

        frontier_results = calculate_efficiency_frontier(star_results)
        print(
            "\nFRONTIER RESULTS:",
            [result["option"] for result in frontier_results]
        )

        return create_efficiency_frontier(frontier_results, chart_colours)

#--------Navigation---------------------------------------------------------------------

    # Conditional Cost navigation card
    @render.ui
    def results_cost_card():

        if decision_type_state() == "STAR - MCDA":

            return results_nav_card(
                "edit_cost",
                "💷",
                "Cost"
            )

        return None

    # Navigation cards on Results page
    @reactive.effect
    @reactive.event(input.edit_decision)
    def edit_decision():
        ui.update_navset(
            "main_nav",
            selected="decision"
        )

    @reactive.effect
    @reactive.event(input.edit_options)
    def edit_options():
        ui.update_navset(
            "main_nav",
            selected="options"
        )

    @reactive.effect
    @reactive.event(input.edit_criteria)
    def edit_criteria():
        ui.update_navset(
            "main_nav",
            selected="criteria"
        )

    @reactive.effect
    @reactive.event(input.edit_weighting)
    def edit_weighting():
        ui.update_navset(
            "main_nav",
            selected="weighting"
        )

    @reactive.effect
    @reactive.event(input.edit_cost)
    def edit_cost():
        ui.update_navset(
            "main_nav",
            selected="star_cost"
        )

    @reactive.effect
    @reactive.event(input.edit_scores)
    def edit_scores():
        ui.update_navset(
            "main_nav",
            selected="scores"
        )

#--------Download PDF report---------------------------------------------------------------------

    @render.download(
        filename=lambda: (
                f"prioritisation_report_"
                f"{datetime.now():%Y%m%d_%H%M}.pdf"
        ),
        media_type="application/pdf"
    )
    def download_report():
        decision = decision_context()
        decision_type = decision_type_state()
        options = options_list()
        criteria = criteria_list()
        weights = weights_state()
        costs = costs_state()
        scores = scores_state()

        # MCDA results
        results = get_results()

        if not decision:
            ui.notification_show(
                "Complete and save the decision page before downloading the report.",
                type="error",
                duration=3
            )
            return

        if not options:
            ui.notification_show(
                "Add and save at least one option before downloading the report.",
                type="error",
                duration=3
            )
            return

        if not criteria:
            ui.notification_show(
                "Select and save at least one criterion before downloading the report.",
                type="error",
                duration=3
            )
            return

        if not weights:
            ui.notification_show(
                "Save the criterion weights before downloading the report.",
                type="error",
                duration=3
            )
            return

        if not scores:
            ui.notification_show(
                "Save the option scores before downloading the report.",
                type="error",
                duration=3
            )
            return

        if not results:
            ui.notification_show(
                "No calculated results are available for the report.",
                type="error",
                duration=3
            )
            return

        # STAR-MCDA requires saved costs
        if decision_type == "STAR - MCDA":

            if not costs:
                ui.notification_show(
                    "Save the intervention costs before downloading the STAR-MCDA report.",
                    type="error",
                    duration=3
                )
                return

            # Add Cost, VFM Ratio and STAR ranking
            results = calculate_star_results(
                results,
                costs
            )

        ui.notification_show(
            "✅ Generating report....",
            type="message",
            duration=3
        )

        pdf_buffer = generate_pdf_report(
            project_name=project_name,
            project_subtitle=project_subtitle,
            project_footername=project_footername,
            project_logo=project_logo,
            project_colour=palette["primary"],
            chart_colours=chart_colours,
            decision=decision,
            options=options,
            criteria=criteria,
            weights=weights,
            scores=scores,
            results=results,
            project_root=Path(__file__).parent
        )

        pdf_bytes = pdf_buffer.getvalue()

        print(f"PDF size: {len(pdf_bytes)} bytes")

        yield pdf_buffer.getvalue()

#------------------------------------------------------------------------------------------------------------
app = App(app_ui, server, static_assets=Path(__file__).parent / "assets")
