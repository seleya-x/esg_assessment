
import os
import time
import dotenv
import asyncio
import nest_asyncio
import pdfplumber
import pandas as pd
from llama_parse import LlamaParse


dotenv.load_dotenv()
nest_asyncio.apply()

async def pdf_parser(origin_file_path:str, 
              origin_file_name:str,
              target_file_path:str=None, 
              target_file_name:str=None
):
    try:
        start_time = time.time()
        print(f"Start parsing {origin_file_name} to markdown format")
        llama_cloud_api_key = os.environ.get("LLAMA_CLOUD_API_KEY")

        parser = LlamaParse(api_key=llama_cloud_api_key, result_type="markdown")

        # documents = parser.load_data(os.path.join(origin_file_path, origin_file_name))
        documents = await parser.aload_data(os.path.join(origin_file_path, origin_file_name))

        # print(type(documents[0].text))
        with open(file=os.path.join(target_file_path, target_file_name), mode="w") as f:
            f.write(documents[0].text)

        print(f"Finish parsing {origin_file_name} to markdown format, Time elapsed: {time.time() - start_time}")

    except Exception as e:
        print(f"Error: {origin_file_name} {e}")
        pass
        


async def main():
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

    # 2023
    origin_file_path = "../resources/origin_pdf_directory_2023"
    target_file_path = "../resources/target_markdown_directory_2023"
    download_info = pd.read_csv("../resources/download_2023_info.csv")

    total_pages = 0
    tasks = []
    for i in range(len(download_info)):
        origin_file_name = download_info["file_name"][i]
        if origin_file_name == "No link":
            continue

        target_file_name = origin_file_name.replace(".pdf", ".md")
        downloaded_file_list = os.listdir(target_file_path)
        if target_file_name in downloaded_file_list:
            print(f"{origin_file_name} has been downloaded")
            continue

        try:
            with pdfplumber.open(os.path.join(origin_file_path, origin_file_name)) as pdf:
                file_pages = len(pdf.pages)
            print(f"The pages of {origin_file_name} is {file_pages}")
            total_pages += file_pages
        except Exception as e:
            print(f"Error: {origin_file_name} {e}")
            continue

        limit = 1000
        if total_pages > limit:
            print(f"Total pages at the end of {origin_file_name} is more than {limit}")
            break
        print(f"Total pages {total_pages}")
        
        task_coroutine = pdf_parser(origin_file_path, origin_file_name, target_file_path, target_file_name)
        task_obj = asyncio.create_task(task_coroutine)
        tasks.append(task_obj)

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main(), debug=False)
