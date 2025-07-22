import streamlit as st

from app.sections import base_distributions, grades_analysis, nps, other, pilos
from backend.data_extractors import ExitEmbaExtractor
from backend.raw_data_processor import process_exit_survey

# Page config
st.set_page_config(page_title="EMBA-35 report", layout="wide")

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
            "Pairings",
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
    if "Pairings" in section_types:
        st.header("Pairings")
        st.markdown("#### Coming soon...")
