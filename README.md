# Important

  

Due to high traffic you may not get your response:

![lmsys high traffic error](https://i.imgur.com/XCKyE2r.png)

A workaround is to change the LLM (eg. claude-2.1 to gpt-4-turbo), but depending of chosen LLM some contents may be refused to be replied, like happens with chatGPT

  

You have to know that using this code you agree to the following, since my code will automatically click OK:

  

![lmsys agreement](https://i.imgur.com/n5ajuLD.png)

  

**chat.Imsys.org say:

Users of this website are required to agree to the following terms:

The service is a research preview. It only provides limited safety

measures and may generate offensive content. It must not be

used forany llegal, harmful, violent, racist, or sexual purposes.

The service collects user dialogue data and reserves the right to

distribute it under a Creative Commons Attribution (CC-BY) ora

similar license.**

  

It means everything you share using this project will be public or used somehow by lmsys team, so, please, **don't share ANY sensitive info**.

I'm not responsible for any misuse of this tool.

  

## Overview

#### Made to run on Linux, so, be aware about bugs on Windows or other OS.

#### If you have a dedicated GPU install faiss-gpu, otherwise faiss-cpu

This is a project about how to RAG (Retrieval Augmented Generation), a structure that allow you to chat with your own documents using langchain, FAISS and very large LLMs even in low resource computers through chat.lmsys.org

I want to make a GUI later, but now **it's just an example code**

  

I have nothing related to lmsys.org

### How it works:

Once you run it, FAISS vectorstore (database) will be created, then you can change line 31 (```

reset_database = True```) to False for next executions if you don't want to add new documents, so it will run faster next time.

  

**Note**: *most/larger documents, more the time to start the inference, even in high performance computers.*

  

This is just a local API that use all-MiniLM-L6-v2 as embedding model to find best results in your documents accordingly with your QUERY, then it use your Chrome Browser to connect to chat.lmsys.org and send a message like this:

```

based on the context, answer the question:

context: best found results in your documents

question: your QUERY

```

After your message be sent to the LLM, it will print "waiting..." until the model finish to write the answer, then will print the answer.

  

**Note:**  *All the code is adapted to use portuguese, feel free to edit to use any language you want. Also, the browser will launch in headless mode (invisible).*

  

## Usage

For now, just drop your documents into documents folder, write your question to the QUERY constant in line 33 and run the code.

The LLM used for this is set in line 34 (claude 2.1), and you may change if you want and know what are you doing.

## Supported file extensions

  

The supported files are limited to **Document Loader supported files**.

  

**from langchain:**

  

[Retrieval](https://python.langchain.com/docs/modules/data_connection/)

  

- [Document loaders](https://python.langchain.com/docs/modules/data_connection/document_loaders/)

  

- [CSV](https://python.langchain.com/docs/modules/data_connection/document_loaders/csv)

  

- [File Directory](https://python.langchain.com/docs/modules/data_connection/document_loaders/file_directory)

  

- [HTML](https://python.langchain.com/docs/modules/data_connection/document_loaders/html)

  

- [JSON](https://python.langchain.com/docs/modules/data_connection/document_loaders/json)

  

- [Markdown](https://python.langchain.com/docs/modules/data_connection/document_loaders/markdown)

  

- [PDF](https://python.langchain.com/docs/modules/data_connection/document_loaders/pdf)

  

\***or any plaintext like**
**Note:** Maybe it work with some ebook files too, you should try to be sure.