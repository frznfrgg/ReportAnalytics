import streamlit as st

from backend.plotter import PlotGenerator


def render(emba_extractor):
    st.header("Прочее")

    def _render_hbar(title, data, x_axs_title, y_axs_title):
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
