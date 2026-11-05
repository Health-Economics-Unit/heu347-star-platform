# HEU Strategic Prioritisation Platform

## Overview

The HEU Strategic Prioritisation Platform is an application designed by the Health Economics Unit (HEU) to support health economics prioritisation, 
Socio-Technical Allocation of Resources (STAR) analysis, and structured decision-making within healthcare settings.

The platform enables decision-makers to:

- Define the decision context, objectives, and population affected
- Identify and compare competing options/interventions
- Define evaluation criteria
- Assign relative importance to criteria through weighting
- Score options against the selected criteria
- Apply Multi-Criteria Decision Analysis (MCDA)
- Perform STAR-MCDA prioritisation incorporating costs and population size
- Compare options based on benefit and value for money
- Visualise STAR-MCDA results using an efficiency frontier
- Generate a PDF report summarising the analysis
- Export project data and reload it in a later session
- Support transparent and evidence-based resource allocation decisions

---

## Current Development Status

The application is currently under active development.

The application currently supports two decision-analysis approaches:

1. **MCDA**
2. **STAR-MCDA**

Additional functionality, validation, reporting, deployment configuration, and user-interface improvements may continue to be added.

Before making changes, check the latest Git branch and commit history to understand recent development.

---

## Technology Stack

The application currently uses:

- Python
- Shiny for Python
- ShinyWidgets
- Plotly
- Pandas
- ReportLab
- HTML/CSS
- JSON
- Git/GitHub

---

## Repository Structure

```text
app.py                       Main application entry point and application orchestration

config/
    active_project.py        Selects/imports the active project configuration
    hse.py                   HSE project configuration and branding
    mcda.py                  MCDA project configuration and branding
    star.py                  STAR project configuration and branding

modules/
    landingpage.py           Landing/home page
    decision.py              Decision context and decision type UI
    options.py               Options/interventions UI
    criteria.py              Criteria selection UI
    weighting.py             Criteria weighting UI
    star_cost.py             STAR-MCDA cost and population UI
    scores.py                Option/criterion scoring UI
    results.py               Results page UI
    components.py            Reusable UI components

calculations/
    weights_calc.py          Weight normalisation
    mcda_results_calc.py     MCDA calculations and ranking
    star_results_calc.py     STAR-MCDA cost, benefit, VFM and efficiency frontier calculations

core/
    themes.py                Shared application styling/themes
    charts.py                MCDA and STAR-MCDA visualisation charts
    validators.py            Input validation functions for decision, options and criteria UI pages

reports/
    pdf_report.py            PDF report generation

assets/
    Logos and other static application assets
```

---

## Application Workflow

The main application workflow is:

```text
Landing page
   ↓
Decision
   ↓
Options
   ↓
Criteria
   ↓
Weighting
   ↓
Cost (STAR-MCDA only)
   ↓
Scores
   ↓
Results
```

The selected decision type controls whether the user follows the standard MCDA workflow or the STAR-MCDA workflow.

### MCDA

```text
Decision
→ Options
→ Criteria
→ Weighting
→ Scores
→ Results
```

### STAR-MCDA

```text
Decision
→ Options
→ Criteria
→ Weighting
→ Cost
→ Scores
→ Results
```

---

## Running the Application Locally

### 1. Clone the repository

```bash
git clone <repository-url>
cd <repository-folder>
```

### 2. Create/activate the appropriate Python environment

Install the dependencies required by the application.

If using `uv`, activate/use the project environment as appropriate.

### 3. Run the application

From the project root:

```bash
shiny run --reload app.py
```

The development application is normally available at:

```text
http://127.0.0.1:8000/
```

The `--reload` option automatically reloads the application when code changes are detected during development.

---

## Application State

The main application state is managed in `app.py` using Shiny reactive values.

The principal state objects are:

```python
decision_context
decision_type_state
options_list
criteria_list
weights_state
costs_state
scores_state
```

These hold the information entered by the user during the active application session.

### Important

Application session state should not be considered permanent storage.

If the browser session closes, the application restarts, or the hosting session ends, in-session data may be lost.

Users should use **Export Project** to retain their work for later use.

---

## Project Export and Load

The application provides an **Export Project** function that downloads the current project information as a JSON file.

The exported project contains:

```text
Decision
Decision type
Options
Criteria
Weights
Costs
Scores
Saved timestamp
```

Project data is generated through:

```python
build_project_record() in `app.py`.
```

A previously exported JSON file can be restored using **Load Project** from the application header.

The load process restores the relevant reactive application states so the user can continue working on the project.

### User guidance

The application displays the following guidance:

> Your work is retained while your session remains active. To keep your progress, use Export Project to download a copy of your project. When you return, use Load Project to upload the file and continue where you left off.

---

## MCDA Method

MCDA evaluates options against multiple criteria.

Each criterion has:

- A raw weight
- A normalised weight
- A score assigned to each option

### Weight normalisation

Criterion weights are normalised so that their relative contributions sum to 100%.

### Weighted criterion score

For each option:

```text
Weighted Score = Criterion Score × Normalised Criterion Weight
```

### Benefit Score

The overall Benefit Score is calculated from the weighted criterion scores:

```text
Benefit Score = Sum of Weighted Criterion Scores
```

A higher Benefit Score represents stronger overall performance against the selected criteria.

For standard MCDA, options are ranked according to their Benefit Score.

Calculation logic is maintained primarily in:

```text
calculations/weights_calc.py
calculations/mcda_results_calc.py
```

---

## STAR-MCDA Method

STAR-MCDA extends the MCDA calculation by incorporating costs and the number of people receiving each intervention.

The STAR Cost stage collects:

- Cost per person
- Number of people receiving the intervention
- Total cost

### Total Cost

```text
Total Cost = Cost per Person × Number of People
```

### Benefit Score

The Benefit Score is calculated using the weighted MCDA criteria scores.

```text
Benefit Score = Sum of Weighted Criterion Scores
```

### Total Benefit

For STAR-MCDA, the Benefit Score is scaled by the number of people receiving the intervention.

```text
Total Benefit = Benefit Score × Number of People
```

This allows the STAR-MCDA analysis to account for the scale of the population expected to benefit from an intervention.

### Value for Money Ratio

The Value for Money ratio represents the cost per unit of total benefit.

```text
VFM Ratio = Total Cost / Total Benefit
```

A **lower VFM Ratio indicates better value for money**.

Interventions are ranked according to their VFM Ratio, with lower cost per unit of benefit ranked more favourably.

STAR-MCDA logic is primarily maintained in:

```text
calculations/star_results_calc.py
```

---

## Efficiency Frontier

STAR-MCDA results are visualised using an efficiency frontier.

Interventions are ordered by value for money and plotted cumulatively according to:

- Total Cost
- Total Benefit

The visualisation is intended to help users understand the relationship between additional expenditure and additional benefit across interventions.

The calculation logic is maintained in:

```text
calculations/star_results_calc.py
```

The visualisation logic is maintained in:

```text
core/charts.py
```

---

## Scores

The Scores page allows users to assign a score to each option against each criterion.

Scores must fall within the permitted scoring range:

```text
0 to 100
```

The score matrix is generated dynamically based on the current:

- Options
- Criteria

Saved scores are stored in:

```python
scores_state
```

and are included when a project is exported.

When project JSON is loaded, previously saved scores should be restored into the score matrix.

---

## PDF Report

The Results page allows users to generate a PDF report of the prioritisation analysis.

PDF generation is handled by:

```text
reports/pdf_report.py
```

The report uses the application state and calculated results to provide a portable summary of the analysis.

Depending on the decision type, the report may include:

- Decision context
- Decision objectives
- Options/interventions
- Criteria
- Criterion weights
- Scores
- Weighted scores
- Benefit Scores
- STAR-MCDA costs
- Total Benefit
- Value for Money results
- Rankings
- Results visualisations

If report content or formatting needs changing, start with:

```text
reports/pdf_report.py
```

---

## Charts and Visualisations

Charts are maintained primarily in:

```text
core/charts.py
```

### MCDA

MCDA uses a results visualisation to show weighted criterion contributions and overall option performance.

### STAR-MCDA

STAR-MCDA uses an efficiency frontier based on cumulative cost and benefit.

Plotly/ShinyWidgets are used for interactive STAR-MCDA visualisation.

---

## Project Configuration and Branding

The application has been structured so the underlying functionality can be reused across differently branded projects.

Project-specific configuration is stored under:

```text
config/
```

The active project configuration is controlled through:

```text
config/active_project.py
```

Configuration may include:

- Project name
- Project subtitle
- Footer text
- Logo
- Colour palette
- Chart colours
- Suggested/default criteria

Shared application themes and CSS are maintained in:

```text
core/themes.py
```

When changing project branding, avoid duplicating core application functionality unnecessarily.

---

## Reusable Components

Reusable UI components are maintained in:

```text
modules/components.py
```

These currently include elements such as:

- Page header
- Application banner
- Landing-page navigation cards
- Decision cards
- Page navigation
- Results navigation cards
- Application footer

Shared UI behaviour should preferably be changed here rather than duplicated across individual pages.

---

## Where to Make Common Changes

| Change required                   | Main location                                                |
|-----------------------------------|--------------------------------------------------------------|
| Main application/server behaviour | `app.py`                                                     |
| Landing page navigation cards     | `project specific pages in config/`                          |
| Decision page                     | `modules/decision.py`                                        |
| Options page                      | `modules/options.py`                                         |
| Criteria page                     | `modules/criteria.py` or `project specific pages in config/` |
| Weighting page                    | `modules/weighting.py`                                       |
| STAR cost page                    | `modules/star_cost.py` / `app.py`                            |
| Scores page                       | `modules/scores.py` / `app.py`                               |
| Results page                      | `modules/results.py` / `app.py`                              |
| Shared cards/buttons/navigation   | `modules/components.py`                                      |
| Weight calculations               | `calculations/weights_calc.py`                               |
| MCDA results                      | `calculations/mcda_results_calc.py`                          |
| STAR-MCDA results                 | `calculations/star_results_calc.py`                          |
| Efficiency frontier               | `calculations/star_results_calc.py` and `core/charts.py`     |
| Charts                            | `core/charts.py`                                             |
| Validation                        | `core/validators.py`                                         |
| Application themes                | `core/themes.py`                                             |
| Project branding                  | `config/`                                                    |
| Active project                    | `config/active_project.py`                                   |
| PDF report                        | `reports/pdf_report.py`                                      |
| Logos/assets                      | `assets/`                                                    |

---

## Development Approach

The application separates functionality into several layers:

### UI

Individual pages are maintained under:

```text
modules/
```

### Application orchestration

Cross-page state, navigation, saving/loading, and server behaviour are primarily handled in:

```text
app.py
```

### Calculations

Method-specific calculations should be kept under:

```text
calculations/
```

### Charts

Reusable chart-generation logic should be kept under:

```text
core/charts.py
```

### Configuration

Project-specific names, colours, branding, and defaults should be kept under:

```text
config/
```

### Reports

PDF-specific logic should remain under:

```text
reports/
```

When modifying the application, maintain this separation where practical rather than placing all functionality in `app.py`.

---

## Git and GitHub Workflow

Git/GitHub is used for version control.

Before starting new development work:

```bash
git pull
```

Check the current repository state:

```bash
git status
```

After making and testing changes:

```bash
git add .
git status
git commit -m "Describe the changes made"
git push
```

For example:

```bash
git commit -m "Update STAR-MCDA benefit calculations and interface"
```

### Files that should generally not be committed

Local or environment-specific files should be excluded through `.gitignore`, including where applicable:

```text
.venv/
venv/
__pycache__/
.idea/
.posit/
.env
```

Never commit passwords, access tokens, API keys, credentials, or other secrets.

---

## Testing Before Deployment

Before publishing a new version, test the complete workflow locally.

### MCDA checklist

- [ ] Landing page loads
- [ ] Decision context can be entered
- [ ] MCDA decision type can be selected
- [ ] Options can be added/deleted
- [ ] Criteria can be added/deleted
- [ ] Criterion weights can be entered
- [ ] Weights normalise correctly
- [ ] Scores can be entered
- [ ] Scores remain within 0–100
- [ ] Results calculate correctly
- [ ] Rankings are correct
- [ ] MCDA visualisation displays correctly
- [ ] Export Project works
- [ ] Load Project restores data
- [ ] PDF report downloads successfully
- [ ] Light/dark theme functions correctly

### STAR-MCDA checklist

In addition to the above:

- [ ] STAR-MCDA decision type can be selected
- [ ] Cost stage appears only where appropriate
- [ ] Cost per person can be entered
- [ ] Number of people can be entered
- [ ] Total Cost calculates correctly
- [ ] Benefit Score calculates correctly
- [ ] Total Benefit includes population size correctly
- [ ] VFM Ratio calculates correctly
- [ ] Lower VFM Ratio receives the better ranking
- [ ] Zero/invalid Total Benefit is handled safely
- [ ] Efficiency frontier displays correctly
- [ ] Chart labels/hover information is correct
- [ ] STAR-MCDA PDF report contains the appropriate results
- [ ] Exported STAR-MCDA projects reload correctly

---

## Deployment

The application has been tested/deployed using Posit Connect Cloud during development.

Deployment configuration may change, so the following should be checked at handover:

- Hosting platform
- Deployment account/owner
- Repository
- Deployment branch
- Deployment method
- Application URL
- Python version
- Dependency configuration
- Any environment variables
- Hosting usage limits

### Posit Connect Cloud

- When using a free hosting tier, be aware that compute/usage allowances may limit availability.

- Exceeding the hosting account's allowance may make the deployed application temporarily unavailable until the allowance resets or the hosting plan is changed.

- For this reason, hosting arrangements should be reviewed before relying on the application as a continuously available production service.

---

## Potential Alternative Hosting

Alternative deployment approaches may be investigated depending on organisational requirements.

Possible options include:

- Posit Connect Cloud
- GitHub-based deployment workflows
- Shinylive with static hosting where package/functionality compatibility allows

Before changing hosting platform, test all functionality, particularly:

- Shiny reactive behaviour
- ShinyWidgets
- Plotly
- Project JSON upload/download
- PDF generation
- Asset loading
- Multi-module imports

---

## Data and Information Governance

- The application is intended to support healthcare prioritisation and decision analysis.

- The hosting environment and information-governance requirements should be reviewed before entering or processing confidential, sensitive, personal, or patient-identifiable data.

- For publicly hosted development or demonstration versions, users should avoid entering patient-identifiable or otherwise confidential information.

- Production deployment should follow the relevant organisational information-governance, security, and hosting requirements.

---

## Known Limitations

Current considerations include:

- Application data is primarily held in reactive session state.
- Session state is not permanent storage.
- Users should use Export Project to retain their work.
- Exported projects must be retained by the user if the project will be revisited later.
- Hosting availability depends on the hosting platform and applicable usage limits.
- Free hosting services may impose compute, runtime, bandwidth, build, or availability restrictions.
- The application is under active development and should be tested after calculation, workflow, or dependency changes.

Add newly identified issues to this section rather than relying on undocumented knowledge.

---

## Handover Checklist

Before transferring responsibility for the application to another developer/analyst, confirm that the colleague has:

- [ ] Access to the GitHub repository
- [ ] Access to the appropriate Git branch
- [ ] Access to the deployment platform, where required
- [ ] The correct Python version/environment
- [ ] The application running locally
- [ ] An understanding of MCDA calculations
- [ ] An understanding of STAR-MCDA calculations
- [ ] Tested project Export and Load
- [ ] Tested PDF generation
- [ ] Tested the MCDA workflow
- [ ] Tested the STAR-MCDA workflow
- [ ] Reviewed the deployment configuration
- [ ] Reviewed outstanding issues/work

---

## Key Handover Notes

A new developer should understand the following before making substantial changes:

1. `app.py` orchestrates the application and maintains cross-page reactive state.
2. Page UI is generally separated into files under `modules/`.
3. Reusable UI components are maintained in `modules/components.py`.
4. Calculation logic should remain under `calculations/`.
5. STAR-MCDA uses population size to calculate Total Benefit.
6. STAR-MCDA VFM ranking is based on cost per unit of Total Benefit.
7. Chart logic is maintained primarily in `core/charts.py`.
8. PDF generation is maintained in `reports/pdf_report.py`.
9. Project branding/configuration is separated under `config/`.
10. Export Project is the mechanism for retaining project data beyond the active application session.
11. Changes should be tested in both MCDA and STAR-MCDA before deployment.
12. GitHub should be kept up to date so that the repository remains the authoritative version of the application.

---

## Future Development

Potential future development areas may include:

- Further sensitivity-analysis functionality
- Additional validation and user guidance
- Hosting/deployment improvements

Any substantial methodological changes should be documented in this README.

---

## Maintenance

When making a substantial change to the application:

1. Update and test the code.
2. Test both MCDA and STAR-MCDA where the change could affect both.
3. Update calculation/report logic where necessary.
4. Update this README if the architecture, methodology, workflow, dependencies, or deployment process changes.
5. Commit the changes to Git.
6. Push the tested version to GitHub.
7. Deploy/re-publish where appropriate.
8. Verify the deployed application after publication.

The README should be maintained alongside the code so that it remains suitable for future handover.



