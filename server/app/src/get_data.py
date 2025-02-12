import pandas as pd
import os
import opendatasets as od

from kaggle.api.kaggle_api_extended import KaggleApi
api = KaggleApi()
api.authenticate()


def get_data(dataset, filename):
    # Assign the Kaggle data set URL into variable
    dataset = 'https://www.kaggle.com/datasets/kouroshalizadeh/history-of-philosophy'
    # print(filename)
    # download single file
    # Signature: dataset_download_file(dataset, file_name, path=None, force=False, quiet=True)
    # TODO: Get the Dataset URL from user & recursively search page for .csv file
    files = api.dataset_download_files(dataset)
    print("FILES: ", files)

    return files

    # # Using opendatasets let's download the data sets
    # return od.download(dataset)