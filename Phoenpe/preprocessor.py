import re
import pandas as pd
import calendar

def preprocess(df):
    df.rename(columns={"Transaction Statement for 8851084852": "Datetime"}, inplace=True)
    df.rename(columns={"Unnamed: 1": "Name"}, inplace=True)
    df.rename(columns={"Unnamed: 3": "Type"}, inplace=True) 
    df.rename(columns={"Unnamed: 4": "Amount"}, inplace=True)
    df = df.dropna()
    df["Amount"] = df["Amount"].str.replace("INR ", "").astype(float)
    df["Datetime"] = pd.to_datetime(df["Datetime"].str.split("\n").str[0], format="%b %d, %Y")
    def extract_text(row):
        if row["Type"] == "Credit":
            return row["Name"].split("Received from ")[1].split("\n")[0] if "Received from" in row["Name"] else None
        elif row["Type"] == "Debit":
            if "Paid to" in row["Name"]:
                return row["Name"].split("Paid to ")[1].split("\n")[0]
            elif "Paid -" in row["Name"]:
                return row["Name"].split("Paid - ")[1].split("\n")[0]
            else:
                return None
        else:
            return None
    df["Name"] = df.apply(extract_text, axis=1)
    df['Year'] = df['Datetime'].dt.year
    df['Month'] = df['Datetime'].dt.month
    df['Month'] = df['Month'].apply(lambda x: calendar.month_name[int(x)])
    df['Date'] = df['Datetime'].dt.day
    df['Day_of_Week'] = df['Datetime'].dt.day_name()
    

    return df