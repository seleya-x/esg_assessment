import os
import re
import sys
import json
import openai
import dotenv
from tqdm import tqdm
import pandas as pd
from intercept import pdf_pages

dotenv.load_dotenv()

endpoint = os.environ.get("OPENAI_API_ENDPOINT")
api_key = os.environ.get("OPENAI_API_KEY")
api_version = os.environ.get("OPENAI_API_VERSION")
api_type = os.environ.get("OPENAI_API_TYPE")


def llm_parser(chat_type:str, 
               documents:str, 
               time:str=None, 
               company_name:str=None, 
               document_title:str=None,
               llm_model:str="gpt-4o"):

    if chat_type == "title_extraction":
        instruction = "The following is a document written by a company. The document is written in markdown format. Please provide the title of the document.Please output the above answer with the JSON format:{\"title\":\"xxxx\"}"
    
        messages = [
            {
                "role": "system",
                "content": "You are an artificial intelligence assistant, and you are better at Chinese and English conversations. You will provide users with safe, helpful, and accurate answers. At the same time, you will reject all answers related to terrorism, racial discrimination, yellow violence, and other issues.",
            },
            {
                "role": "user", 
                "content": instruction},
        ]

    elif chat_type == "esg_assessment":
        # 0629
        # instruction = "The ESG report title for %s is \"%s\". Please answer the following questions based on the information in the above documents: \
        #                 \n\t1. What is the title of the current document? \
        #                 \n\t2. Verify if the document's corporate entity is the same company as %s\
        #                 \n\t3. Ignore the time in the title and give a similarity score between the given ESG report title and the current document title. The total score is 10 points, with 0 being the lowest and 10 being the highest. \
        #                 \n\t4. Ignore the time factor and rate the overlap between the current document and the provided title? The total score is 10 points, with 0 being the lowest and 10 being the highest. \
        #                 \n\t5. Based on the similarity between the current document title and the provided ESG report title for %s as well as the content of the current document, \
        #                     infer that whether the ESG report framework used in the current document is consistent with the ESG report framework for %s? Exclude news trailers and other news. \
        #                     If so, please output the corporate entity and fiscal year of the above document. If not, it is not necessary to output. \
        #             \nPlease output the above answers in JSON format and no need to use markdown syntax to encapsulate JSON string into Code Block.\
        #             \nYou can refer to the following output examples: \
        #                     \n\t1）{\"title\": \"xxx\", \"company_match\": \"True\",\"title_similarity\": 10, \"similarity\": 10, \"is_ESG\": \"yes\", \"corporate_entity\": \"xxxx\", \"fiscal_year\": \"xxxx\"} \
        #                     \n\t2）{\"title\": \"xxx\", \"company_match\": \"False\",\"title_similarity\": 3, \"similarity\": 2, \"is_ESG\": \"no\"}"% (company_name, document_title, company_name, company_name, company_name)
        
        instruction = "ESG reports disclose environmental, social and corporate governance data aiming to expose a company’s risk profile to investors. These reports focus more on the relationship between the internal work on the environment, social and governmental structure and the overall output of the company.\
            \n ESG report is on a company’s internal structure leading to its output. The three focuses of ESG reporting are:\
            \n\t 1) Environment – corporate climate policies, energy use, waste, pollution, natural resource conservation, treatment of animals, and a company’s environmental risks.\
            \n\t 2) Social – relationship with the stakeholders, including employees, customers, suppliers and investors.\
            \n\t 3) Governance – how the board of directors manages factors such as the interests of the company’s stakeholders and government policy when making decisions.\
            \n The ESG report title for %s is \"%s\". Please answer the following questions based on the information in the above documents: \
            \n\t 1. What is the title of the current document? \
            \n\t 2. Verify the corporate entity if same as %s, if %s does not have country and corporate entity has country, they are not the same entity. \
            \n\t 3. Ignore the time in the title and give a similarity score between the given ESG report title and the current document title. The total score is 10 points, with 0 being the lowest and 10 being the highest. \
            \n\t 4. Ignore the time factor and rate the overlap between the current document and the provided title? The total score is 10 points, with 0 being the lowest and 10 being the highest. \
            \n\t 5. Based on the similarity between the current document title and the provided ESG report title for %s as well as the content of the current document, infer that whether the ESG report framework used in the current document is consistent with the ESG report framework for %s? Exclude news trailers and other news. If so, please output the corporate entity and fiscal year of the above document. If not, it is not necessary to output. \
            \n Please output the above answers in JSON format and no need to use markdown syntax to encapsulate JSON string into Code Block.\
            \n You can refer to the following output examples: \
            \n\t 1）{\"title\": \"xxx\", \"company_match\": \"True\",\"title_similarity\": 10, \"similarity\": 10, \"is_ESG\": \"yes\", \"corporate_entity\": \"xxxx\", \"fiscal_year\": \"xxxx\"} \
            \n\t 2）{\"title\": \"xxx\", \"company_match\": \"False\",\"title_similarity\": 3, \"similarity\": 2, \"is_ESG\": \"no\"}"% (company_name, document_title, company_name, company_name, company_name, company_name)
 
        messages = [
            {
                "role": "system",
                "content": "You are an helpful assistant.",
            },
            {
                "role": "system", 
                "content": documents},
            {
                "role": "user", 
                "content": instruction},
        ]

    elif chat_type == "annual_assessment":
        
        # instruction = "Annual reports provide a significant amount of information on a company’s overall performance in the previous year in every aspect of the business, aiming to provide insights to every type of stakeholders. It provides an outlook for the future, outlining a company’s goals and objectives. Annual reports focus primarily on financials, but we have seen an increasing trend of including sustainability-related data, such as carbon emissions. \
        # \n Please answer the following questions based on the information in the above documents: \
        # \n 1. What is the title of the current document?  \
        # \n 2. Verify if the document's corporate entity is the same company as %s \
        # \n 3. According to the definition of annual report, determine whether the document is an annual report for %s. \
        # \n 4. Please output the corporate entity and fiscal year of the above document. If there is no, it is not necessary to output. \
        # \n Please output the above answers in JSON format and no need to use markdown syntax to encapsulate JSON string into Code Block.\
        # \n You can refer to the following output examples: \
        # \n\t 1）{\"title\": \"xxx\",\"company_match\": \"True\", \"is_annual_report\": \"yes\", \"corporate_entity\": \"xxxx\", \"fiscal_year\": \"xxxx\"} \
        # \n\t 2）{\"title\": \"xxx\",\"company_match\": \"True\", \"is_annual_report\": \"no\", \"corporate_entity\": \"xxxx\", \"fiscal_year\": \"xxxx\"} \
        # \n\t 3）{\"title\": \"xxx\",\"company_match\": \"True\", \"is_annual_report\": \"no\"} \
        # \n\t 4）{\"title\": \"xxx\",\"company_match\": \"False\", \"is_annual_report\": \"no\"}" % (company_name, company_name)
        
        instruction = "Annual reports provide a significant amount of information on a company's overall performance in the previous year in every aspect of the business, aiming to provide insights to every type of stakeholders. It provides an outlook for the future, outlining a company's goals and objectives. Annual reports focus primarily on financials.\
        \n Please answer the following questions based on the definition of Annual report and the above document: \
        \n 1. What is the title of the current document? \
        \n 2. Verify if the document's corporate entity is the same company as %s.\
        \n 3. According to the definition of annual reports, determine whether the document is an annual report for %s. (Titles for annual report are usually: Annual Reports, Integrated Report, Business Report, Universal Registration Document, Financial Result ,Financial Document, Financial Statement, Board Report, Outcome of Board Meeting, Report & Account, Report and Accounts, Accounts and Reports, Finance Report) \
        \n 4. Please output the corporate entity and fiscal year of the above document. \
        \n Please output the above answers in JSON format and no need to use markdown syntax to encapsulate JSON string into Code Block.\
        \n You can refer to the following output examples: \
        \n\t 1）{\"title\": \"xxx\",\"company_match\": \"True\", \"is_annual_report\": \"yes\", \"corporate_entity\": \"xxxx\", \"fiscal_year\": \"xxxx\"} \
        \n\t 2）{\"title\": \"xxx\",\"company_match\": \"True\", \"is_annual_report\": \"no\", \"corporate_entity\": \"xxxx\", \"fiscal_year\": \"xxxx\"} \
        \n\t 3）{\"title\": \"xxx\",\"company_match\": \"True\", \"is_annual_report\": \"no\"} \
        \n\t 4）{\"title\": \"xxx\",\"company_match\": \"False\", \"is_annual_report\": \"no\"}" % (company_name, company_name)
        
        messages = [
            {
                "role": "system",
                "content": "You are an helpful assistant.",
            },
            {
                "role": "system", 
                "content": documents},
            {
                "role": "user", 
                "content": instruction},
        ]
    
    elif chat_type == "info_extract":
        
        instruction = "Please answer the following questions based on the information in the above documents: \
        \n 1. What is the title of the current document?  \
        \n 2. Verify if the document's corporate entity is the same company as %s \
        \n 3. Output the corporate entity of the above document. If there is no, it is not necessary to output. \
        \n 4. Output the fiscal year of the above document. If there is no, it is not necessary to output. \
        \n Please output the above answers in JSON format and no need to use markdown syntax to encapsulate JSON string into Code Block.\
        \n You can refer to the following output examples: \
        \n\t 1）{\"title\": \"xxx\", \"company_match\": \"True\", \"corporate_entity\": \"xxxx\", \"fiscal_year\": \"xxxx\"} \
        \n\t 2）{\"title\": \"xxx\", \"company_match\": \"False\", \"corporate_entity\": \"xxxx\", \"fiscal_year\": \"xxxx\"} \
        \n\t 3）{\"title\": \"xxx\", \"company_match\": \"True\", \"fiscal_year\": \"xxxx\"} \
        \n\t 4）{\"title\": \"xxx\", \"company_match\": \"True\", \"corporate_entity\": \"xxxx\"}" % (company_name)
        
        messages = [
            {
                "role": "system",
                "content": "You are an helpful assistant.",
            },
            {
                "role": "system", 
                "content": documents},
            {
                "role": "user", 
                "content": instruction},
        ]
    
    else:
        raise ValueError("Invalid chat type")

    client = openai.AzureOpenAI(azure_endpoint=endpoint,
                                api_key=api_key,
                                api_version=api_version)
    
    try:
        chat_completion = client.chat.completions.create(
            model=llm_model,
            messages=messages
        )

        result = chat_completion.choices[0].message.content

    except Exception as e:
        raise e

    return result


def is_esg():
    # openai.BadRequestError: Error code: 400 - {'error': {'message': "This model's maximum context length is 131072 tokens. However, your messages resulted in 150944 tokens. Please reduce the length of the messages.", 'type': 'invalid_request_error', 'param': 'messages', 'code': 'context_length_exceeded'}}
    
    # potential intercepted document
    # 20240612
    # markdown_file_path = "../resources/potential_markdown_directory_20240611"
    # assessment_file_path = "../resources/potential_assessment_20240611_info.csv"
    # convert_file_path = "../resources/potential_convert_20240611_info.csv"
    # 20240626 
    # markdown_file_path = "../resources/potential_markdown_directory_20240625"
    # assessment_info_file_path = "../resources/potential_assessment_20240625_3_info.csv"
    # convert_info_file_path = "../resources/potential_convert_20240625_2_info.csv"
    
    # 20240723 
    # markdown_file_path = "../resources/potential_origin_markdown_directory_20240723"
    # intercept_pdf_file_path = "../resources/potential_origin_markdown_directory_20240723"
    # convert_info_file_path = "../resources/potential_convert_20240723_info.csv"
    # assessment_info_file_path = "../resources/potential_assessment_20240723_test_info.csv"
    
    # 20240927
    markdown_file_path = "../resources/potential_origin_markdown_directory_20240927"
    # intercept_pdf_file_path = "../resources/potential_origin_intercept_pdf_directory_20240927"
    convert_info_file_path = "../resources/potential_convert_20240927_info.csv"
    assessment_info_file_path = "../resources/potential_assessment_20240927_info.csv"
    
    markdown_file_list = os.listdir(markdown_file_path)
    try:
        # 防止重复解析
        result = pd.read_csv(assessment_info_file_path)

    except FileNotFoundError:
        result = pd.read_csv(convert_info_file_path)
        result = result.fillna("nan")
        result["intercept_pdf_pages"] = None
        result["parser_info"] = None
        result["document_title"] = None
        result["company_match"] = None
        result["title_similarity"] = None
        result["similarity"] = None
        result["is_ESG"] = None
        result["company"] = None
        result["fiscal_year"] = None

    for i in tqdm(range(len(result))):
        if pd.isna(result["document_title"][i]) != True:
            print(f"report_title: %s has assessmented" % result["document_title"][i])
            result.loc[i, "parser_info"] = "success"
            continue
            
        # 0723 
        file_name_last_year = str(result["filename"][i]).replace(".pdf", "").split("_")[-1]
        
        # file_name_last_year = str(result["title"][i])
        # if file_name_last_year == "nan":
        #     file_name_last_year = str(result["filename"][i]).split("/")[-1].replace(".pdf", "").split("_")[-1]

        # markdown_file_name = str(result["link"][i]).split("/")[-1].replace(".pdf", ".md")
        markdown_file_name = str(result["link_filename"][i]).replace(".pdf", ".md")
        
        company_name = result["name"][i]
        
        if markdown_file_name != "No link" and markdown_file_name in markdown_file_list and markdown_file_name != "nan":
            print(f"2022_report_title: %s, \ncompany_name: %s, \n2023_file_name: %s" % (file_name_last_year, company_name, markdown_file_name))
            
            with open(file=os.path.join(markdown_file_path, markdown_file_name), mode="r") as f:
                documents = f.read()

            if len(documents) == 0:
                print(f"Error: {markdown_file_name} {documents}")
                result.loc[i, "parser_info"] = "Markdown file is empty."
                continue

            llm_parser_res = llm_parser("esg_assessment", documents=documents[:131071], company_name=company_name, document_title=file_name_last_year, llm_model="gpt-4o")
            try:
                res = json.loads(llm_parser_res)
                res_title = res["title"]
                res_company_match = res["company_match"]
                res_title_similarity = res["title_similarity"]
                res_similarity = res["similarity"]
                res_is_ESG = res["is_ESG"]
                    
                patten_list = ["Climate Change", "Disclosure", "Index"]
                is_match = False
                for pa in patten_list:
                    match = re.search(pa.lower(), res_title.lower())
                    if match:
                        is_match = True
                if is_match:
                    res_is_ESG = "no"
                    res_company = None
                    res_fiscal_year = None

                if res_is_ESG == "yes" and res_company_match:
                    res_company = res["corporate_entity"]
                    res_fiscal_year = res["fiscal_year"]
                else:
                    res_company = "nan"
                    res_fiscal_year = "nan"
                    
                result.loc[i, "document_title"] = res_title
                result.loc[i, "company_match"] = res_company_match    
                result.loc[i, "title_similarity"] = res_title_similarity    
                result.loc[i, "similarity"] = res_similarity
                result.loc[i, "is_ESG"] = res_is_ESG
                result.loc[i, "company"] = res_company
                result.loc[i, "fiscal_year"] = res_fiscal_year
                result.loc[i, "parser_info"] = "success"

            except Exception as e:
                print(f"Error: {markdown_file_name} {e}")
                print(f"Error: {markdown_file_name} {llm_parser_res}")
                result.loc[i, "parser_info"] = llm_parser_res
                continue
        else:
            result.loc[i, "parser_info"] = "failed"
            continue

    result.to_csv(assessment_info_file_path, index=False)
    

def is_annual_report():
    # 20240709
    convert_info_file_path = "../resources/potential_convert_annual_20240709_info.csv"
    markdown_file_path = "../resources/potential_annual_markdown_directory_20240709"
    intercept_pdf_file_path = "../resources/potential_intercepted_annual_pdf_directory_20240709"
    assessment_info_file_path = "../resources/potential_annual_report_assessment_20240709_info@0731.csv"
    
    # 20240716
    # convert_info_file_path = "../resources/potential_convert_annual_20240716_info.csv"
    # markdown_file_path = "../resources/potential_annual_markdown_directory_20240716"
    # intercept_pdf_file_path = "../resources/potential_intercepted_annual_pdf_directory_20240716"
    # assessment_info_file_path = "../resources/potential_annual_report_assessment_20240716_info.csv"

    markdown_file_list = os.listdir(markdown_file_path)
    
    try:
        result = pd.read_csv(assessment_info_file_path)

    except FileNotFoundError:
        # 防止重复解析
        result = pd.read_csv(convert_info_file_path)
        result = result.fillna("nan")
        result["parser_info"] = None
        result["document_title"] = None
        result["company_match"] = None
        result["is_annual_report"] = None
        result["company"] = None
        result["fiscal_year"] = None

    patten_list = ["annual", "integrated", "Integrated Report", "Business Report", "Universal Registration Document", "Financial Result", "Financial Document", "Financial Statement", "Board Report", "Outcome of Board Meeting", "Report & Accounts", "Report and Accounts", "Accounts and Reports", "Finance Report"]
    
    for i in tqdm(range(len(result))):
        if i >=300:
            break
            
        if pd.isna(result["document_title"][i]) != True:
            print(f"report_title: %s has assessmented" % result["document_title"][i])
            result.loc[i, "parser_info"] = "success"
            continue
        
        intercept_pdf_file_name = str(result["link_filename"][i])
        markdown_file_name = intercept_pdf_file_name.replace(".pdf", ".md")
        
        company_name = result["name"][i]

        if markdown_file_name != "No link" and markdown_file_name in markdown_file_list and markdown_file_name != "nan":
            print(f"company_name: %s, markdown_file_name: %s, intercept_pdf_file_name:%s" % (company_name, markdown_file_name, intercept_pdf_file_name))

            # 读取markdown文件
            with open(file=os.path.join(markdown_file_path, markdown_file_name), mode="r") as f:
                documents = f.read()

            if len(documents) == 0:
                print(f"Error: {markdown_file_name} {documents}")
                result.loc[i, "parser_info"] = "Markdown file is empty."
                continue
            
            # 统计pdf页数
            intercept_pdf_pages = pdf_pages(intercept_pdf_file_path, intercept_pdf_file_name)
            
            if intercept_pdf_pages < 10:
                result.loc[i, "is_annual_report"] = "no"
                result.loc[i, "parser_info"] = "file pages < 10."
                result.loc[i, "document_title"] = "nan"
                result.loc[i, "company_match"] = "nan"    
                result.loc[i, "company"] = "nan"
                continue
                
            intercept_pdf_file_name = intercept_pdf_file_name.replace("_", " ").replace("-", " ")
            for pa in patten_list:
                match = re.search(pa.lower(), markdown_file_name.lower())
            if match:
                result["is_annual_report"] = "yes"
    
                llm_parser_res = llm_parser("info_extract", documents=documents[:131071], company_name=company_name, llm_model="gpt-4o")
        
                try:
                    res = json.loads(llm_parser_res)
                    res_title = res["title"]
                    res_company_match = res["company_match"]

                    if res_is_annual == "yes" and res_company_match:
                        res_company = res["corporate_entity"]
                        res_fiscal_year = res["fiscal_year"]
                    else:
                        res_company = "nan"
                        res_fiscal_year = "nan"

                    result.loc[i, "document_title"] = res_title
                    result.loc[i, "company_match"] = res_company_match    
                    result.loc[i, "company"] = res_company
                    result.loc[i, "fiscal_year"] = res_fiscal_year
                    result.loc[i, "parser_info"] = "success"
                except Exception as e:
                    print(f"Error: {markdown_file_name} {e}")
                    print(f"Error: {markdown_file_name} {llm_parser_res}")
                    result.loc[i, "parser_info"] = llm_parser_res
                    continue
                    
            else:
                llm_parser_res = llm_parser("annual_assessment", documents=documents[:131071], company_name=company_name, llm_model="gpt-4o")
                try:
                    res = json.loads(llm_parser_res)
                    res_title = res["title"]
                    res_company_match = res["company_match"]
                    res_is_annual = res["is_annual_report"]


                    is_match = True
                    for pa in patten_list:
                        match = re.search(pa.lower(), res_title.lower())
                        if match:
                            is_match = False
                    if is_match:
                        res_is_annual = "no"
                        res_company = "nan"
                        res_fiscal_year = "nan"

                    if res_is_annual == "yes" and res_company_match:
                        res_company = res["corporate_entity"]
                        res_fiscal_year = res["fiscal_year"]
                    else:
                        res_company = "nan"
                        res_fiscal_year = "nan"

                    result.loc[i, "document_title"] = res_title
                    result.loc[i, "company_match"] = res_company_match    
                    result.loc[i, "is_annual_report"] = res_is_annual
                    result.loc[i, "company"] = res_company
                    result.loc[i, "fiscal_year"] = res_fiscal_year
                    result.loc[i, "parser_info"] = "success"

                except Exception as e:
                    print(f"Error: {markdown_file_name} {e}")
                    print(f"Error: {markdown_file_name} {llm_parser_res}")
                    result.loc[i, "parser_info"] = llm_parser_res
                    continue
        else:
            result.loc[i, "parser_info"] = "failed"
            continue
    result.to_csv(assessment_info_file_path, index=False)
    
if __name__ == "__main__":
    is_esg()
    # is_annual_report()