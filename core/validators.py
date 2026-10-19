#-------Validations------------------------------------------------------------------------------------------

def validate_decision(decision_description,decision_type):

    errors = []

    if not decision_description.strip():
        errors.append(
                "Decision description is required."
        )

    if decision_type is None:
            errors.append(
                "A decision type must be selected."
        )

    return errors

#----------Validation for Options page----------------------------------------------------------

def validate_options(options):
    errors = []

    if len(options) == 0:
        errors.append(
            "At least one option must be added."
        )

    return errors

#----------Validation for Criteria page----------------------------------------------------------

def validate_criteria(criteria):
    errors = []

    if len(criteria) == 0:
        errors.append(
            "At least one criteria must be added or selected."
        )

    return errors
