import os
import pandas as pd

res = pd.read_excel("../resources/reports_collection_2023.xlsx")
res= res.fillna("nan")

# res = pd.read_csv("../resources/download_intercept_2023_info.csv")

origin_pdf_directory_2023 = "../resources/origin_pdf_directory_2023/"

intercepted_pdf_directory_20233 = "../resources/intercepted_pdf_directory_2023/"

target_intercepted_markdown_directory_2023 = "../resources/target_intercepted_markdown_directory_2023"


target_intercepted_markdown_directory_2023_test = "../resources/target_intercepted_markdown_directory_2023_test"

res["download_info"] = None
res["intercept_info"] = None
res["converted_info"] = None

for i in range(len(res)):
    # 2022 ESG Report pdf
    # url = res["link_2022"][i] if res["link_2022"][i] else None
    # 2023 ESG Report pdf
    url = res["link_filename"][i] if res["link_filename"][i] else None

    if url is not None and url != "nan":
        file_name = url.split("/")[-1]
        if file_name in os.listdir(origin_pdf_directory_2023):
            res["download_info"][i] = "success"
        else:
            res["download_info"][i] = "failed"

        if file_name in os.listdir(intercepted_pdf_directory_20233):
            res["intercept_info"][i] = "success"
        else:
            res["intercept_info"][i] = "failed"
        
        if file_name.replace(".pdf", ".md") in os.listdir(target_intercepted_markdown_directory_2023_test):
            res["converted_info"][i] = "success"
        else:
            res["converted_info"][i] = "failed"
        
    else:
        res["download_info"][i] = "nan"
        res["intercept_info"][i] = "nan"
        res["converted_info"][i] = "nan"

res.to_csv("../resources/res.csv", index=False)
