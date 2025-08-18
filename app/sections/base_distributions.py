from typing import Union

import pandas as pd
import streamlit as st
from backend.data_extractors import ExitEmbaExtractor
from backend.plotter import PlotGenerator


def render(emba_extractor: ExitEmbaExtractor) -> None:
    """Render pie charts showing basic demographic distributions of EMBA survey respondents using Streamlit.

    Displays:
    - Age distribution of students.
    - Distribution of students across industries.
    - Distribution of students by job positions.
    Args:
        emba_extractor (ExitEmbaExtractor): Object that provides preprocessed survey data for visualization.
    """
    st.header("Базовые распределения")

    def _render_pie(title: str, data: Union[pd.DataFrame, pd.Series]) -> None:
        """Helper function to render a pie chart within an expandable section.

        Args:
            title (str): Title of the chart and expander.
            data (Union[pd.DataFrame, pd.Series]): Dictionary where keys are labels and values are counts.
        """
        fig = PlotGenerator.make_piechart(data=data, title=title)
        with st.expander(title):
            st.plotly_chart(fig, use_container_width=True)

    _render_pie("Распределение возрастов", emba_extractor.get_age_distr())
    _render_pie(
        "Распределение студентов по индустриям", emba_extractor.get_industry_distr()
    )
    _render_pie(
        "Распределение студентов по занимаемым должностям",
        emba_extractor.get_job_distr(),
    )
