"""Add classes of data extractors for different surveys/tables/programs here."""

from typing import IO, Dict, List, Tuple

import pandas as pd


class ExitEmbaExtractor:
    """Extracts and organizes data from an Excel table for plotting purposes.
    This class reads a structured .xlsx file and provides methods to extract
    and preprocess data for generating various analytical plots (e.g., distribution charts, trends)
    and calculating some metrics.

    Methods:
        get_age_distr: Returns respondent counts by age group.
        get_industry_distr: Returns distribution of respondents by industry.
        get_job_distr: Returns counts of selected job functions.
        get_overall_csi: Extracts average CSI scores for key program components.
        calulate_csi: Computes overall CSI score from component data.
        get_basic_csi, get_design_csi, get_intern_modules_csi, get_support_csi,
        get_group_csi: Extract CSI data for various program evaluation blocks.
        get_pilos: Aggregates counts of ratings for program learning outcomes.
        get_top_lectors: Counts and ranks lecturer selections.
        get_collaborators: Summarizes alumni collaboration preferences.
        get_programs_nps, get_industry_nps: Return NPS data for programs and industries.
    """

    def __init__(self, table_path: str | IO):
        """Initialize an extractor object

        Args:
            table_path (str | IO): string with a path to a structured Excel tables or a file-like object.
        """
        self.df = pd.read_excel(table_path)

    # below are methods for extracting data, used in piecharts
    def get_age_distr(self, age_Qind: int = 15) -> Dict[str, int]:
        """Returns the distribution of respondents by age group.
        This method extracts responses from a specific question in the table.

        Args:
            age_Qind (int, optional): The index of the question containing age group information. Defaults to 15.

        Returns:
            Dict[str, int]: A dictionary mapping age group labels (e.g., "25-34")
            to the number of respondents in each group.
        """
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

    def get_industry_distr(self, industry_Qind: int = 14) -> Dict[str, int]:
        """Returns the distribution of respondents by industry.
        This method extracts responses from a specific question in the table.

        Args:
            industry_Qind (int, optional): Index of the industry question. Defaults to 14.

        Returns:
            Dict[str, int]: Industry labels mapped to respondent counts.
        """
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

    def get_job_distr(self, job_Qinds: int = 13) -> Dict[str, int]:
        """Returns the distribution of selected job functions.
        This method extracts responses from a specific question in the table.

        Args:
            job_Qinds (int, optional): Index of the job-related question. Defaults to 13.

        Returns:
            Dict[str, int]: Jobs labels mapped to selection counts.
        """
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
    def get_overall_csi(
        self, csi_Qinds: List[int] = [2, 3, 5, 7, 8, 9]
    ) -> Dict[str, pd.Series]:
        """Returns average CSI scores across key program components.
        This method extracts responses from multiple questions in the table.

        Args:
            csi_Qinds (List[int], optional): Question indices for CSI blocks. Defaults to [2, 3, 5, 7, 8, 9].

        Returns:
            Dict[str, pd.Series]: Block labels mapped to per-respondent averages.
        """
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

    def calulate_csi(self, csi_data: Dict[str, List[float]]) -> float:
        """Calculates the overall CSI from component-level CSI data.

        Args:
            csi_data (Dict[str, List[float]]): Average component scores for each section.

        Returns:
            float: Averaged overall CSI score.
        """
        component_csis = []
        for value in list(csi_data.values()):
            component_csis.append(sum(value) / len(value))
        return sum(component_csis) / len(component_csis)

    def _get_csi(self, new_colnames: List[str], csi_Qind: int) -> Dict[str, pd.Series]:
        """Internal helper for extracting CSI block data.

        Args:
            new_colnames (List[str]): New labels for each CSI subquestion.
            csi_Qind (int): Index of the CSI block question.

        Returns:
            Dict[str, pd.Series]: Subquestion labels mapped to rating series.
        """
        csi_cols = [col for col in self.df.columns if col.startswith(f"Q{csi_Qind}")]
        ratings = [self.df[col] for col in csi_cols]
        csi_data = dict(zip(new_colnames, ratings))
        return csi_data

    def get_basic_csi(self, csi_Qind: int = 2) -> Dict[str, pd.Series]:
        """Returns CSI data for the overall csi block.
        This method extracts responses from a specific question in the table.

        Args:
            csi_Qind (int, optional): Question index for this block. Defaults to 2.

        Returns:
            Dict[str, pd.Series]: CSI item labels mapped to rating series.
        """
        new_colnames = [
            "Административная<br>поддержка",
            "Приобретенные<br>знания",
            "ППС",
        ]
        return self._get_csi(new_colnames, csi_Qind)

    def get_design_csi(self, csi_Qind: int = 5) -> Dict[str, pd.Series]:
        """Returns CSI data for the 'Program Design' block.
        This method extracts responses from a specific question in the table.

        Args:
            csi_Qind (int, optional): Question index for this block. Defaults to 5.

        Returns:
            Dict[str, pd.Series]: CSI item labels mapped to rating series.
        """
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

    def get_intern_modules_csi(self, csi_Qind: int = 7) -> Dict[str, pd.Series]:
        """Returns CSI data for the 'International Modules' block.

        Args:
            csi_Qind (int, optional): Question index for this block. Defaults to 7.

        Returns:
            Dict[str, pd.Series]: CSI item labels mapped to rating series.
        """
        new_colnames = [
            "Качество<br>кейсов",
            "Применимость<br>знаний",
            "Групповая<br>работа",
            "Выбор<br>локаций",
        ]
        return self._get_csi(new_colnames, csi_Qind)

    def get_support_csi(self, csi_Qind: int = 8) -> Dict[str, pd.Series]:
        """Returns CSI data for the 'Program Team Support' block.
        This method extracts responses from a specific question in the table.

        Args:
            csi_Qind (int, optional): Question index for this block. Defaults to 8.

        Returns:
            Dict[str, pd.Series]: CSI item labels mapped to rating series.
        """
        new_colnames = [
            "Отклик<br>на потребности",
            "Организация<br>образовательного<br>процесса",
        ]
        return self._get_csi(new_colnames, csi_Qind)

    def get_group_csi(self, csi_Qind: int = 9) -> Dict[str, pd.Series]:
        """Returns CSI data for the 'Group Quality' block.

        Args:
            csi_Qind (int, optional): Question index for this block. Defaults to 9.

        Returns:
            Dict[str, pd.Series]: CSI item labels mapped to rating series.
        """
        new_colnames = [
            "Поддержка\nи взаимопомощь",
            "Опыт и знания\nодногруппников",
            "Разнообразие\nиндустрий",
            "Приобритение\nделовых\nконтактов",
        ]
        return self._get_csi(new_colnames, csi_Qind)

    # below are methods for extracting data, used in barplots
    def _get_program_nps(self, nps_Qind: str = "12.1") -> float:
        """Computes Net Promoter Score (NPS) from the program recommendation question.
        This method extracts responses from a specific question in the table.

        Args:
            nps_Qind (str, optional): Index of the NPS question. Defaults to "12.1".

        Returns:
            float: Calculated NPS value.
        """
        nps_colname = f"Q{nps_Qind}  - 🔴  Готовы ли вы порекомендовать программу своим друзьям/коллегам?"
        num_students = self.df.shape[0]
        num_promoters = self.df[self.df[nps_colname] >= 9].shape[0]
        num_critics = self.df[self.df[nps_colname] <= 6].shape[0]
        nps_value = int((num_promoters - num_critics) / num_students * 100)
        return nps_value

    def get_industry_nps(self) -> Tuple[List[str], List[int], List[str]]:
        """Returns industry-level NPS comparison data for barplot rendering.
        This method extracts responses from a specific question in the table.

        Returns:
            Tuple[List[str], List[int], List[str]]: Labels, values, and color mapping used in a barplot.
        """
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

    def get_programs_nps(self) -> Tuple[List[str], List[int], List[str]]:
        """Returns NPS data comparing different program cohorts.
        This method extracts responses from a specific question in the table.

        Returns:
            Tuple[List[str], List[int], List[str]]: Labels, values, and color mapping used in a barplot.
        """
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

    def get_pilos(self, nps_Qind: str = 3) -> pd.DataFrame:
        """Returns counts of ratings for each PILO (Program Intended Learning Outcome).
        This method extracts responses from a specific question in the table.

        Args:
            nps_Qind (str, optional): Index of the PILO question. Defaults to 3.

        Returns:
            pd.DataFrame: Aggregated rating counts per PILO item.
        """
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
        """Returns a ranked count of most frequently selected lecturers.
        This method extracts responses from a specific question in the table.

        Args:
            lectors_Qind (int, optional): Index of the lecturer evaluation question. Defaults to 6.

        Returns:
            Dict[str, int]: Lecturer names mapped to selection counts.
        """
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
        """Returns the distribution of preferred alumni collaboration formats.

        Args:
            collab_Qind (int, optional): Index of the collaboration question. Defaults to 11.

        Returns:
            Dict[str, int]: Collaboration types mapped to respondent counts.
        """
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
