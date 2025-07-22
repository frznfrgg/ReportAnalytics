import streamlit as st

from backend.plotter import PlotGenerator


def render(emba_extractor):
    st.header("Распределение оценок PILOs")
    st.markdown(
        "PILOs (Programme Intended Learning Outcomes) - программа предполагаемых результатов обучения."
    )

    def _render_stacked_bar(title, data):
        fig = PlotGenerator.make_stacked_barplot(
            score_counts=data,
            title=title,
            x_axs_title="Предмет",
            y_axs_title="Количество студентов",
        )
        with st.expander(title):
            st.plotly_chart(fig, use_container_width=True)

    _render_stacked_bar("Распределение оценок PILOs", emba_extractor.get_pilos())
