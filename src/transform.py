
import os
import time
import dotenv
import asyncio
import nest_asyncio
import pdfplumber
import pandas as pd
from llama_parse import LlamaParse

dotenv.load_dotenv()

def pdf_parser(
        origin_file_path:str, 
        origin_file_name:str,
        target_file_path:str=None,
        target_file_name:str=None,
        llama_cloud_api_key:str="",
        result_type:str="markdown"
):
    try:
        start_time = time.time()
        print(f"Start parsing {origin_file_name} to markdown format")

        parser = LlamaParse(api_key=llama_cloud_api_key, result_type="markdown")

        documents = parser.load_data(os.path.join(origin_file_path, origin_file_name))

        with open(file=os.path.join(target_file_path, target_file_name), mode="w") as f:
            f.write(documents[0].text)

        print(f"Finish parsing {origin_file_name} to markdown format, Time elapsed: {time.time() - start_time}")
        return "success"

    except Exception as e:
        print(f"Error: {origin_file_name} {e}")
        return e
        

def main():

    llama_cloud_api_key_list = [os.environ.get("LLAMA_CLOUD_API_KEY"),
                                os.environ.get("LLAMA_CLOUD_API_KEY1"),
                                os.environ.get("LLAMA_CLOUD_API_KEY2"),
                                os.environ.get("LLAMA_CLOUD_API_KEY3"),
                                os.environ.get("LLAMA_CLOUD_API_KEY4"),
                                os.environ.get("LLAMA_CLOUD_API_KEY5"),
                                os.environ.get("LLAMA_CLOUD_API_KEY6"),
                                os.environ.get("LLAMA_CLOUD_API_KEY7"),
                                os.environ.get("LLAMA_CLOUD_API_KEY8"),
                                os.environ.get("LLAMA_CLOUD_API_KEY9")]

    #  test
    # origin_file_path = "../resources/origin_pdf_directory_2022"
    # target_file_path = "../resources/target_markdown_directory_2022"
    # origin_file_name = "MSFT.OQ_FY2022_Sustainable Development Goals Report 2022.pdf"
    # target_file_name = "MSFT.OQ_FY2022_Sustainable Development Goals Report 2022.md"
    # pdf_parser(origin_file_path, origin_file_name, target_file_path, target_file_name)

    # 2022
    # origin_file_path = "../resources/origin_pdf_directory_2022"
    # target_file_path = "../resources/target_markdown_directory_2022"
    # download_info = pd.read_csv("../resources/download_info.csv")

    # 2023 complete PDF document
    origin_file_path = "../resources/origin_pdf_directory_2023"
    target_file_path = "../resources/target_markdown_directory_2023"
    download_info = pd.read_csv("../resources/download_2023_info.csv")

    # 2023 intercepted pdf document
    origin_file_path = "../resources/intercepted_pdf_directory_2023"
    target_file_path = "../resources/target_intercepted_markdown_directory_2023_bk"
    download_info = pd.read_csv("../resources/download_2023_info.csv")

    total_pages = 0
    num = 0
    download_info["converted_info"] = None
    for i in range(len(download_info)):
        intercept_info = download_info["intercept_info"][i]
        if intercept_info != "success":
            download_info["converted_info"][i] = "can not convert to markdown format"
            continue

        origin_file_name = download_info["file_name"][i]
        target_file_name = origin_file_name.replace(".pdf", ".md")

        downloaded_file_list = os.listdir(target_file_path)
        if target_file_name in downloaded_file_list:
            print(f"{origin_file_name} has been converrted to markdown format")
            continue

        try:
            with pdfplumber.open(os.path.join(origin_file_path, origin_file_name)) as pdf:
                file_pages = len(pdf.pages)

            if file_pages == 0:
                download_info["converted_info"][i] = "No page in the pdf"
                continue
            print(f"The pages of {origin_file_name} is {file_pages}")
            
            total_pages += file_pages
        except Exception as e:
            print(f"Error: {origin_file_name} {e}")
            download_info["converted_info"][i] = e
            continue

        llama_cloud_api_key = llama_cloud_api_key_list[0]
        limit = 1000
        if total_pages > limit:
            print(f"Total pages {total_pages}")
            print(f"Total pages at the end of {origin_file_name} is more than {limit}")
            num += 1
            print(f"num {num}")
            if num >= len(llama_cloud_api_key_list):
                break
            llama_cloud_api_key = llama_cloud_api_key_list[num]
            total_pages = 0

        transform_info = pdf_parser(origin_file_path, origin_file_name, target_file_path, target_file_name, llama_cloud_api_key)
        download_info["converted_info"][i] = transform_info

    download_info.to_csv("../resources/download_2023_info@20240529.csv", index=False)

if __name__ == "__main__":
    main()
