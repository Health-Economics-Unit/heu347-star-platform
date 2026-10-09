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
from core.themes import light_theme, dark_theme
from uuid import uuid4

#------------------------------------------------------------------------------------------------

app_ui = ui.page_fluid(

    ui.div(
        ui.tags.style(light_theme + dark_theme),
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

#------------------------------------------------------------------------------------------------
        page_header(),                                                  #header for all pages
#------------------------------------------------------------------------------------------------
        app_banner(),                                                   #title for all pages
#------------------------------------------------------------------------------------------------
    #navigation cards

        ui.div(
        ui.navset_hidden(
        ui.nav_panel("landing", landing_page),
            ui.nav_panel("decision", decision_page),
            ui.nav_panel("options", options_page),
            ui.nav_panel("criteria", criteria_page),
            ui.nav_panel("scores", scores_page),
            ui.nav_panel("weighting", weighting_page),
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
    @reactive.event(input.go_scores)
    def goto_scores():
        ui.update_navset(
            "main_nav",
            selected="scores"
        )

    @reactive.effect
    @reactive.event(input.go_weighting)
    def goto_weighting():
        ui.update_navset(
            "main_nav",
            selected="weighting"
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

    #criteria_context = reactive.value({})           #stores everything selected on Criteria's page
    criteria_list = reactive.value([])              #stores criteria added manually on criteria page


#-------Validations------------------------------------------------------------------------------------------

    def validate_decision():

        errors = []

        # if not input.decision_title().strip():
        #     errors.append("Decision title is required.")

        if not input.decision_description().strip():
            errors.append("Decision description is required.")

        if decision_type_state() is None:
            errors.append("A decision type must be selected.")

        return errors


    def validate_options():
        errors = []

        if len(options_list()) == 0:
            errors.append(
                "At least one option must be added."
            )

        return errors


    def validate_criteria():
        errors = []

        if len(criteria_list()) == 0:
            errors.append(
                "At least one criteria must be added."
            )

        return errors


#---------Decision page logic--------------------------------------------------------------

    # Decision type selection

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

    # @reactive.effect
    # @reactive.event(input.clinical_decision_making)
    # def select_workforce_planning():
    #     decision_type_state.set(
    #         "Clinical Decision Making"
    #     )

    @reactive.effect
    @reactive.event(input.other_decision)
    def select_other_decision():
        decision_type_state.set(
            "Other"
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

#------------------Helper: build the decision record------------------------------------------

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

        errors = validate_decision()
        if errors:
            ui.notification_show("\n".join(errors), type="error", duration=3)
            return

        decision_context.set(build_decision_record())

        print("Saved decision:", decision_context())        #prints to the terminal

        ui.notification_show("Decision saved",          #popup notification
            type="message",
            duration=3
        )

    # Save Decision and continue to Options page---------------------------------------------------------

    @reactive.effect
    @reactive.event(input.save_continue_decision)
    def save_continue_decision():

        errors = validate_decision()
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

    # -----------Previous Decision page navigation--------------------

    @reactive.effect
    @reactive.event(input.back_to_decision)
    def back_to_decision():
        ui.update_navset(
            "main_nav",
            selected="decision"
        )

    # -----------Previous Options page navigation--------------------

    @reactive.effect
    @reactive.event(input.back_to_options)
    def back_to_option():
        ui.update_navset(
            "main_nav",
            selected="options"
        )
#--------------------------------------Options card----------------------------------------------------------------------
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

        # Prevent duplicate option names-----------------------------------
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

    # Display options------------------------------

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

    # delete button for options----------------------------------------------
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

    # Save Options----------------------------------------------------------------

    @reactive.effect
    @reactive.event(input.save_options)
    def save_options():

        errors = validate_options()

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

        errors = validate_options()

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

#--------------------------------------Criteria card----------------------------------------------------------------------
#-----------Criteria selection----------------------------------------------------------------------------
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
        errors = validate_criteria()

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


    # Save Criteria and continue to Weighting page ----------------------------------

    @reactive.effect
    @reactive.event(input.save_continue_criteria)
    def save_continue_criteria():
        errors = validate_criteria()

        if errors:
            ui.notification_show("\n".join(errors),
                                 type="error",
                                 duration=3
                                 )

            return

        print("Saved criteria:", criteria_list())

        ui.notification_show(
            "Criteria saved",
            type="message",
            duration=2
        )

        ui.update_navset(
            "main_nav",
            selected="weighting"
        )


#------------------------------------------------------------------------------------------------------------
app = App(app_ui, server)
