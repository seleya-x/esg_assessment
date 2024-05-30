import os
import pandas as pd
import requests
from requests.adapters import HTTPAdapter


def download_file(url, save_path, file_name):

    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=3))
    s.mount('https://', HTTPAdapter(max_retries=3))

    try:
        myfile = s.get(url=url, allow_redirects=True, stream=True, verify=False, timeout=10)

        with open(os.path.join(save_path, file_name), mode="wb") as f:
            f.write(myfile.content)

        return url, file_name, "success"
    
    except requests.exceptions.RequestException as e:
        print(url, e)
        return url, file_name, e


if __name__ == "__main__":

    res = pd.read_excel("../resources/reports_collection_2023.xlsx")
    res= res.fillna("nan")

    # url = res.head()["link_2022"][1]
    # file_name = url.split("/")[-1]
    save_path = "../resources/origin_pdf_directory_2023/"
    # download_file(url, save_path, file_name)

    save_info = []
    file_namme_list = []

    for i in range(len(res)):
        # 2022 ESG Report pdf
        # url = res["link_2022"][i] if res["link_2022"][i] else None
        # 2023 ESG Report pdf
        url = res["link_filename"][i] if res["link_filename"][i] else None

        if url is not None and url != "nan":
            file_name = url.split("/")[-1]
            url, file_name, info = download_file(url, save_path, file_name)
            print(f"{file_name} is downloaded")
            save_info.append(info)
            file_namme_list.append(file_name)
        else:
            save_info.append("No link")
            file_namme_list.append("No link")

    pd.DataFrame({"filename_2023": file_namme_list, "info": save_info}).to_csv("../resources/download_2023_info.csv", index=False)