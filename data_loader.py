import pandas as pd

def load_sales_data(csv_path):
    df = pd.read_csv(csv_path)
    
    if "Sales" in df.columns:
        df = df.rename(columns={"Sales": "Total"})
        
    df["Total"] = pd.to_numeric(df["Total"])
    return df

def get_categories(df):
    categories = sorted(df["City"].unique())
    return ["Semua Kota"] + categories

def filter_by_category(df, category):
    if category == "Semua Kota":
        return df
    return df[df["City"] == category]

def summarize_data(df):
    summary = df.groupby("Product line", observed=False)["Total"].sum().reset_index()
    summary = summary.sort_values("Total", ascending=False)
    return summary