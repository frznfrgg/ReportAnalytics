import pandas as pd
import streamlit as st
from backend.data_extractors import ExitEmbaExtractor
from backend.plotter import PlotGenerator


def render(emba_extractor: ExitEmbaExtractor) -> None:
    """Render PILOs score distributions using Streamlit and Plotly visualizations.

    Displays a header and description, then renders a collapsible stacked barplot
    showing the distribution of student scores on Programme Intended Learning Outcomes (PILOs).

    Args:
        emba_extractor (ExitEmbaExtractor): An object with a `get_pilos()` method returning a DataFrame
                        suitable for `PlotGenerator.make_stacked_barplot`
    """
    st.header("Распределение оценок PILOs")
    st.markdown(
        "PILOs (Programme Intended Learning Outcomes) - программа предполагаемых результатов обучения."
    )

    def _render_stacked_bar(title: str, data: pd.DataFrame) -> None:
        """Render a single stacked bar chart in a collapsible expander.

        Args:
            title (str): The title for both the chart and the expander section.
            data (pd.DataFrame): A DataFrame where rows represent categories (e.g., subjects)
            and columns represent score counts to be visualized.
        """
        fig = PlotGenerator.make_stacked_barplot(
            score_counts=data,
            title=title,
            x_axs_title="Предмет",
            y_axs_title="Количество студентов",
        )
        with st.expander(title):
            st.plotly_chart(fig, use_container_width=True)

    _render_stacked_bar("Распределение оценок PILOs", emba_extractor.get_pilos())
    _render_stacked_bar("Распределение оценок PILOs", emba_extractor.get_pilos())
