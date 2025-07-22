"""Add classes of data extractors for different surveys/tables/programs here."""

from typing import IO, Dict, List

import pandas as pd


class ExitEmbaExtractor:
    def __init__(self, table_path: str | IO):
        self.df = pd.read_excel(table_path)

    # below are methods for extracting data, used in piecharts
    def get_age_distr(self, age_Qind: int = 15):
        age_groups = {
            1.0: "18-24",
            2.0: "25-34",
            3.0: "35-44",
            4.0: "45-54",
            5.0: "55+",
        }
        age_counts = self.df[f"Q{age_Qind} 🔴  Укажите ваш  возраст"].value_counts()
        age_counts.index = age_counts.index.to_series().map(age_groups)
        age_counts = age_counts.to_dict()
        return age_counts

    def get_industry_distr(self, industry_Qind: int = 14):
        industry_codes = {
            1: "Средства массовой информации и развлечения",
            2: "Здравоохранение",
            3: "Образование",
            4: "Некоммерческие организации, неправительственные организации",
            5: "Государственный сектор",
            6: "Консалтинг",
            7: "Недвижимость",
            8: "Финансы",
            9: "Технологии",
            10: "Отели, Рестораны, Кейтеринг",
            11: "Логистика",
            12: "Товары народного потребления",
            13: "Торговля",
            14: "Строительство",
            15: "Энергетика",
            16: "Производство",
            17: "Добыча полезных ископаемых",
            18: "Сельское хозяйство",
            19: "Другое",
        }
        industry_col = [
            col
            for col in self.df.columns
            if col.startswith(f"Q{industry_Qind}") and self.df[col].dtype == "int64"
        ][0]
        industry_counts = self.df[industry_col].value_counts()
        industry_counts.index = industry_counts.index.to_series().map(industry_codes)
        industry_counts = industry_counts.to_dict()
        return industry_counts

    def get_job_distr(self, job_Qinds: int = 13):
        job_cols = [
            col
            for col in self.df.columns
            if col.startswith(f"Q{job_Qinds}") and self.df[col].dtype == "int64"
        ]
        jobs_counts = self.df[job_cols].sum()
        jobs_counts = jobs_counts[jobs_counts > 0].sort_values(ascending=False)
        jobs_counts = jobs_counts.to_dict()
        return jobs_counts

    # below are methods for extracting data, used in boxplots
    def get_overall_csi(self, csi_Qinds: List[int] = [2, 3, 5, 7, 8, 9]):
        new_colnames = [
            "Общая оценка<br>программы (Q2)",
            "Насколько достигнуты<br>цели обучения (Q3)",
            "Дизайн<br>программы (Q5)",
            "Опыт на<br>международных<br>модулях (Q7)",
            "Работа команды<br>программы (Q8)",
            "Качество группы (Q9)",
        ]

        discrete_rate_cols = []
        for i in csi_Qinds:
            discrete_rate_cols.append(
                [col for col in self.df.columns if col.startswith(f"Q{i}")]
            )

        csi_data = {}
        for name, col in zip(new_colnames, discrete_rate_cols):
            mean_series = self.df[col].mean(axis=1)
            csi_data[name] = mean_series
        return csi_data

    def calulate_csi(self, csi_data: Dict[str, List[float]]):
        component_csis = []
        for value in list(csi_data.values()):
            component_csis.append(sum(value) / len(value))
        return sum(component_csis) / len(component_csis)

    def _get_csi(self, new_colnames: List[str], csi_Qind: int):
        csi_cols = [col for col in self.df.columns if col.startswith(f"Q{csi_Qind}")]
        ratings = [self.df[col] for col in csi_cols]
        csi_data = dict(zip(new_colnames, ratings))
        return csi_data

    def get_basic_csi(self, csi_Qind: int = 2):
        new_colnames = [
            "Административная<br>поддержка",
            "Приобретенные<br>знания",
            "ППС",
        ]
        return self._get_csi(new_colnames, csi_Qind)

    def get_design_csi(self, csi_Qind: int = 5):
        new_colnames = [
            "Логичность<br>содержания",
            "Баланс теории<br>и практики",
            "Применимость<br>знаний",
            "Актуальность<br>знаний",
            "Соотношение<br>глобальных<br>и региональных<br>модулей",
            "Достаточность<br>проектной<br>работы",
            "Качество<br>выступающих",
        ]
        return self._get_csi(new_colnames, csi_Qind)

    def get_intern_modules_csi(self, csi_Qind: int = 7):
        new_colnames = [
            "Качество<br>кейсов",
            "Применимость<br>знаний",
            "Групповая<br>работа",
            "Выбор<br>локаций",
        ]
        return self._get_csi(new_colnames, csi_Qind)

    def get_support_csi(self, csi_Qind: int = 8):
        new_colnames = [
            "Отклик<br>на потребности",
            "Организация<br>образовательного<br>процесса",
        ]
        return self._get_csi(new_colnames, csi_Qind)

    def get_group_csi(self, csi_Qind: int = 9):
        new_colnames = [
            "Поддержка\nи взаимопомощь",
            "Опыт и знания\nодногруппников",
            "Разнообразие\nиндустрий",
            "Приобритение\nделовых\nконтактов",
        ]
        return self._get_csi(new_colnames, csi_Qind)

    # below are methods for extracting data, used in barplots
    def _get_program_nps(self, nps_Qind: str = "12.1") -> int:
        nps_colname = f"Q{nps_Qind}  - 🔴  Готовы ли вы порекомендовать программу своим друзьям/коллегам?"
        num_students = self.df.shape[0]
        num_promoters = self.df[self.df[nps_colname] >= 9].shape[0]
        num_critics = self.df[self.df[nps_colname] <= 6].shape[0]
        nps_value = int((num_promoters - num_critics) / num_students * 100)
        return nps_value

    def get_industry_nps(self):
        nps_value = self._get_program_nps()
        labels = [
            "Уровень 'Отлично'\n by Quesionstar",
            "EMBA-35",
            "Сфера образования",
            "Сфера высшего\nобразования",
        ]
        values = [30, nps_value, 42, 51]
        colors = ["#A9A9A9"] * len(values)
        colors[1] = "#FF007F"
        return labels, values, colors

    def get_programs_nps(self):
        nps_value = self._get_program_nps()
        labels = [
            "EMBA-31+32",
            "EMBA-33",
            "EMBA-34",
            "EMBA-35",
            "SKOLKOVO DEGREE",
            "SKOLKOVO EMBA average",
        ]
        values = [57, 47, 51, nps_value, 65, 77]
        colors = ["#A9A9A9"] * len(values)
        colors[3] = "#FF007F"
        return labels, values, colors

    def get_pilos(self, nps_Qind: str = 3):
        q3_cols = [col for col in self.df.columns if col.startswith(f"Q{nps_Qind}")]
        new_colnames = [
            "Экспертный<br>уровень знания<br>бизнес-дисциплин",
            "Анализ данных<br>для принятия<br>решений",
            "Определение<br>стратегии для<br>устойчивого<br>развития",
            "Интеграционное<br>лидерство",
            "Эффективная<br>коммуникация",
            "Структурирование<br>стратегий",
            "Оценка контекста<br>и технологий",
            "Внедрение<br>ERS",
            "Креативность<br>новаторство",
            "Предпринимательское<br>мышление",
        ]
        PILOs_df = self.df[q3_cols]
        PILOs_df.columns = new_colnames
        PILOs_df = PILOs_df.astype(int)
        PILOs_df = PILOs_df.melt(var_name="param", value_name="score")
        score_counts = (
            PILOs_df.groupby(["param", "score"])
            .size()
            .unstack(fill_value=0)
            .reindex(columns=range(1, 11), fill_value=0)
        ).reset_index()
        return score_counts

    def get_top_lectors(self, lectors_Qind: int = 6) -> Dict[str, int]:
        lectors_cols = [
            col for col in self.df.columns if col.startswith(f"Q{lectors_Qind}")
        ]
        all_lectors = self.df[lectors_cols]
        mask_all_zeros = (all_lectors == 0).all(axis=1)
        zeros_count = mask_all_zeros.sum()
        lectors = all_lectors.loc[~mask_all_zeros, lectors_cols].values.flatten()
        lectors = [lector for lector in lectors if lector != 0]
        lectors_counts = pd.Series(lectors).value_counts()
        lectors_counts["Никто"] = zeros_count
        lectors_counts = lectors_counts.sort_values(ascending=True).to_dict()
        return lectors_counts

    def get_collaborators(self, collab_Qind: int = 11) -> Dict[str, int]:
        new_colnames = [
            "качестве приглашенного спикера",
            "качестве ментора",
            "мероприятиях для выпускников",
            "адмиссии",
            "другое",
            "в качестве протагониста",
            "отказываюсь",
        ]
        events_cols = [
            col
            for col in self.df.columns
            if col.startswith(f"Q{collab_Qind}")
            and not col.startswith(f"Q{collab_Qind}.1.")
        ]
        all_events = self.df[events_cols].replace("No comments", False).astype(bool)
        all_events["Отказываюсь"] = (~all_events).all(axis=1)
        all_events.columns = new_colnames

        events_counts = {}
        for col in new_colnames:
            events_counts[col] = all_events[col].sum()
        events_counts = pd.Series(events_counts).sort_values(ascending=True).to_dict()
        return events_counts
