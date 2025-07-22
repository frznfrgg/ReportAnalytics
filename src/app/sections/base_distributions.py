import streamlit as st
from backend.plotter import PlotGenerator


def render(emba_extractor):
    st.header("Базовые распределения")

    def _render_pie(title, data):
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
