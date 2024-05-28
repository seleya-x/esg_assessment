# ESG Report assessment


## Download & intercept



## Convert


## Extract & assessment
### Title Extract prompt

```
The following is a document written by a company. The document is written in markdown format. Please provide the title of the document.Please output the above answer with the JSON format:{\"title\":\"xxxx\"}

```



### ESG report  Assessment prompt
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


