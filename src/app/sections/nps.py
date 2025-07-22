import streamlit as st

from backend.plotter import PlotGenerator


def render(emba_extractor):
    st.header("NPS")

    def _render_nps(title, barnames, values, colors):
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
