
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

    except Exception as e:
        print(f"Error: {source_file} {e}")

        if os.path.exists(src):
            # 执行复制操作
            shutil.copy(src, dst)
            print(f"文件已从 {src} 复制到 {dst}")
        else:
            print(f"源文件 {src} 不存在")


if __name__== "__main__":

    # 2022
    # input_pdf_path = "../resources/origin_pdf_directory_2022"
    # output_pdf_path = "../resources/extracted_pdf_directory_2022"
    # download_info = pd.read_csv("../resources/download_info.csv")

    # 2023
    input_pdf_path = "../resources/origin_pdf_directory_2023"
    output_pdf_path = "../resources/intercepted_pdf_directory_2023"
    download_info = pd.read_csv("../resources/download_2023_info.csv")

    for i in tqdm(range(len(download_info))):
        input_pdf_name = download_info["file_name"][i]
        output_pdf_name = input_pdf_name.replace(".pdf", "_intercepted.pdf")
        intercept_pdf(input_pdf_path, input_pdf_name, output_pdf_path, output_pdf_name, pages_to_extract=[0,1,2,3,4,5, 6, 7, 8, 9])