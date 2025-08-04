from typing import Union

import pandas as pd
import streamlit as st
from backend.data_extractors import ExitEmbaExtractor
from backend.plotter import PlotGenerator


def render(emba_extractor: ExitEmbaExtractor) -> None:
    """Render horizontal bar charts for additional survey insights using Streamlit.

    Displays:
    - Top-voted lecturers.
    - Areas where alumni are willing to collaborate.

    Args:
        emba_extractor (ExitEmbaExtractor): Extractor providing survey-derived insights.
    """
    st.header("Прочее")

    def _render_hbar(
        title: str,
        data: Union[pd.Series, pd.DataFrame],
        x_axs_title: str,
        y_axs_title: str,
    ) -> None:
        """Render a horizontal bar chart inside a collapsible Streamlit expander.

        Args:
            title (str): Title of the plot and expander.
            data (Union[pd.Series, pd.DataFrame]): Data to plot; typically a Series of counts.
            x_axs_title (str): Label for the x-axis.
            y_axs_title (str): Label for the y-axis.
        """
        fig = PlotGenerator.make_hbarplot(
            score_counts=data,
            title=title,
            x_axs_title=x_axs_title,
            y_axs_title=y_axs_title,
        )
        with st.expander(title):
            st.plotly_chart(fig, use_container_width=True)

    _render_hbar(
        "Лучшие преподаватели",
        emba_extractor.get_top_lectors(),
        x_axs_title="Количество голосов",
        y_axs_title="Преподаватель",
    )
    _render_hbar(
        "В каких активностях готовы участвовать выпускники",
        emba_extractor.get_collaborators(),
        x_axs_title="Количество согласившихся",
        y_axs_title="Готов участвовать в...",
    )
