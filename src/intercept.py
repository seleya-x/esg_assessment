
import os
import pandas as pd
from tqdm import tqdm
from Crypto.Cipher import AES
import shutil
from fitz import Document

def intercept_pdf(source_path, source_file, destination_path, dest_file, pages_to_extract=[0,1,2,3,4,5]):

    src = os.path.join(source_path, source_file)
    dst = os.path.join(destination_path, dest_file)
    try:
        src_doc = Document(src)

        # 创建一个新的PDF文档来保存提取的页面
        dest_doc = Document()

        total_pages = src_doc.page_count
        if  total_pages == 0:
            return "No page in the pdf"

        if max(pages_to_extract) > total_pages:
            pages_to_extract = [page for page in pages_to_extract if page <= total_pages]

        # 遍历要提取的页面
        for page_num in pages_to_extract:
            # 插入页面到新文档中
            dest_doc.insert_pdf(src_doc, from_page=page_num, to_page=page_num)

        # 保存新文档
        dest_doc.save(dst)
        # 关闭文档
        src_doc.close()
        dest_doc.close()

        return "success"

    except Exception as e:
        print(f"Error: {source_file} {e}")

        return e

if __name__== "__main__":

    # 2022
    # input_pdf_path = "../resources/origin_pdf_directory_2022"
    # output_pdf_path = "../resources/extracted_pdf_directory_2022"
    # download_info = pd.read_csv("../resources/download_info.csv")

    # 2023
    input_pdf_path = "../resources/origin_pdf_directory_2023"
    output_pdf_path = "../resources/intercepted_pdf_directory_2023"
    download_info = pd.read_csv("../resources/download_2023_info.csv")

    download_info["intercept_info"] = None
    for i in tqdm(range(len(download_info))):
        input_pdf_name = download_info["file_name"][i]
        if input_pdf_name == "No link":
            download_info["intercept_info"][i] = "No link"
            continue
        # output_pdf_name = input_pdf_name.replace(".pdf", "_intercepted.pdf")
        intercept_info = intercept_pdf(input_pdf_path, input_pdf_name, output_pdf_path, dest_file=input_pdf_name, pages_to_extract=[0,1,2,3,4,5, 6, 7, 8, 9])
        download_info["intercept_info"][i] = intercept_info

    download_info.to_csv("../resources/download_2023_info.csv", index=False)