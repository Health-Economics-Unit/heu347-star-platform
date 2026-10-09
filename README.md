# HEU Strategic Prioritisation Platform

**Health Economics Unit (HEU)**
**Developer:** Akshata Ahire
**Organisation:** Imperial College Healthcare NHS Trust  
**Status:** Active Development

## Overview

The HEU Strategic Prioritisation Platform is a Python Shiny application designed to support health economics prioritisation, Socio-Technical Allocation of Resources (STAR) analysis, and decision-making within healthcare settings.

The platform enables decision-makers to:
- Define decision contexts and objectives
- Evaluate and compare competing options
- Apply multi-criteria decision analysis (MCDA) principles
- Perform STAR-based prioritisation
- Explore scenario and sensitivity analyses
- Support transparent and evidence-based resource allocation

## Current Development Status

The application is currently under active development.

## Technology Stack

- Python
- Shiny for Python
- Pandas
- Plotly
- HTML/CSS
- Git/GitHub

## Repository Structure

```text
app.py          Main application entry point and application orchestration
config/         Project specific settings for MCDA/STAR/HSE for now
modules/        Application UI pages 
components/     Reusable UI components
core/           Shared logic and utilities
calculations/   All calculations weighting, ranking etc
visuals/        App logo, images etc