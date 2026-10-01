from shiny import ui

options_page = ui.div(

     ui.h1("📋 Options"),
     ui.br(),
     ui.p("Options should ideally be identified through discussion with key stakeholders during the decision making process. "
          "Define the options, interventions, services, or initiatives that will be assessed within the prioritisation model. "
          "Options should align with the objectives of the decision and be within the scope of the "
          "decision makers to implement or fund. A smaller number of clearly defined options will "
          "usually lead to a more effective decision process."
          ),

#----------------Add option section-----------------------------------------------------------------------
     ui.card(

         ui.card_header("Add Option"),

         ui.input_text(
             "option_name",
             "Option Name"
         ),

         ui.input_action_button(
             "add_option",
             "➕ Add Option",
              class_="btn-outline-primary",
         )
     ),
#----------------Current selected options----------------------------------------------
     ui.card(

         ui.card_header("Current Options"),

         ui.output_ui("options_table")
     ),

#----------------Key considerations----------------------------------------------------

     ui.card(

         ui.card_header("Key considerations"),

         ui.tags.ul(

             ui.tags.li(
                 "Ensure all options align with the objectives of the decision."
             ),

             ui.tags.li(
                 "Focus on options that decision-makers can realistically fund, implement or influence."
             ),

             ui.tags.li(
                 "Keep the number of options manageable to support meaningful discussion and comparison."
             )
         )
     ),

#--------------------Save and continue---------------------------------------------------------

    ui.div(
        ui.input_action_button(
            "save_options",
            "💾 Save options",
            class_="btn-outline-primary",
        ),

        ui.input_action_button(
            "save_continue_options",
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


