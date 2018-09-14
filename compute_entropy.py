import os
import requests
import zipfile
import pandas as pd
import math

def download_file(url, filename):
    """Download filename from url"""
    print("Downloading {}, from: {}".format(filename, url))
    res = requests.get(url, allow_redirects=True)
    open(filename, "wb").write(res.content)

def unzip_file(filezip, datadir):
    """Unzip provided zipfile into datadir"""
    print("Extracting: {}".format(filezip))
    with zipfile.ZipFile(filezip, "r") as zip_ref:
        zip_ref.extractall(datadir)
    print("{} extracted".format(filezip))

def load_hdb_data(ddir=""):
    """Check if HDB resale file exists, if not, download from data.gov.sg. Returns data as pandas df."""
    url = "https://data.gov.sg/dataset/7a339d20-3c57-4b11-a695-9348adfd7614/download"
    filezip = os.path.join(ddir, "resale-flat-prices.zip")
    datadir = os.path.join(ddir, "resale-flat-prices")
    filename = "resale-flat-prices-based-on-registration-date-from-jan-2015-onwards.csv"
    filepath = os.path.join(datadir, filename)
    if not os.path.exists(filepath):
        print("{} does not exist, checking for zipfile: {}".format(filepath, filezip))
        if not os.path.exists(filezip):
            download_file(url, filezip)
        unzip_file(filezip, datadir)
    print("Reading data from: {}".format(filepath))
    data = pd.read_csv(filepath)
    return data

def load_taxi_data(ddir=""):
    """Check if taxi trip file exists, if not, download from data.cityofnewyork.us. Returns data as pandas df."""
    url = "https://data.cityofnewyork.us/resource/uacg-pexx.json"
    filename = "2016_Yellow_Taxi_Trip_Data.json"
    filepath = os.path.join(ddir, filename)
    if not os.path.exists(filepath):
        download_file(url, filepath)
    print("Reading data from: {}".format(filepath))
    data = pd.read_json(filepath)
    return data

def compute_entropy(data):
    """Compute entropy of data provided.
    
    Args:
      data (list or list-like):  list of categorical data.
      
    Returns:
      float: Computed entropy.
    """
    length = len(data)
    count_dict = {}
    for elem in data:
        count_dict[elem] = count_dict.get(elem, 0) + 1
    
    entropy = 0
    for count in count_dict.values():
        prob = count / float(length)
        entropy += - prob * math.log(prob, 2)
    
    return entropy

def bucketise_data(data, n_buckets):
    """Bucketise provided numeric data into n_buckets of equal width"""
    data = list(data)
    max_v = max(data)
    min_v = min(data)
    increment = float(max_v - min_v) / n_buckets
    buck_thres = [min_v+(i+1)*increment for i in range(n_buckets)]
    data.sort()
    bucket_no = 0
    buck_data = []
    for elem in data:
        if elem <= buck_thres[bucket_no]:
            buck_data.append(bucket_no)
        else:
            bucket_no += 1
    return buck_data

def pd_compute_entropy(df, col, to_bucketise=False, n_buckets=5):
    """Compute entropy of provided column of pandas df.
    
    Args:
      df (pandas.DataFrame): pandas DataFrame.
      col (str): column name of interest.
      to_bucketise (bool): whether to bucketise data. Only for numeric data.
      n_buckets (int): number of buckets to breakdown numeric data.
    
    Returns:
      float: Computed entropy.
    """
    data = df[col]
    if to_bucketise:
        data = bucketise_data(data, n_buckets)
    return compute_entropy(data)

if __name__ == "__main__":
    pass

# use:
# hdb_data = load_hdb_data()
# taxi_data = load_taxi_data()
# compute_entropy(hdb_data["storey_range"])
# pd_compute_entropy(hdb_data, "flat_type")
# pd_compute_entropy(taxi_data, "dropoff_latitude", to_bucketise=True)
# pd_compute_entropy(taxi_data, "payment_type")