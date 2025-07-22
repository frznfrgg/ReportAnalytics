from typing import Dict, List

import pandas as pd
import plotly.graph_objects as go
from plotly.colors import sample_colorscale


class PlotGenerator:
    title_template = {
        "text": "SAMPLE_TITLE",
        "x": 0.45,
        "xanchor": "center",
        "y": 0.9,
        "font": dict(size=20),
    }

    rectangle_template = dict(
        type="rect",
        xref="paper",
        yref="y",
        x0=0,
        x1=1,
        y0=0,
        y1=20,
        fillcolor="SAMPLE COLOR",
        opacity=0.4,
        line_width=0,
    )

    @classmethod
    def _make_title(cls, title_text: str):
        title = cls.title_template.copy()
        title["text"] = title_text
        return title

    # used in nps barplots as backgroud
    @classmethod
    def _edit_shape(cls, y0: int, y1: int, color: str) -> dict:
        shape = cls.rectangle_template.copy()
        shape["fillcolor"] = color
        shape["y0"] = y0
        shape["y1"] = y1
        return shape

    # used to make legends for non-data objects in plot (e.g. background shapes)
    @staticmethod
    def _make_legend(legend_text: str, color: str) -> dict:
        dummy_legend = dict(
            x=[None],
            y=[None],
            mode="markers",
            marker=dict(size=10, color=color, opacity=0.6),
            name=legend_text,
        )
        invisible_fig = go.Scatter(dummy_legend)
        return invisible_fig

    @classmethod
    def make_boxplot(cls, data: Dict[str, List[float]], title: str) -> go.Figure:
        fig = go.Figure()
        for name in data.keys():
            fig.add_trace(go.Box(y=data[name], name=name, boxmean=True))

        fig.update_xaxes(tickangle=0)
        fig.update_layout(title=cls._make_title(title))
        return fig

    @classmethod
    def make_piechart(cls, data: Dict[str, float], title: str) -> go.Figure:
        total = sum(list(data.values()))
        fig = go.Figure()
        fig.add_trace(
            go.Pie(labels=list(data.keys()), values=list(data.values()), name=title)
        )
        fig.update_traces(hole=0.4, hoverinfo="value+percent+label")
        fig.update_layout(
            title=cls._make_title(title),
            annotations=[
                dict(
                    text=f"<b>{total}</b>", x=0.5, y=0.5, font_size=20, showarrow=False
                )
            ],
        )
        return fig

    @classmethod
    def make_nps_barplot(
        cls, barnames: List[str], values: List[int], colors: List[str], title: str
    ) -> go.Figure:
        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                x=barnames,
                y=values,
                showlegend=False,
                name="",
                marker=dict(color=colors),
            )
        )
        fig.add_traces(
            [
                cls._make_legend("Good (by Bain&Company)", color="#b2df8a"),
                cls._make_legend("Favorable (by Bain&Company)", color="#66bb6a"),
                cls._make_legend("Excellent (by Bain&Company)", color="#388e3c"),
                cls._make_legend("World class (by Bain&Company)", color="#1b5e20"),
            ]
        )
        fig.update_layout(
            height=600,
            title=cls._make_title(title),
            yaxis=dict(range=[-100, 100]),
            shapes=[
                cls._edit_shape(y0=0, y1=20, color="#b2df8a"),
                cls._edit_shape(y0=20, y1=50, color="#66bb6a"),
                cls._edit_shape(y0=50, y1=80, color="#388e3c"),
                cls._edit_shape(y0=80, y1=100, color="#1b5e20"),
            ],
        )
        return fig

    @classmethod
    def make_stacked_barplot(
        cls,
        score_counts: pd.DataFrame,
        title: str,
        x_axs_title: str = "x",
        y_axs_title: str = "y",
    ):
        fig = go.Figure()
        colors = sample_colorscale("RdYlGn", [i / 9 for i in range(10)])
        for score in range(1, 11):
            fig.add_trace(
                go.Bar(
                    x=score_counts["param"],
                    y=score_counts[score],
                    name=str(score),
                    marker_color=colors[score - 1],
                )
            )
        fig.update_layout(
            height=600,
            title=cls._make_title(title),
            barmode="stack",
            xaxis_title=x_axs_title,
            yaxis_title=y_axs_title,
        )
        fig.update_xaxes(tickangle=270)
        return fig

    @classmethod
    def make_hbarplot(
        cls,
        score_counts: Dict[str, int],
        title: str,
        x_axs_title: str = "x",
        y_axs_title: str = "y",
    ):
        fig = go.Figure()
        num_colors = len(set(score_counts.values()))
        palette = sample_colorscale(
            "Greens", [i / (num_colors - 1) for i in range(num_colors)]
        )
        votes_to_colors = dict(zip(sorted(set(score_counts.values())), palette))
        scores_colors = [votes_to_colors[i] for i in score_counts.values()]
        fig.add_trace(
            go.Bar(
                x=list(score_counts.values()),
                y=list(score_counts.keys()),
                marker_color=scores_colors,
                orientation="h",
            )
        )
        fig.update_layout(
            height=600,
            title=cls._make_title(title),
            barmode="stack",
            xaxis_title=x_axs_title,
            yaxis_title=y_axs_title,
        )

        return fig
