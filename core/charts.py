import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np

#--------------MCDA bar chart-------------------------------------------------------------------------------

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
        color="#1F4E99",
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

    ax.set_ylim(0, 105)         # fixing the y axis from 0 to 100
    ax.set_yticks(range(0, 101, 20))

    fig.tight_layout()

    return fig

# ---------------- STAR-MCDA efficiency frontier chart ------------------------

def create_efficiency_frontier(
    frontier_results,
    chart_colours
):

    fig = go.Figure()


    # No results

    if not frontier_results:

        fig.add_annotation(
            text=(
                "No results available.<br>"
                "Complete the Weighting, Cost and Scores pages first."
            ),
            x=0.5,
            y=0.5,
            xref="paper",
            yref="paper",
            showarrow=False,
            align="center",
            font=dict(
                size=14
            )
        )

        fig.update_xaxes(
            visible=False
        )

        fig.update_yaxes(
            visible=False
        )

        fig.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            showlegend=False
        )

        return fig


    # Filled intervention triangles

    for index, result in enumerate(frontier_results):

        start_cost = result["start_cost"]
        start_benefit = result["start_benefit"]

        end_cost = result["end_cost"]
        end_benefit = result["end_benefit"]

        colour = chart_colours[
            index % len(chart_colours)
        ]

        hover_text = (
            f"<b>{result['option']}</b><br>"
            f"Total Cost: £{result['cost']:,.2f}<br>"
            f"Benefit Score: {result['benefit_score']:.2f}<br>"
            f"VFM Ratio: {result['vfm_ratio']:.2f} per benefit<br>"
            f"VFM Rank: {result['rank']}"
        )

        fig.add_trace(
            go.Scatter(
                x=[
                    start_cost,
                    end_cost,
                    end_cost,
                    start_cost,
                    start_cost
                ],

                y=[
                    start_benefit,
                    start_benefit,
                    end_benefit,
                    start_benefit,
                    start_benefit
                ],

                mode="lines",

                fill="toself",
                fillcolor=colour,

                line=dict(
                    color=colour,
                    width=0
                ),

                opacity=0.80,

                name=result["option"],

                text=[
                    hover_text,
                    hover_text,
                    hover_text,
                    hover_text,
                    hover_text
                ],

                hovertemplate=(
                    "%{text}"
                    "<extra></extra>"
                ),

                # Makes the filled area the hover target
                hoveron="fills"
            )
        )

    # Layout

    fig.update_layout(

        # title=dict(
        #     text="Efficiency Frontier",
        #     x=0.01,
        #     xanchor="center"
        # ),

        height=550,

        xaxis=dict(
            title="Cumulative Cost (£)",

            tickprefix="£",
            tickformat=",",

            rangemode="tozero",

            showgrid=False,

            showline=True,
            linecolor="#333333",
            linewidth=1,

            ticks="outside",
            tickcolor="#333333",

            zeroline=False
        ),

        yaxis=dict(
            title="Cumulative Benefit Score",

            rangemode="tozero",

            showgrid=False,

            showline=True,
            linecolor="#333333",
            linewidth=1,

            ticks="outside",
            tickcolor="#333333",

            zeroline=False
        ),

        # Legend outside the graph
        legend=dict(
            title="Interventions",

            orientation="v",

            x=1.02,
            y=1,

            xanchor="left",
            yanchor="top",

            bgcolor="rgba(255,255,255,1)",

            bordercolor="#DDDDDD",
            borderwidth=1
        ),

        hovermode="closest",

        plot_bgcolor="white",
        paper_bgcolor="white",

        # Space reserved for legend
        margin=dict(
            l=80,
            r=180,
            t=85,       # gap between the legend and the plot zoom features etc
            b=70
        )
    )

    return fig