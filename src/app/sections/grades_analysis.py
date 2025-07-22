import streamlit as st

from backend.plotter import PlotGenerator


def render(emba_extractor):
    st.header("Анализ оценок")

    def _render_boxplot(title, data):
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
