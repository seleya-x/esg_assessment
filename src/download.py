import os
import pandas as pd
import requests
from tqdm import tqdm
from requests.adapters import HTTPAdapter


def download_file(url, save_path, file_name):

    session = requests.Session()
    session.mount('http://', HTTPAdapter(max_retries=10))
    session.mount('https://', HTTPAdapter(max_retries=10))

    try:
        myfile = session.get(url=url, allow_redirects=True, stream=True, verify=False, timeout=100)

        with open(os.path.join(save_path, file_name), mode="wb") as f:
            f.write(myfile.content)

        return url, file_name, "success"
    
    except requests.exceptions.RequestException as e:
        print(url, e, os.path.join(save_path, file_name))
        return url, file_name, e
    

def dowload_origin():

    # download_res_df = pd.read_csv("../resources/potential_reports_20240530.csv")
    download_res_df = pd.read_csv("../resources/potential_reports_20240611.csv")

    download_res_df= download_res_df.fillna("nan")

    # save_path = "../resources/origin_pdf_directory_2023/"
    # 20240531
    # save_path = "../resources/potential_origin_pdf_directory_2023/"
    # 20240611
    save_path = "../resources/potential_origin_pdf_directory_20240611/"

    download_res_df["download_info"] = None
    download_res_df["link_filename"] = None

    for i in tqdm(range(len(download_res_df))):
        # 2022 ESG Report pdf
        # url = download_res_df["link_2022"][i] if res["link_2022"][i] else None
        # 2023 ESG Report pdf
        # url = download_res_df["link_filename"][i] if res["link_filename"][i] else None
        # 2023 potential reports 20240530
        url = download_res_df["link"][i] if download_res_df["link"][i] else None

        if url is not None and url != "nan":
            file_name = url.split("/")[-1]
            if file_name == "":
                download_res_df.loc[i, "download_info"] = "failed"
                download_res_df.loc[i, "link_filename"] = file_name

            if file_name in os.listdir(save_path):
                download_res_df.loc[i, "download_info"] = "success"
                download_res_df.loc[i, "link_filename"] = file_name
                print(f"{i}, {url}, {file_name} is already downloaded")
                continue
            try:
                url, file_name, info = download_file(url, save_path, file_name)
                print(f"{i}, {url}, {file_name} is downloaded {info}")
            except Exception as e:
                print(i, e, url, os.path.join(save_path, file_name))

            download_res_df.loc[i, "download_info"] = info
            download_res_df.loc[i, "link_filename"] = file_name
        else:
            download_res_df.loc[i, "download_info"] = "No link"
            download_res_df.loc[i, "link_filename"] = "No link"
            print(i, url)

    # download_res_df.to_csv("../resources/potential_download_2023_info.csv", index=False)
    download_res_df.to_csv("../resources/potential_download_20240611_info.csv", index=False)    

def redownload():
    input_pdf_path = "../resources/potential_origin_pdf_directory_2023"
    download_info = pd.read_csv("../resources/potential_intercept_2023_info.csv")


    for i in tqdm(range(307, len(download_info))):
        url = download_info["link"][i]
        file_name = str(url).split("/")[-1]
        if download_info["intercept_info"][i] != "success":
            print(f"{file_name} is not downloaded")
            try:
                url, file_name, info = download_file(url, input_pdf_path, file_name)
            except Exception as e:
                print(url, e, os.path.join(input_pdf_path, file_name))

            download_info.loc[i, "download_info"] = info
            download_info.loc[i, "link_filename"] = file_name

    download_info.to_csv("../resources/potential_download_2023_info.csv", index=False)
     
if __name__ == "__main__":
    dowload_origin()
    # redownload()
