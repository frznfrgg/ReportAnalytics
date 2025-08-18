from typing import List

import streamlit as st
from backend.data_extractors import ExitEmbaExtractor
from backend.plotter import PlotGenerator


def render(emba_extractor: ExitEmbaExtractor) -> None:
    """Render Net Promoter Score (NPS) bar plots using Streamlit and Plotly.

    Displays NPS comparisons:
    - Between EMBA-35 and other industries.
    - Across various programs at the institution.

    Args:
        emba_extractor (ExitEmbaExtractor): Extractor object providing NPS-related data.
    """
    st.header("NPS")

    def _render_nps(
        title: str,
        barnames: List[str],
        values: List[int],
        colors: List[str],
    ) -> None:
        """Render an NPS bar plot inside a collapsible Streamlit expander.

        Args:
            title (str): Title of the plot and expander section.
            barnames (List[str]): Labels for each bar.
            values (List[int]): Numerical values for each group.
            colors (List[str]): Bar colors corresponding to NPS categories.
        """
        fig = PlotGenerator.make_nps_barplot(
            barnames=barnames, values=values, colors=colors, title=title
        )
        with st.expander(title):
            st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        "NPS (Net Promoter Score) - индекс потребительской лояльности, \
        показывающий насколько клиенты довольны компанией и готовы рекомендовать ее услуги."
    )

    barnames, values, colors = emba_extractor.get_industry_nps()
    _render_nps("NPS EMBA-35 vs NPS индустрии", barnames, values, colors)
    barnames, values, colors = emba_extractor.get_programs_nps()
    _render_nps("Сравнение NPS разных программ Школы", barnames, values, colors)
    barnames, values, colors = emba_extractor.get_programs_nps()
    _render_nps("Сравнение NPS разных программ Школы", barnames, values, colors)
