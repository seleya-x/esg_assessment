import os
import json
import openai
import dotenv
import pandas as pd

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
               llm_model:str="gpt-35-turbo"):

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

    elif chat_type == "assessment":
        # time = "2022"
        # company_name = "Westpac Banking Corp"
        # document_title = "Sustainability Supplement 2022 - Westpac Group"

        # instruction = "The following is a document written by a company. The document is written in markdown format. \
        #         \nThe ESG report title of %s for %s is \"%s\". Please refer to the above information to read the current document and answer the following questions: \
        #             \n\t1. What is the title of the current document? \
        #             \n\t2. Regardless of time, Check the similarity of the giving title and the current document title, with a total score of 10 points, with 0 being the lowest and 10 being the highest. \
        #             \n\t3. Rate the degree of overlap between the current document and the given title. The total score is 10 points, with 0 being the lowest and 10 being the highest. \
        #             \n\t4. Please determine whether the current document is the original ESG report of %s based on the similarity of the title and the content of the document? If so, please output the report body and report date of the document. If not, it is not necessary to output. Please note that the report date refers to the financial reporting period, not the publication date of the document. \
        #         \nPlease output the above answer results in JSON format. Do not use markdown syntax for output results.\
        #         \nYou can refer to the following output examples: \
        #                 \n\t1）{\"title\": \"xxx\", \"title_similarity\": 10, \"similarity\": 10, \"is_ESG\": \"yes\", \"company\": \"xxxx\", \"financial_report_time\": \"xxxx\"} \
        #                 \n\t2）{\"title\": \"xxx\", \"title_similarity\": 3, \"similarity\": 2, \"is_ESG\": \"no\"} \
        #         \n\nThe detailed content of the document is as follows: \n\n%s" % (time, company_name, document_title, company_name, documents)        

        # instruction = "The ESG report title of %s for %s is \"%s\". Please refer to the above information to read the current document and answer the following questions: \
        #             \n\t1. What is the title of the current document? \
        #             \n\t2. Regardless of time, Check the similarity of the giving title and the current document title, with a total score of 10 points, with 0 being the lowest and 10 being the highest. \
        #             \n\t3. Rate the degree of overlap between the current document and the given title. The total score is 10 points, with 0 being the lowest and 10 being the highest. \
        #             \n\t4. Please determine whether the current document is the original ESG report of %s based on the similarity of the title and the content of the document? If so, please output the report body and report date of the document. If not, it is not necessary to output. Please note that the report date refers to the financial reporting period, not the publication date of the document. \
        #         \nPlease output the above answer results in JSON format. \
        #         \nYou can refer to the following output examples: \
        #                 \n\t1）{\"title\": \"xxx\", \"title_similarity\": 10, \"similarity\": 10, \"is_ESG\": \"yes\", \"company\": \"xxxx\", \"financial_report_time\": \"xxxx\"} \
        #                 \n\t2）{\"title\": \"xxx\", \"title_similarity\": 3, \"similarity\": 2, \"is_ESG\": \"no\"} \
        #         \nPlease Do not use markdown syntax for output results." % (time, company_name, document_title, company_name)
        
        instruction = "The ESG report title of %s for %s is \"%s\". Please refer to the above information to read the current document and answer the following questions: \
                        \n\t1. What is the title of the current document? \
                        \n\t2. Regardless of time, Check the similarity of the giving title and the current document title, with a total score of 10 points, with 0 being the lowest and 10 being the highest. \
                        \n\t3. Rate the degree of overlap between the current document and the given title. The total score is 10 points, with 0 being the lowest and 10 being the highest. \
                        \n\t4. Based on the similarity between the current document title and the ESG report title for the %s of %s as well as the content of the current document, \
                            infer that  whether the ESG report framework used in the current document is consistent with the ESG report framework for the %s of %s? \
                            If so, please output the corporate entity and fiscal year of the document. If not, it is not necessary to output. \
                    \nPlease output the above answer results in JSON format. \
                    \nYou can refer to the following output examples: \
                            \n\t1）{\"title\": \"xxx\", \"title_similarity\": 10, \"similarity\": 10, \"is_ESG\": \"yes\", \"corporate_entity\": \"xxxx\", \"fiscal_year\": \"xxxx\"} \
                            \n\t2）{\"title\": \"xxx\", \"title_similarity\": 3, \"similarity\": 2, \"is_ESG\": \"no\"} \
                    \nPlease Do not use markdown syntax for output results." % (time, company_name, document_title, time ,company_name, time, company_name)
        
        instruction = "The ESG report title of %s for %s is \"%s\". Please refer to the above information to read the current document and answer the following questions: \
                        \n\t1. What is the title of the current document? \
                        \n\t2. Ignore the time in the title and give a similarity score between the given title and the current document title. The total score is 10 points, with 0 being the lowest and 10 being the highest. \
                        \n\t3. Ignore the time factor and rate the overlap between the current document and the provided title? The total score is 10 points, with 0 being the lowest and 10 being the highest. \
                        \n\t4. Based on the similarity between the current document title and the ESG report title for the %s of %s as well as the content of the current document, \
                            infer that  whether the ESG report framework used in the current document is consistent with the ESG report framework for the %s of %s? \
                            If so, please output the corporate entity and fiscal year of the document. If not, it is not necessary to output. \
                    \nPlease output the above answer results in JSON format. \
                    \nYou can refer to the following output examples: \
                            \n\t1）{\"title\": \"xxx\", \"title_similarity\": 10, \"similarity\": 10, \"is_ESG\": \"yes\", \"corporate_entity\": \"xxxx\", \"fiscal_year\": \"xxxx\"} \
                            \n\t2）{\"title\": \"xxx\", \"title_similarity\": 3, \"similarity\": 2, \"is_ESG\": \"no\"} \
                    \nPlease Do not use markdown syntax for output results." % (time, company_name, document_title, time ,company_name, time, company_name)
        
        # add React framework
        instruction = "The ESG report title of %s for %s is \"%s\". Please refer to the above information to read the current document and answer the following questions: \
                        \n\t1. What is the title of the current document? \
                        \n\t2. Ignore the time in the title and give a similarity score between the given title and the current document title. The total score is 10 points, with 0 being the lowest and 10 being the highest. \
                        \n\t3. Ignore the time factor and rate the overlap between the current document and the provided title? The total score is 10 points, with 0 being the lowest and 10 being the highest. \
                        \n\t4. Based on the similarity between the current document title and the ESG report title for the %s of %s as well as the content of the current document, \
                            infer that  whether the ESG report framework used in the current document is consistent with the ESG report framework for the %s of %s? \
                            If so, please output the corporate entity and fiscal year of the document. If not, it is not necessary to output. \
                    \nPlease output the above answer results in JSON format and do not use markdown syntax for output results.\
                    \nYou can refer to the following output examples: \
                            \n\t1）{\"title\": \"xxx\", \"title_similarity\": 10, \"similarity\": 10, \"is_ESG\": \"yes\", \"corporate_entity\": \"xxxx\", \"fiscal_year\": \"xxxx\"} \
                            \n\t2）{\"title\": \"xxx\", \"title_similarity\": 3, \"similarity\": 2, \"is_ESG\": \"no\"} \
                    \nApproach this task step-by-step, take your time and do not skip steps."% (time, company_name, document_title, time ,company_name, time, company_name)
        
        instruction = "The ESG report title for %s is \"%s\". Please refer to the above information to read the current document and answer the following questions: \
                        \n\t1. What is the title of the current document? \
                        \n\t2. Ignore the time in the title and give a similarity score between the given title and the current document title. The total score is 10 points, with 0 being the lowest and 10 being the highest. \
                        \n\t3. Ignore the time factor and rate the overlap between the current document and the provided title? The total score is 10 points, with 0 being the lowest and 10 being the highest. \
                        \n\t4. Based on the similarity between the current document title and the ESG report title for %s as well as the content of the current document, \
                            infer that  whether the ESG report framework used in the current document is consistent with the ESG report framework for %s? \
                            If so, please output the corporate entity and fiscal year of the document. If not, it is not necessary to output. \
                    \nPlease output the above answer results in JSON format and do not use markdown syntax for output results.\
                    \nYou can refer to the following output examples: \
                            \n\t1）{\"title\": \"xxx\", \"title_similarity\": 10, \"similarity\": 10, \"is_ESG\": \"yes\", \"corporate_entity\": \"xxxx\", \"fiscal_year\": \"xxxx\"} \
                            \n\t2）{\"title\": \"xxx\", \"title_similarity\": 3, \"similarity\": 2, \"is_ESG\": \"no\"} \
                    \nApproach this task step-by-step, take your time and do not skip steps."% (company_name, document_title, company_name, company_name)

 
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


if __name__ == "__main__":
    # with open(file="./target_markdown_directory/AAPL.OQ_FY2022_2022 ESG Report.pdfAAPL.OQ_FY2022_2022 ESG Report.md", mode="r") as f:
    #     documents = f.read()

    # title = json.loads(llm_parser("title_extraction", documents, llm_model="gpt-4o"))["title"]
    # print(title)
    # print(llm_parser("qa", documents, time="2022", company_name="Apple Inc.", document_title="Apple’s 2022 ESG Report", llm_model="gpt-4o"))

    # time = "2022"
    # company_name = "Westpac Banking Corp"
    # document_title = "Sustainability Supplement 2022 - Westpac Group"

    # download_info = pd.read_csv("../resources/download_info.csv")

    # file_download_path = "../resources/target_markdown_directory_2022"
    # file_list = os.listdir(file_download_path)

    # title_extraction
    # for file_name in file_list:
    #     with open(file=os.path.join(file_download_path, file_name), mode="r") as f:
    #         documents = f.read()
    #     # openai.BadRequestError: Error code: 400 - {'error': {'message': "This model's maximum context length is 131072 tokens. However, your messages resulted in 150944 tokens. Please reduce the length of the messages.", 'type': 'invalid_request_error', 'param': 'messages', 'code': 'context_length_exceeded'}}
    #     title = llm_parser("title_extraction", documents[:131071], llm_model="gpt-4o")
    #     print(file_name)
    #     print(title)

    # assessment
    # origin_info_df = pd.read_excel("../resources/reports_collection_2023.xlsx")
    # origin_info_df = origin_info_df.fillna("nan")
    # download_2023_info = pd.read_csv("../resources/download_2023_info.csv")
    # result = pd.concat([origin_info_df, download_2023_info], axis=1)

    result = pd.read_csv("../resources/potential_convert_2023_info.csv")
    result = result.fillna("nan")

    # full document
    # file_download_path = "../resources/target_markdown_directory_2023"
    # file_list = os.listdir(file_download_path)

    # potential intercepted document
    file_download_path = "../resources/potential_markdown_directory_2023"
    file_list = os.listdir(file_download_path)

    result["parser_info"] = None
    result["document_title"] = None
    result["title_similarity"] = None
    result["similarity"] = None
    result["is_ESG"] = None
    result["company"] = None
    result["fiscal_year"] = None

    for i in range(len(result)):
        # if i >=300:
        #     break

        if result["document_title"][i] != None and result["document_title"][i] != "nan" and result["document_title"][i] != "No link" and result["document_title"][i] != "No title" and result["document_title"][i] != "nan":
            print(f"2022_report_title: %s, \n has assessmented" % (result["document_title"][i]))
            result.loc[i, "parser_info"] = "success"
            continue

        file_name_last_year = result["filename"][i].split("/")[-1].replace(".pdf", "").split("_")[-1]

        file_name = result["link"][i].split("/")[-1].replace(".pdf", ".md")

        # time = result["FY"][i]
        company_name = result["name"][i]

        if file_name != "No link" and file_name in file_list and file_name != "nan":
            print(f"2022_report_title: %s, \ncompany_name: %s, \n2023_file_name: %s" % (file_name_last_year, company_name, file_name))
            
            with open(file=os.path.join(file_download_path, file_name), mode="r") as f:
                documents = f.read()

            if len(documents) == 0:
                print(f"Error: {file_name} {documents}")
                result.loc[i, "parser_info"] = "Markdown file is empty."
                continue

            try:
                # res = llm_parser("assessment", documents[:131071], time=time, company_name=company_name, document_title=file_name_2022, llm_model="gpt-4o")
                # res = json.loads(llm_parser("assessment", documents=documents[:131071], time=time, company_name=company_name, document_title=file_name_last_year, llm_model="gpt-4o"))
                res = json.loads(llm_parser("assessment", documents=documents[:131071], company_name=company_name, document_title=file_name_last_year, llm_model="gpt-4o"))

                print(f"predict: %s" % res)
                print()
                res_title = res["title"]
                res_title_similarity = res["title_similarity"]
                res_similarity = res["similarity"]
                res_is_ESG = res["is_ESG"]
                if res_is_ESG == "yes":
                    res_company = res["corporate_entity"]
                    res_fiscal_year = res["fiscal_year"]
                else:
                    res_company = "nan"
                    res_fiscal_year = "nan"

                result.loc[i, "document_title"] = res_title
                result.loc[i, "title_similarity"] = res_title_similarity    
                result.loc[i, "similarity"] = res_similarity
                result.loc[i, "is_ESG"] = res_is_ESG
                result.loc[i, "company"] = res_company
                result.loc[i, "fiscal_year"] = res_fiscal_year
                result.loc[i, "parser_info"] = "success"

            except Exception as e:
                print(f"Error: {file_name} {e}")
                result.loc[i, "parser_info"] = e
                continue
        else:
            result.loc[i, "parser_info"] = "failed"
            continue

    result.to_csv("../resources/potential_assessment_2023_info.csv", index=False)