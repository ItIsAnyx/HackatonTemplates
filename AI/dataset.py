import pandas as pd
from fastapi import HTTPException
from config import settings

def read_dataset(file):
    try:
        df = pd.read_csv(file)
        if len(df) > settings.MAX_FILE_ROWS:
            raise HTTPException(status_code=400, detail=f"Too many rows. Max: {settings.MAX_FILE_ROWS}")
        return df

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Извлекается статистическая информация о содержимом датасета - тип, названия столбцов, кол-во пустых, непустых и уникальных элементов. Для числовых считается среднее, мин, макс и медиана
def info_to_str(df: pd.DataFrame) -> dict:
    try:
        total_rows = len(df)
        columns_info = {}

        for col in df.columns:
            columns_info[col] = {
                "dtype": str(df[col].dtype),
                "non_null": int(df[col].notna().sum()),
                "null": int(df[col].isna().sum()),
                "unique": int(df[col].nunique()),
            }
            if str(df[col].dtype) in {"int64", "float64"}:
                columns_info[col]["mean"] = float(df[col].mean().round(4))
                columns_info[col]["min"] = float(df[col].min())
                columns_info[col]["max"] = float(df[col].max())
                columns_info[col]["median"] = float(df[col].median().round(4))

# Итоговый результат с кол-вом строк, стат. информацией о столбцах и 5 примерах строк датасета
        result = {
            "total_rows": total_rows,
            "columns": columns_info,
            "example_strings": df.head(5).to_dict(orient="records")
        }
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))