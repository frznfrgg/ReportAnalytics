"""Add classes for processing raw survey tables"""

from io import BytesIO
from typing import IO

import pandas as pd


def process_exit_survey(raw_table: str | IO):
    raw_data = pd.read_excel(raw_table, skiprows=[0, 2, 3])

    service_cols = [col for col in raw_data.columns if col.startswith("S")]
    unnamed_cols = [col for col in raw_data.columns if col.startswith("Unnamed:")]
    cols_to_drop = ["PS0 Start", "PD0 Duration , sec"] + service_cols + unnamed_cols
    raw_data = raw_data.drop(columns=cols_to_drop)

    # drop all rows where participant name is None
    name_col = "Q16  - 🔴 Укажите  фамилию и имя"
    q6_cols = [col for col in raw_data.columns if col.startswith("Q6")]
    raw_data = raw_data.dropna(subset=[name_col], ignore_index=True)

    # if a student doesnt remember any professors
    raw_data[q6_cols] = raw_data[q6_cols].fillna("Никто")

    # if the age was not provided fill with mode
    age_col = "Q15 🔴  Укажите ваш  возраст"
    raw_data[age_col] = raw_data[age_col].fillna(raw_data[age_col].median())

    score_cols = [
        col
        for col in raw_data.columns
        if col.startswith("Q7") or col.startswith("Q8") or col.startswith("Q9")
    ]
    # if a value in scoring col is missing, replace by the mean
    for col in score_cols:
        raw_data[col] = raw_data[col].fillna(int(raw_data[col].mean()))

    free_answer_cols = [
        "Q4.1 Каковы, на ваш взгляд,  сильные и слабые стороны программы? - Сильные стороны",
        "Q4.2 Каковы, на ваш взгляд,  сильные и слабые стороны программы? - Слабые стороны",
        "Q10 Оставьте ваши  пожелания и дополнительные комментарии  по программе",
        "Q10 Оставьте ваши  пожелания и дополнительные комментарии  по программе",
        "Q11.1.O В качестве приглашенного спикера - брендинг, корпфин",
        "Q11.5.O Другое - протагонист кейса",
        "Q13.6.O Другое - Other",
        "Q14.20.O Другое - Other",
    ]
    # set to "No comments" if the answer wasnt provided in cols with free answer
    for col in free_answer_cols:
        raw_data[col] = raw_data[col].fillna("No comments")

    # save to stream
    buf = BytesIO()
    raw_data.to_excel(buf, index=False)
    buf.seek(0)
    return buf
