import os
import time
import dotenv
import asyncio
import nest_asyncio
import pdfplumber
import pandas as pd
from tqdm import tqdm
from llama_parse import LlamaParse


dotenv.load_dotenv()
nest_asyncio.apply()


async def pdf_parser(
        index:int,
        origin_file_path:str, 
        origin_file_name:str,
        target_file_path:str=None,
        target_file_name:str=None,
        llama_cloud_api_key:str=os.environ.get("LLAMA_CLOUD_API_KEY")
):
    """
    Parse a PDF file to markdown format using LlamaParse API.

    Args:
        index (int): The index of the file being parsed.
        origin_file_path (str): The path to the directory containing the PDF file.
        origin_file_name (str): The name of the PDF file.
        target_file_path (str, optional): The path to the directory where the parsed markdown file will be saved. Defaults to None.
        target_file_name (str, optional): The name of the parsed markdown file. Defaults to None.
        llama_cloud_api_key (str, optional): The API key for accessing the LlamaParse API. Defaults to the value of the "LLAMA_CLOUD_API_KEY" environment variable.

    Returns:
        tuple: A tuple containing the index of the file and a status message indicating the result of the parsing operation.
    """
    try:
        start_time = time.time()
        # print(f"Start parsing {origin_file_name} to markdown format using {llama_cloud_api_key}...")
        parser = LlamaParse(api_key=llama_cloud_api_key, result_type="markdown")
        
        documents = await parser.aload_data(os.path.join(origin_file_path, origin_file_name))
        
        if documents[0].text == "":
            # pdf文件没有文本，不进行保存操作
            return index, "No text in the pdf"
        else:
            with open(file=os.path.join(target_file_path, target_file_name), mode="w") as f:
                f.write(documents[0].text)
            # print(f"Finish parsing {origin_file_name} to markdown format, Time elapsed: {time.time() - start_time}")
            return index, "success"
            
    except Exception as e:
        print(f"Error: {origin_file_name} {e}, {llama_cloud_api_key}")
        return index, e


async def esg_convert():
    """
    Main function to parse PDF files to markdown format using LlamaParse API.
    """
    # llama_cloud_api_key_list = [os.environ.get("LLAMA_CLOUD_API_KEY10"),
    #                             os.environ.get("LLAMA_CLOUD_API_KEY11"),
    #                             os.environ.get("LLAMA_CLOUD_API_KEY12"),
    #                             os.environ.get("LLAMA_CLOUD_API_KEY13"),
    #                             os.environ.get("LLAMA_CLOUD_API_KEY14"),
    #                             os.environ.get("LLAMA_CLOUD_API_KEY15"),
    #                             os.environ.get("LLAMA_CLOUD_API_KEY16"),
    #                             os.environ.get("LLAMA_CLOUD_API_KEY17"),
    #                             os.environ.get("LLAMA_CLOUD_API_KEY18"),
    #                             os.environ.get("LLAMA_CLOUD_API_KEY19")]
    
    llama_cloud_api_key_list = [os.environ.get("LLAMA_CLOUD_API_KEY1"),
                                os.environ.get("LLAMA_CLOUD_API_KEY2"), 
                                os.environ.get("LLAMA_CLOUD_API_KEY3"),
                                os.environ.get("LLAMA_CLOUD_API_KEY4"), 
                                os.environ.get("LLAMA_CLOUD_API_KEY5"),
                                os.environ.get("LLAMA_CLOUD_API_KEY6"), 
                                os.environ.get("LLAMA_CLOUD_API_KEY7"),
                                os.environ.get("LLAMA_CLOUD_API_KEY8"), 
                                os.environ.get("LLAMA_CLOUD_API_KEY9"),
                                os.environ.get("LLAMA_CLOUD_API_KEY10"),
                                os.environ.get("LLAMA_CLOUD_API_KEY11"),
                                os.environ.get("LLAMA_CLOUD_API_KEY12"),
                                os.environ.get("LLAMA_CLOUD_API_KEY13"),
                                os.environ.get("LLAMA_CLOUD_API_KEY14"),
                                os.environ.get("LLAMA_CLOUD_API_KEY15"),
                                os.environ.get("LLAMA_CLOUD_API_KEY16"),
                                os.environ.get("LLAMA_CLOUD_API_KEY17"),
                                os.environ.get("LLAMA_CLOUD_API_KEY18"),
                                os.environ.get("LLAMA_CLOUD_API_KEY19")]

    # 2022
    # origin_file_path = "../resources/origin_pdf_directory_2022"
    # target_file_path = "../resources/target_markdown_directory_2022"
    # download_info = pd.read_csv("../resources/download_info.csv")

    # 2023
    # origin_file_path = "../resources/origin_pdf_directory_2023"
    # target_file_path = "../resources/target_markdown_directory_2023"
    # download_info = pd.read_csv("../resources/download_2023_info.csv")

    # # 2023 intercepted
    # origin_file_path = "../resources/intercepted_pdf_directory_2023"
    # target_file_path = "../resources/target_intercepted_markdown_directory_2023_test"
    # # download_intercept_info = pd.read_csv("../resources/reports_assessment_2023_intercepted_result@0530.csv")
    # download_intercept_info = pd.read_csv("../resources/download_intercept_2023_info.csv")

    # 2023 potential intercepted
    # origin_file_path = "../resources/potential_intercepted_origin_pdf_directory_2023"
    # target_file_path = "../resources/potential_markdown_directory_2023"
    # download_intercept_info = pd.read_csv("../resources/potential_intercept_2023_info.csv")
    
    # 20240612 
    # origin_file_path = "../resources/potential_intercepted_pdf_directory_20240611"
    # target_file_path = "../resources/potential_markdown_directory_20240611"
    # convert_info = "../resources/potential_convert_20240611_info.csv"
    # intercept_info_file = "../resources/potential_intercept_20240611_info.csv"
    
    # 20240626 
    # origin_file_path = "../resources/potential_intercepted_pdf_directory_20240625"
    # target_file_path = "../resources/potential_markdown_directory_20240625"
    # convert_info_file = "../resources/potential_convert_20240625_info.csv"
    # intercept_info_file = "../resources/potential_intercept_20240625_info.csv"
    
    # 20240723 
    # origin_file_path = "../resources/potential_origin_intercept_pdf_directory_20240723"
    # target_file_path = "../resources/potential_origin_markdown_directory_20240723"
    # intercept_info_file = "../resources/potential_intercept_20240723_info.csv"
    # convert_info_file = "../resources/potential_convert_20240723_info.csv"
    
    # 20240926
    origin_file_path = "../resources/potential_origin_intercept_pdf_directory_20240927"
    target_file_path = "../resources/potential_origin_markdown_directory_20240927"
    intercept_info_file = "../resources/potential_intercept_20240927_info.csv"
    convert_info_file = "../resources/potential_convert_20240927_info.csv"
    
    download_intercept_info = pd.read_csv(intercept_info_file)
    num = 0
    total_pages = 0
    tasks = []
    download_intercept_info["converted_info"] = None
    llama_cloud_api_key = llama_cloud_api_key_list[0]
    limit = 1000
    
    if not os.path.exists(target_file_path):
        os.makedirs(target_file_path)
        print(f"文件夹'{target_file_path}'已创建。")
    else:
        print(f"文件夹'{target_file_path}'已存在。")    
    
    for i in tqdm(range(len(download_intercept_info))):
        intercept_info = download_intercept_info["intercept_info"][i]
        if intercept_info != "success":
            # 截取失败的数据不进行转换
            # download_intercept_info["converted_info"][i] = "convert failed"
            download_intercept_info.loc[i, "converted_info"] = "convert failed"
            continue

        # origin_file_name = download_intercept_info["file_name"][i]
        # origin_file_name = download_intercept_info["link"][i].split("/")[-1]
        origin_file_name = download_intercept_info["link_filename"][i]
        
        if origin_file_name.endswith('.PDF'):
            origin_file_name = origin_file_name.replace(".PDF", ".pdf")

        # 解决后缀缺失的问题
        if origin_file_name.endswith('.pdf') is False:
            origin_file_name = origin_file_name + ".pdf"

        target_file_name = origin_file_name.replace(".pdf", ".md")

        if target_file_name in os.listdir(target_file_path):
            # 已经转换过的pdf不再转换
            # print(f"{origin_file_name} has been converrted to markdown format")
            download_intercept_info.loc[i, "converted_info"] = "success"
            continue

        try:
            with pdfplumber.open(os.path.join(origin_file_path, origin_file_name)) as pdf:
                file_pages = len(pdf.pages)
            if file_pages == 0:
                # pdf文件没有页数，不进行转换
                download_intercept_info.loc[i, "converted_info"] = "No page in the pdf"

                continue
            # print(f"The pages of {origin_file_name} is {file_pages}")
            total_pages += file_pages

        except Exception as e:
            print(f"Error: {origin_file_name} {e}")
            download_intercept_info.loc[i, "converted_info"] = e
            continue

        if total_pages > limit:
            # print(f"Total pages {total_pages}")
            # print(f"Total pages at the end of {origin_file_name} is more than {limit}")
            # 超过1000页，切换到下一个api key
            num += 1
            if num >= len(llama_cloud_api_key_list):
                # 超过api key的数量，退出
                break
            print(f"num: {num}, llama_cloud_api_key: {llama_cloud_api_key_list[num]}")
            llama_cloud_api_key = llama_cloud_api_key_list[num]
            total_pages = file_pages

        task_coroutine = pdf_parser(i, 
                                    origin_file_path, 
                                    origin_file_name, 
                                    target_file_path, 
                                    target_file_name, 
                                    llama_cloud_api_key)
        task_obj = asyncio.create_task(task_coroutine)
        tasks.append(task_obj)

    results = await asyncio.gather(*tasks)
    for index, result in results:
        download_intercept_info.loc[index, 'converted_info'] = result
        
    download_intercept_info.to_csv(convert_info_file, index=False)

    
async def convert_annual():
    """
    Main function to convert PDF files to markdown format using LlamaParse API.
    """
    llama_cloud_api_key_list = [os.environ.get("LLAMA_CLOUD_API_KEY1"),
                                os.environ.get("LLAMA_CLOUD_API_KEY2"), 
                                os.environ.get("LLAMA_CLOUD_API_KEY3"),
                                os.environ.get("LLAMA_CLOUD_API_KEY4"), 
                                os.environ.get("LLAMA_CLOUD_API_KEY5"),
                                os.environ.get("LLAMA_CLOUD_API_KEY6"), 
                                os.environ.get("LLAMA_CLOUD_API_KEY7"),
                                os.environ.get("LLAMA_CLOUD_API_KEY8"), 
                                os.environ.get("LLAMA_CLOUD_API_KEY9"),
                                os.environ.get("LLAMA_CLOUD_API_KEY10"),
                                os.environ.get("LLAMA_CLOUD_API_KEY11"),
                                os.environ.get("LLAMA_CLOUD_API_KEY12"),
                                os.environ.get("LLAMA_CLOUD_API_KEY13"),
                                os.environ.get("LLAMA_CLOUD_API_KEY14"),
                                os.environ.get("LLAMA_CLOUD_API_KEY15"),
                                os.environ.get("LLAMA_CLOUD_API_KEY16"),
                                os.environ.get("LLAMA_CLOUD_API_KEY17"),
                                os.environ.get("LLAMA_CLOUD_API_KEY18"),
                                os.environ.get("LLAMA_CLOUD_API_KEY19")]
    
    # 20240626 
    # origin_file_path = "../resources/potential_intercepted_annual_pdf_directory_20240709"
    # target_file_path = "../resources/potential_annual_markdown_directory_20240709"
    # convert_info = "../resources/potential_convert_annual_20240709_info.csv"
    # download_intercept_info = pd.read_csv("../resources/potential_intercept_annual_20240709_info.csv")
    
    origin_file_path = "../resources/potential_intercepted_annual_pdf_directory_20240716"
    target_file_path = "../resources/potential_annual_markdown_directory_20240716"
    convert_info = "../resources/potential_convert_annual_20240716_info.csv"
    download_intercept_info = pd.read_csv("../resources/potential_intercept_annual_20240716_info.csv")

    num = 0
    total_pages = 0
    tasks = []
    download_intercept_info["converted_info"] = None
    llama_cloud_api_key = llama_cloud_api_key_list[0]
    limit = 1000
    
    for i in tqdm(range(len(download_intercept_info))):
        intercept_info = download_intercept_info["intercept_info"][i]
        if intercept_info != "success":
            # 截取失败的数据不进行转换
            # download_intercept_info["converted_info"][i] = "convert failed"
            download_intercept_info.loc[i, "converted_info"] = "convert failed"
            continue

        # origin_file_name = download_intercept_info["file_name"][i]
        origin_file_name = download_intercept_info["link_pdf"][i].split("/")[-1]
        
        if origin_file_name.endswith('.PDF'):
            origin_file_name = origin_file_name.replace(".PDF", ".pdf")

        # 解决后缀缺失的问题
        if origin_file_name.endswith('.pdf') is False:
            origin_file_name = origin_file_name + ".pdf"

        target_file_name = origin_file_name.replace(".pdf", ".md")

        if target_file_name in os.listdir(target_file_path):
            # 已经转换过的pdf不再转换
            # print(f"{origin_file_name} has been converrted to markdown format")
            download_intercept_info.loc[i, "converted_info"] = "success"
            continue

        try:
            with pdfplumber.open(os.path.join(origin_file_path, origin_file_name)) as pdf:
                file_pages = len(pdf.pages)
            if file_pages == 0:
                # pdf文件没有页数，不进行转换
                download_intercept_info.loc[i, "converted_info"] = "No page in the pdf"

                continue
            # print(f"The pages of {origin_file_name} is {file_pages}")
            total_pages += file_pages

        except Exception as e:
            print(f"Error: {origin_file_name} {e}")
            download_intercept_info.loc[i, "converted_info"] = e
            continue

        if total_pages > limit:
            # print(f"Total pages {total_pages}")
            # print(f"Total pages at the end of {origin_file_name} is more than {limit}")
            # 超过1000页，切换到下一个api key
            num += 1
            if num >= len(llama_cloud_api_key_list):
                # 超过api key的数量，退出
                break
            print(f"num: {num}, llama_cloud_api_key: {llama_cloud_api_key_list[num]}")
            llama_cloud_api_key = llama_cloud_api_key_list[num]
            total_pages = file_pages

        task_coroutine = pdf_parser(i, origin_file_path, origin_file_name, 
                                    target_file_path, target_file_name, llama_cloud_api_key)
        task_obj = asyncio.create_task(task_coroutine)
        tasks.append(task_obj)

    results = await asyncio.gather(*tasks)
    for index, result in results:
        download_intercept_info.loc[index, 'converted_info'] = result
        
    download_intercept_info.to_csv(convert_info, index=False)
    
    
async def convert_pdf(report_list):
    """
    Main function to convert PDF files to markdown format using LlamaParse API.
    """
    llama_cloud_api_key_list = [os.environ.get("LLAMA_CLOUD_API_KEY1"),
                                os.environ.get("LLAMA_CLOUD_API_KEY2"), 
                                os.environ.get("LLAMA_CLOUD_API_KEY3"),
                                os.environ.get("LLAMA_CLOUD_API_KEY4"), 
                                os.environ.get("LLAMA_CLOUD_API_KEY5"),
                                os.environ.get("LLAMA_CLOUD_API_KEY6"), 
                                os.environ.get("LLAMA_CLOUD_API_KEY7"),
                                os.environ.get("LLAMA_CLOUD_API_KEY8"), 
                                os.environ.get("LLAMA_CLOUD_API_KEY9"),
                                os.environ.get("LLAMA_CLOUD_API_KEY10"),
                                os.environ.get("LLAMA_CLOUD_API_KEY11"),
                                os.environ.get("LLAMA_CLOUD_API_KEY12"),
                                os.environ.get("LLAMA_CLOUD_API_KEY13"),
                                os.environ.get("LLAMA_CLOUD_API_KEY14"),
                                os.environ.get("LLAMA_CLOUD_API_KEY15"),
                                os.environ.get("LLAMA_CLOUD_API_KEY16"),
                                os.environ.get("LLAMA_CLOUD_API_KEY17"),
                                os.environ.get("LLAMA_CLOUD_API_KEY18"),
                                os.environ.get("LLAMA_CLOUD_API_KEY19")]
    
    num = 0
    total_pages = 0
    tasks = []
    llama_cloud_api_key = llama_cloud_api_key_list[0]
    limit = 1000
    
    origin_file_path = "../resources/20240829/"
    target_file_path = "../resources/20240829/"
    
    for i in tqdm(range(len(report_list))):
        origin_file_name = report_list[i]
        target_file_name = report_list[i].replace(".pdf", ".md")
        
        try:
            with pdfplumber.open(os.path.join(origin_file_path, origin_file_name)) as pdf:
                file_pages = len(pdf.pages)
            if file_pages == 0:
                # pdf文件没有页数，不进行转换
                download_intercept_info.loc[i, "converted_info"] = "No page in the pdf"

                continue
            # print(f"The pages of {origin_file_name} is {file_pages}")
            total_pages += file_pages

        except Exception as e:
            print(f"Error: {origin_file_name} {e}")
            download_intercept_info.loc[i, "converted_info"] = e
            continue

        if total_pages > limit:
            # print(f"Total pages {total_pages}")
            # print(f"Total pages at the end of {origin_file_name} is more than {limit}")
            # 超过1000页，切换到下一个api key
            num += 1
            if num >= len(llama_cloud_api_key_list):
                # 超过api key的数量，退出
                break
            print(f"num: {num}, llama_cloud_api_key: {llama_cloud_api_key_list[num]}")
            llama_cloud_api_key = llama_cloud_api_key_list[num]
            total_pages = file_pages

        task_coroutine = pdf_parser(i, origin_file_path, origin_file_name, target_file_path, target_file_name, llama_cloud_api_key)
        task_obj = asyncio.create_task(task_coroutine)
        tasks.append(task_obj)

    results = await asyncio.gather(*tasks)



if __name__ == "__main__":
    asyncio.run(esg_convert(), debug=False)
    # asyncio.run(convert_annual(), debug=False)
    # report_list = ["Annual_Report.pdf", "Sustainability_Report.pdf", "Climate_Vision_2050_Report.pdf"]
    # asyncio.run(convert_pdf(report_list), debug=False)
    