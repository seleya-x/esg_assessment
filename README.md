# ESG Report assessment
![prrocess flow](./asserts/processing%20flow.png)

## 1. Download & intercept

### 1.1. Download
download pdf file

### 1.2. intercept
Intercept the first 10 pages of origin pdf file


## 2. Convert
convert pdf to markdown format by [LlamaParse](https://www.llamaindex.ai/blog/introducing-llamacloud-and-llamaparse-af8cedf9006b)


## 3. Extract & Assessment
Using GPT to analysis file content and extract some information

### 3.1. Title Extract prompt

```
The following is a document written by a company. The document is written in markdown format. Please provide the title of the document.Please output the above answer with the JSON format:{\"title\":\"xxxx\"}

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


