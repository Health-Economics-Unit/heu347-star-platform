import matplotlib.pyplot as plt
import numpy as np


def create_results_chart(results, chart_colours):

    if not results:

        fig, ax = plt.subplots()

        ax.text(
            0.5,
            0.5,
            (
                "No results available.\n"
                "Complete the Weighting and Scores pages first."
            ),
            ha="center",
            va="center",
            transform=ax.transAxes
        )

        ax.axis("off")

        return fig

    criterion_names = list(
        results[0]["weighted_scores"].keys()
    )

    option_names = [
        result["option"]
        for result in results
    ]

    x_positions = np.arange(
        len(option_names)
    )

    bottom_values = np.zeros(
        len(option_names)
    )

    fig, ax = plt.subplots(
        figsize=(11, 6)
    )

    for index, criterion_name in enumerate(
        criterion_names
    ):

        criterion_values = [
            result["weighted_scores"].get(
                criterion_name,
                0
            )
            for result in results
        ]

        colour = chart_colours[
            index % len(chart_colours)
        ]

        ax.bar(
            x_positions,
            criterion_values,
            bottom=bottom_values,
            label=criterion_name,
            color=colour,
            width=0.65
        )

        bottom_values += np.array(
            criterion_values
        )

    for index, result in enumerate(results):

        ax.text(
            index,
            result["benefit_score"] + 1,
            f"{result['benefit_score']:.2f}",
            ha="center",
            va="bottom",
            fontweight="bold"
        )

    ax.set_title(
        "Contribution of Criteria to Overall Benefit Score",
        fontsize=14,
        fontweight="bold",
        pad=20
    )

    ax.set_xlabel(
        "Options"
    )

    ax.set_ylabel(
        "Weighted Score"
    )

    ax.set_xticks(
        x_positions
    )

    ax.set_xticklabels(
        option_names
    )

    ax.legend(
        title="Criteria",
        bbox_to_anchor=(1.02, 1),
        loc="upper left",
        frameon=False
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.grid(
        axis="y",
        linestyle="--",
        alpha=0.3
    )

    ax.set_axisbelow(True)

    fig.tight_layout()

    return fig