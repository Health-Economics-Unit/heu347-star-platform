# This page contains fixed values for the MCDA project like project details, landing page details, color palette, chart_colors, theme_css ::

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
note_text = ("Note: Complete the stages below in sequence, as each stage builds on the information collected in the previous step.")



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


#--------------------------------Project Aesthetics------------------------------------------------------------------
#------------------------Color palette-------------------------------------------------------------------------------

palette = {
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

body {
    background-color: #F3F5F4;                  /* Page background */
}


.hse-heading {                                  /* Headings */
    color: #0D6B5A;
    font-weight: 700;
}

/*--------------------------- hse banner------------------*/
.project-banner {

    background-color: #000000;
    color: white;
    border-radius: 0;
    border: none;
    padding: 50px;
    margin-top: 20px;
    margin-bottom: 30px;
    min-height: 250px;
}

.project-banner h1{
    color: #4F8F88;
    font-weight: 700;
},

.project-banner h2,
.project-banner h3,
.project-banner h4,
.project-banner h5 {
    color: #234B4B;
}

.project-banner-subtitle {

    color: white;
    font-size: 1.25rem;
    font-weight: 600;
}

/*-----------------------------Cards---------------------------*/
.nav-card {                                     

    background-color: #BFD7D3;
    border: 2px solid #C9DEDA;
    border-radius: 20px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.06);
    margin-bottom: 20px;
}

/*-----------------------Card header---------------------------*/

.nav-card .card-header {                        

    background-color: #FFFFFF;
    color: #0D6B5A;
    font-weight: 600;
    border-bottom: 2px solid #C9DEDA;
}

.nav-card:hover {

    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}


/*---------------------Criteria cards-----------------------*/

.criterion-card {                               
    background-color: #FFFFFF;
    border: 2px solid #C9DEDA;
    border-radius: 15px;
    color: #0D6B5A;
    font-weight: 600;
}

.criterion-card:hover {
    background-color: #F3F5F4;
    border-color: #0D6B5A;
}


/*---------------------Navigation Cards---------------------*/

.nav-card {

    background-color: #FFFFFF;
    border: 2px solid #C9DEDA;
    border-radius: 20px;
    color: #0D6B5A;
}

.nav-card:hover {

    background-color: #F3F5F4;
    border-color: #0D6B5A;
}


/*---------------------Primary Buttons---------------------*/

.btn-primary {

    background-color: #0D6B5A;
    border-color: #0D6B5A;
}

.btn-primary:hover {

    background-color: #2A8B77;

    border-color: #2A8B77;
}

"""