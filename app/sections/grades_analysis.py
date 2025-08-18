from typing import Union

import pandas as pd
import streamlit as st
from backend.data_extractors import ExitEmbaExtractor
from backend.plotter import PlotGenerator


def render(emba_extractor: ExitEmbaExtractor) -> None:
    """Render boxplot visualizations and CSI summary using Streamlit.

    Displays:
    - Customer Satisfaction Index (CSI) for the program.
    - Boxplots for various components of the educational experience.

    Args:
        emba_extractor (ExitEmbaExtractor): Data extractor providing CSI-related survey results.
    """
    st.header("Анализ оценок")

    def _render_boxplot(title: str, data: Union[pd.Series, pd.DataFrame]) -> None:
        """Render a boxplot inside a collapsible Streamlit expander.

        Args:
            title (str): Title for the plot and expander section.
            data (Union[pd.Series, pd.DataFrame]): DataFrame or Series used for boxplot generation.
        """
        fig = PlotGenerator.make_boxplot(data=data, title=title)
        with st.expander(title):
            st.plotly_chart(fig, use_container_width=True)

    overall_csi = emba_extractor.get_overall_csi()
    csi = emba_extractor.calulate_csi(overall_csi)
    st.markdown(f"#### Общее значение CSI* для всей программы: {csi:.2}/10")
    st.markdown(
        "\* CSI (Customer Satisfaction Index) - метрика, показывающая насколько\
        клиенты удовлетворены продуктом."
    )

    _render_boxplot("Оценка программы в целом", emba_extractor.get_basic_csi())
    _render_boxplot("Распределение оценок различных составляющих курса", overall_csi)
    _render_boxplot("Оценка дизайна программы", emba_extractor.get_design_csi())
    _render_boxplot(
        "Оценка международных модулей", emba_extractor.get_intern_modules_csi()
    )
    _render_boxplot("Оценка работы команды курса", emba_extractor.get_support_csi())
    _render_boxplot("Оценка качества группы", emba_extractor.get_group_csi())
    _render_boxplot("Оценка работы команды курса", emba_extractor.get_support_csi())
    _render_boxplot("Оценка качества группы", emba_extractor.get_group_csi())
