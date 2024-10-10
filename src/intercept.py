
import os
import pandas as pd
from tqdm import tqdm
# from Crypto.Cipher import AES
import shutil
from fitz import Document
import PyPDF2

def is_pdf_by_extension(file_path):
    _, file_extension = os.path.splitext(file_path)
    return file_extension.lower() == '.pdf'


def intercept_pdf_(source_path, source_file, destination_path, dest_file, pages_to_extract=[0,1,2,3,4,5,6,7,8,9]):

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
        

def intercept_pdf(source_path, source_file, dest_path, dest_file, max_pages=10):

    try:
        with open(os.path.join(source_path, source_file), 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            
            # 创建分割后的 PDF 文件的 writer
            writer = PyPDF2.PdfWriter()
            for i, page in enumerate(reader.pages):
                if i >= max_pages:
                    break
                writer.add_page(page)
            
        with open(os.path.join(dest_path, dest_file), 'wb') as output_pdf:
            writer.write(output_pdf) 
        return "success"

    except Exception as e:
        print(f"Error: {source_file} {e}")
        return e
    

def pdf_pages(source_path, source_file):

    try:
        with open(os.path.join(source_path, source_file), 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            return len(reader.pages)

    except Exception as e:
        print(f"Error: {source_file} {e}")
        return e
   
    
def pdf_pages_(source_path, source_file):

    src = os.path.join(source_path, source_file)
    try:
        src_doc = Document(src)
        total_pages = src_doc.page_count
        if  total_pages == 0:
            return "No page in the pdf"

        # 关闭文档
        src_doc.close()
        return total_pages

    except Exception as e:
        print(f"Error: {source_file} {e}")
        return e
    

def intercept_esg_pdf():

    # 20240530 potential
    # input_pdf_path = "../resources/potential_origin_pdf_directory_2023"
    # output_pdf_path = "../resources/potential_intercepted_origin_pdf_directory_2023_test"
    # download_info = pd.read_csv("../resources/potential_download_2023_info.csv")
    
    # 20240612 
    # input_pdf_path = "../resources/potential_origin_pdf_directory_20240611"
    # output_pdf_path = "../resources/potential_intercepted_pdf_directory_20240611"
    # download_info = pd.read_csv("../resources/potential_download_20240611_info.csv")
    
    # 20240626 
    # input_pdf_path = "../resources/potential_origin_pdf_directory_20240625"
    # output_pdf_path = "../resources/potential_intercepted_pdf_directory_20240625"
    # download_info = pd.read_csv("../resources/potential_download_20240625_info.csv")
    # intercept_info_path ="../resources/potential_intercept_20240625_info.csv"
    
    # 20240723
    # input_pdf_path = "../resources/potential_origin_pdf_directory_20240723"
    # output_pdf_path = "../resources/potential_origin_intercept_pdf_directory_20240723"
    # download_info = pd.read_csv("../resources/potential_download_20240723_info.csv")
    # intercept_info_path ="../resources/potential_intercept_20240723_info.csv"
    
    # 20240927
    input_pdf_path = "../resources/potential_origin_pdf_directory_20240927"
    output_pdf_path = "../resources/potential_origin_intercept_pdf_directory_20240927"
    download_info = pd.read_csv("../resources/potential_download_20240927_info.csv")
    intercept_info_path ="../resources/potential_intercept_20240927_info.csv"
    
    if not os.path.exists(output_pdf_path):
        os.makedirs(output_pdf_path)
        print(f"文件夹'{output_pdf_path}'已创建。")
    else:
        print(f"文件夹'{output_pdf_path}'已存在。")

    index = 0
    for i in tqdm(range(len(download_info))):
        # input_pdf_name = str(download_info["link"][i]).split("/")[-1]
        input_pdf_name = download_info["link_filename"][i]

        output_file = input_pdf_name
        if input_pdf_name == "No link":
            download_info.loc[i, "intercept_info"] = "No link"
            continue  
        
        if input_pdf_name == "":
            download_info.loc[i, "intercept_info"] = "url error"
            continue
    
        if input_pdf_name in os.listdir(output_pdf_path):
            download_info.loc[i, "intercept_info"] = "success"
            continue

        if input_pdf_name not in os.listdir(input_pdf_path):
            download_info.loc[i, "intercept_info"] = "not download yet"
            continue

        # .PDF, change to .pdf
        if output_file.endswith('.PDF'):
            output_file = input_pdf_name.replace(".PDF", ".pdf")

        # 解决后缀缺失的问题
        if output_file.endswith('.pdf') is False:
            output_file = output_file + ".pdf"
            download_info.loc[i, "link_filename"] = output_file

        # print(f"input_pdf_name: {input_pdf_name}, output_file {output_file}")

        # intercept_info = intercept_pdf(input_pdf_path, input_pdf_name, output_pdf_path, output_file)
        intercept_info = intercept_pdf(input_pdf_path, input_pdf_name, output_pdf_path, output_file)

        if intercept_info != "success":
            index +=1

        download_info.loc[i, "intercept_info"]  = intercept_info

    print(index)

    # download_info.to_csv("../resources/potential_intercept_20240611_info.csv", index=False)
    download_info.to_csv(intercept_info_path, index=False) 
    
    
def intercept_annual_pdf():
    
    # 20240709
    # input_pdf_path = "../resources/potential_annual_pdf_directory_20240709"
    # output_pdf_path = "../resources/potential_intercepted_annual_pdf_directory_20240709"
    # download_info = pd.read_csv("../resources/potential_annual_download_20240709_info.csv")
    # intercept_info_path = "../resources/potential_intercept_annual_20240709_info.csv"
    
    # 20240716
    input_pdf_path = "../resources/potential_annual_pdf_directory_20240716"
    output_pdf_path = "../resources/potential_intercepted_annual_pdf_directory_20240716"
    download_info = pd.read_csv("../resources/potential_annual_download_20240716_info.csv")
    intercept_info_path = "../resources/potential_intercept_annual_20240716_info.csv"

    if not os.path.exists(output_pdf_path):
        os.makedirs(output_pdf_path)
        print(f"文件夹'{output_pdf_path}'已创建。")
    else:
        print(f"文件夹'{output_pdf_path}'已存在。")
        
    index = 0
    for i in tqdm(range(len(download_info))):
        input_pdf_name = str(download_info["link_pdf"][i]).split("/")[-1]
        
        output_file = input_pdf_name
        if input_pdf_name == "No link":
            download_info.loc[i, "intercept_info"] = "No link"
            continue  
        
        if input_pdf_name == "":
            download_info.loc[i, "intercept_info"] = "url error"
            continue
    
        if input_pdf_name in os.listdir(output_pdf_path):
            download_info.loc[i, "intercept_info"] = "success"
            continue

        if input_pdf_name not in os.listdir(input_pdf_path):
            download_info.loc[i, "intercept_info"] = "not download yet"
            continue

        # .PDF, change to .pdf
        if output_file.endswith('.PDF'):
            output_file = input_pdf_name.replace(".PDF", ".pdf")

        # 解决后缀缺失的问题
        if output_file.endswith('.pdf') is False:
            output_file = output_file + ".pdf"
            download_info.loc[i, "link_filename"] = output_file

        # print(f"input_pdf_name: {input_pdf_name}, output_file {output_file}")

        intercept_info = intercept_pdf(input_pdf_path, input_pdf_name, output_pdf_path, output_file)

        if intercept_info != "success":
            index +=1

        download_info.loc[i, "intercept_info"]  = intercept_info

    print(index)
    download_info.to_csv(intercept_info_path, index=False) 

if __name__== "__main__":
    intercept_esg_pdf()
    # intercept_annual_pdf()

   