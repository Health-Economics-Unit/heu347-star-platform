from shiny import ui


def calculate_total_cost(
    cost_per_person,
    people_receiving
):

    try:
        cost_per_person = float(cost_per_person)
    except:
        cost_per_person = 0

    try:
        people_receiving = int(people_receiving)
    except:
        people_receiving = 0

    return cost_per_person * people_receiving