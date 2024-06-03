import os
import pandas as pd
import requests
from tqdm import tqdm
from requests.adapters import HTTPAdapter


def download_file(url, save_path, file_name):

    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=3))
    s.mount('https://', HTTPAdapter(max_retries=3))

    try:
        myfile = s.get(url=url, allow_redirects=True, stream=True, verify=False, timeout=50)

        with open(os.path.join(save_path, file_name), mode="wb") as f:
            f.write(myfile.content)

        return url, file_name, "success"
    
    except requests.exceptions.RequestException as e:
        print(url, e, os.path.join(save_path, file_name))
        return url, file_name, e


if __name__ == "__main__":

    # res = pd.read_excel("../resources/reports_collection_2023.xlsx")
    res = pd.read_csv("../resources/potential_reports_20240530.csv")
    res= res.fillna("nan")

    # url = res.head()["link_2022"][1]
    # file_name = url.split("/")[-1]
    # save_path = "../resources/origin_pdf_directory_2023/"
    save_path = "../resources/potential_origin_pdf_directory_2023/"
    # download_file(url, save_path, file_name)

    res["download_info"] = None
    res["link_filename"] = None

    for i in tqdm(range(len(res))):
        # 2022 ESG Report pdf
        # url = res["link_2022"][i] if res["link_2022"][i] else None
        # 2023 ESG Report pdf
        # url = res["link_filename"][i] if res["link_filename"][i] else None

        # 2023 potential reports 20240530
        print(i)
        url = res["link"][i] if res["link"][i] else None

        if url is not None and url != "nan":
            file_name = url.split("/")[-1]
            if file_name == "":
                res.loc[i, "download_info"] = "failed"
                res.loc[i, "link_filename"] = file_name

            if file_name in os.listdir(save_path):
                # res["download_info"][i] = "success"
                # res["link_filename"][i] = file_name
                res.loc[i, "download_info"] = "success"
                res.loc[i, "link_filename"] = file_name
                print(f"{url}, {file_name} is already downloaded")
                continue
            try:
                url, file_name, info = download_file(url, save_path, file_name)
                print(f"{url}, {file_name} is downloaded {info}")
            except Exception as e:
                print(url, e, os.path.join(save_path, file_name))

            # res["download_info"][i] = info
            # res["link_filename"][i] = file_name
            res.loc[i, "download_info"] = info
            res.loc[i, "link_filename"] = file_name
        else:
            res.loc[i, "download_info"] = "No link"
            res.loc[i, "link_filename"] = "No link"
            # res["download_info"][i] = "No link"
            # res["link_filename"][i] = "No link"

    res.to_csv("../resources/potential_download_2023_info.csv", index=False)