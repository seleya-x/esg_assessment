# ESG Report assessment
![prrocess flow](./asserts/processing%20flow.png)

## 1. Download & intercept

### 1.1. Download
Download the PDF file using the provided URLs.

| link_2022 | filename_2022  | link_filename |
|:------|:-----|:-----|
| https://portagebay.azureedge.net/nsark/audit_files/AAPL.OQ/AAPL.OQ_FY2022_2022 ESG Report.pdf | AAPL.OQ_FY2022_2022 ESG Report.pdf | https://www.apple.com/environment/pdf/Apple_Environmental_Progress_Report_2023.pdf |
| https://portagebay.azureedge.net/nsark/audit_files/MSFT.OQ/MSFT.OQ_FY2022_Sustainable Development Goals Report 2022.pdf | MSFT.OQ_FY2022_Sustainable Development Goals Report 2022.pdf | https://s3.amazonaws.com/sustainabledevelopment.report/2023/sustainable-development-report-2023.pdf |

### 1.2. intercept
Extract the first 10 pages from the original PDF file. Considering the original PDF file has a few hundred pages, it will take a large number of GPT tokens, so we capture the first 10 pages for PDF to markdown format conversion.


## 2. Convert
Convert pdf to markdown format by [LlamaParse](https://www.llamaindex.ai/blog/introducing-llamacloud-and-llamaparse-af8cedf9006b). The converting period takes a long time, but LlamaParse offers an async API, so we use the async API to parallelize our data.


## 3. Extract & Assessment
Using GPT to analyze file content and extract information through prompt engineering. in this project, we use native chat.completions api with openai.AzureOpenAI.

### 3.1. Title Extract prompt

```
The above is a document written by a company. The document is written in markdown format. Please provide the title of the document. 
Please output the above answer with the JSON format:{\"title\":\"xxxx\"}

```

### 3.2. ESG report  Assessment prompt
```
"The ESG report title of %s for %s is "%s". Please refer to the above information to read the current document and answer the following questions:
    1. What is the title of the current document?
    2. Regardless of time, Check the similarity of the giving title and the current document title, with a total score of 10 points, with 0 being the lowest and 10 being the highest.
    3. Rate the degree of overlap between the current document and the given title. The total score is 10 points, with 0 being the lowest and 10 being the highest.
    4. Based on the similarity between the current document title and the ESG report title for the %s of %s as well as the content of the current document, infer that  whether the ESG report framework used in the current document is consistent with the ESG report framework for the %s of %s?
If so, please output the corporate entity and fiscal year of the document. If not, it is not necessary to output.
Please output the above answer results in JSON format.
You can refer to the following output examples:
    1）{\"title\": \"xxx\", \"title_similarity\": 10, \"similarity\": 10, \"is_ESG\": \"yes\", \"corporate_entity\": \"xxxx\", \"fiscal_year\": \"xxxx\"}
    2）{\"title\": \"xxx\", \"title_similarity\": 3, \"similarity\": 2, \"is_ESG\": \"no\"}
Please Do not use markdown syntax for output results." % (time, company_name, document_title, time ,company_name, time, company_name)
```

### 3.3. main process code 

```
import openai

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
            "content": instruction}]

client = openai.AzureOpenAI(azure_endpoint=endpoint,
                            api_key=api_key,
                            api_version=api_version)

chat_completion = client.chat.completions.create(
        model=llm_model,
        messages=messages)

result = chat_completion.choices[0].message.content

```
