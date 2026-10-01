"""
HEU Strategic Prioritisation Platform
The Socio-Technical Allocation of Resource (STAR)

# This page only contains navigation and application structure

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
        ui.update_navs(
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
        ui.update_navs(
            "main_nav",
            selected="decision"
        )

    @reactive.effect
    @reactive.event(input.go_options)
    def goto_options():

        ui.update_navs(
            "main_nav",
            selected="options"
        )

    @reactive.effect
    @reactive.event(input.go_criteria)
    def goto_criteria():
        ui.update_navs(
            "main_nav",
            selected="criteria"
        )

    @reactive.effect
    @reactive.event(input.go_scores)
    def goto_scores():
        ui.update_navs(
            "main_nav",
            selected="scores"
        )

    @reactive.effect
    @reactive.event(input.go_weighting)
    def goto_weighting():
        ui.update_navs(
            "main_nav",
            selected="weighting"
        )

    @reactive.effect
    @reactive.event(input.go_results)
    def goto_results():
        ui.update_navs(
            "main_nav",
            selected="results"
        )


app = App(app_ui, server)
