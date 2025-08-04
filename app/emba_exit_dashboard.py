"""Rendering the main page of an report app."""

import streamlit as st
from backend.data_extractors import ExitEmbaExtractor
from backend.raw_data_processor import process_exit_survey

from app.sections import (
    base_distributions,
    download,
    grades_analysis,
    nps,
    other,
    pilos,
)

# Page config
st.set_page_config(page_title="EMBA-35 report", layout="wide")
st.markdown(
    """
    ## Отчет EMBA-35
<div style='font-size:18px'>
    Опрос проводится после итоговой аттестации среди студентов, завершивших обучение.<br>
    Он включает <strong>15</strong> вопросов об оценке программы, результатов, команды и предпочтениях в общении со Школой.<br>
    <strong>Цель:</strong> получить обратную связь выпускников для улучшения программы, использования в маркетинге, подготовки аккредитационной отчётности.<br><br>
</div>
""",
    unsafe_allow_html=True,
)

# Sidebar
st.sidebar.title("Фильтры")
with st.sidebar:
    section_types = st.multiselect(
        label="По разделам:",
        options=[
            "Базовые распределения",
            "Анализ оценок",
            "NPS",
            "PILOs",
            "Прочие графики",
            "Скачать отчет",
        ],
    )

# File loader
excel_file = st.file_uploader(
    label="Загрузите excel-файл с опросом по программе EMBA-35",
    type=["xls", "xlsx"],
    key="competencies_excel",
    accept_multiple_files=False,
)

# File processing (in back)
if "survey_processed" not in st.session_state:
    st.session_state.survey_processed = False

if excel_file and not st.session_state.survey_processed:
    processed_file = process_exit_survey(excel_file)
    emba_extractor = ExitEmbaExtractor(processed_file)
    st.session_state.emba_extractor = emba_extractor
    st.session_state.survey_processed = True

# Results (main render)
if st.session_state.survey_processed:
    emba_extractor = st.session_state.emba_extractor
    if "Базовые распределения" in section_types:
        base_distributions.render(emba_extractor)
    if "Анализ оценок" in section_types:
        grades_analysis.render(emba_extractor)
    if "NPS" in section_types:
        nps.render(emba_extractor)
    if "PILOs" in section_types:
        pilos.render(emba_extractor)
    if "Прочие графики" in section_types:
        other.render(emba_extractor)
    if "Скачать отчет" in section_types:
        if st.button("Скачать отчет"):
            docx_path = download.generate_docx(emba_extractor)
    if "Pairings" in section_types:
        st.header("Pairings")
        st.markdown("#### Coming soon...")
        other.render(emba_extractor)
    if "Скачать отчет" in section_types:
        if st.button("Скачать отчет"):
            docx_path = download.generate_docx(emba_extractor)
    if "Pairings" in section_types:
        st.header("Pairings")
        st.markdown("#### Coming soon...")
