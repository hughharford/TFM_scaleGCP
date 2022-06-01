import pandas as pd

AWS_BUCKET_PATH = '' #"s3://wagon-public-datasets/taxi-fare-train.csv"
LOCAL_PATH = "raw_data/train_10k.csv"
CLOUD_DATA = True
BUCKET_NAME = 'wagon-data-900-harford'
BUCKET_TRAIN_DATA_PATH = 'data/train_1k.csv'

def get_data(nrows=10_000):
    '''returns a DataFrame with nrows from s3 bucket'''
    if AWS_BUCKET_PATH:
        CSV_path = AWS_BUCKET_PATH
    elif CLOUD_DATA == False:
        CSV_path = LOCAL_PATH
        df = pd.read_csv(CSV_path, nrows=nrows)
    elif CLOUD_DATA == True:
        df = pd.read_csv(f"gs://{BUCKET_NAME}/{BUCKET_TRAIN_DATA_PATH}", nrows=1000)

    return df


def clean_data(df, test=False):
    df = df.dropna(how="any", axis="rows")
    df = df[(df.dropoff_latitude != 0) | (df.dropoff_longitude != 0)]
    df = df[(df.pickup_latitude != 0) | (df.pickup_longitude != 0)]
    if "fare_amount" in list(df):
        df = df[df.fare_amount.between(0, 4000)]
    df = df[df.passenger_count < 8]
    df = df[df.passenger_count >= 0]
    df = df[df["pickup_latitude"].between(left=40, right=42)]
    df = df[df["pickup_longitude"].between(left=-74.3, right=-72.9)]
    df = df[df["dropoff_latitude"].between(left=40, right=42)]
    df = df[df["dropoff_longitude"].between(left=-74, right=-72.9)]
    return df


if __name__ == "__main__":
    df = get_data()
