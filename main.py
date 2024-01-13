# import json

import regex
import torch
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import DirectoryLoader, TextLoader

from langchain.embeddings.base import  Embeddings
from sentence_transformers import SentenceTransformer
# from langchain.chains import RetrievalQA
# import CharacterTextSplitter
from langchain.text_splitter import CharacterTextSplitter

# from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.keys import Keys
# from os.path import exists, dirname, realpath, join, isfile
# from os import makedirs, remove, system, getcwd
# from typing import Union
# from random import uniform
from time import sleep
# from threading import Thread
# from pynput.keyboard import Controller, Listener, GlobalHotKeys
# from PySide2.QtCore import *
# from PySide2.QtWidgets import *
# from PySide2.QtGui import *
import undetected_chromedriver as uc
import selenium.webdriver.support.expected_conditions as EC
# from lxml import html
reset_database = True

QUERY = 'O que o incrédulo Voltaire orgulhosamente disse certa vez?'
LLM = 'claude-2.1\n'

if LLM[-1] != '\n':
    LLM += '\n'

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
def remove_emojis(data):
    emoj = regex.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", regex.UNICODE)
    return regex.sub(emoj, '', data)
def search_score(query):
    results = db.similarity_search_with_relevance_scores(query, k=3)
    if len(results) == 0 or results[0][1] < 0.36:
        print("Sem resultados relevantes.")
        return 
    context_text = '||'.join([doc.page_content for doc, _score in results])
    print(context_text)
    return context_text#, results

class SentenceTransformerEmbeddings(Embeddings):
    'all-MiniLM-L6-v2'
    "intfloat/multilingual-e5-large"
    def __init__(self, model_name='all-MiniLM-L6-v2', device=device):
        self._embedding_function = SentenceTransformer(model_name, device=device)
    def embed_documents(self, texts):
        embeddings = self._embedding_function.encode(texts, convert_to_numpy=True).tolist()
        return [list(map(float, e)) for e in embeddings]
    def embed_query(self, text):
        embeddings = self._embedding_function.encode([text], convert_to_numpy=True).tolist()
        return [list(map(float, e)) for e in embeddings][0]
    
embeddings = SentenceTransformerEmbeddings()
vectorstore_path = "./db/embeddings/"

vectorstore = FAISS
index_name = "vectorstore_faiss"


if reset_database:
    db = None
    max_fetch = -1
    max_query = 20

    loader = DirectoryLoader("./documents", glob= "*.*", loader_cls=TextLoader, use_multithreading=True, max_concurrency=4)
    docs = loader.load()
    texts = [x.page_content for x in docs]
    raw_text = ''
    for i, text in enumerate(texts):
        if text:
            raw_text += text

    text_splitter = CharacterTextSplitter(
        separator = '\n',
        chunk_size = 800,
        chunk_overlap  = 200,
        length_function = len,
    )
    texts = text_splitter.split_text(raw_text)
    ddx = text_splitter.split_documents(docs)

    db = vectorstore.from_documents(ddx, embeddings)
    db.save_local(index_name)
else:
    db = FAISS.load_local(index_name, embeddings)
# retriever = db.as_retriever(search_kwargs={"k": 4}) #4




opt = uc.ChromeOptions()
opt.add_argument("--headless=new")
opt.add_argument('--use-gl=angle')
# opt.add_argument("user-agent=")

driver = uc.Chrome(options=opt)
driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36", "platform":"Windows"})
with driver:
    driver.get('https://chat.lmsys.org')
    # sleep(5)
    # driver.save_screenshot('lmsys.png')
    # exit()
    WebDriverWait(driver, timeout=3).until(EC.alert_is_present())

    alert = driver.switch_to.alert
    alert.dismiss()
    sleep(1)
    driver.find_element(By.CSS_SELECTOR, ".svelte-kqij2n:nth-child(3)").click()
    sleep(1)
    text = search_score(QUERY).replace('\n', '')

    # set model
    
    model = driver.find_elements(By.CSS_SELECTOR, '.border-none.svelte-1xsj8nn')[2]
    driver.execute_script('arguments[0].value="";', model)
    
    model.send_keys(LLM)
    sleep(1.5)
    # driver.save_screenshot("teste.png")
    # input()
    driver.find_element(By.CSS_SELECTOR, "#component-87 .scroll-hide").send_keys('Baseando-se no contexto, responda de forma resumida.\\n contexto: \\n' +remove_emojis(text)+'\\nCom base no contexto fornecido, responda: '+QUERY+"\n")
    sleep(1.5)
    print('\nwaiting...')
    while True:
        if not driver.find_element(By.CSS_SELECTOR, "#component-92").is_enabled():
            sleep(0.5)
            # driver.save_screenshot("teste2.png")
        else:
            break
        
    last_messages = driver.find_elements(By.CSS_SELECTOR, '[data-testid="bot"]')[-1]
    messages = last_messages.find_elements(By.CSS_SELECTOR, 'p')
    print('\n'.join([msg.text for msg in messages]))
input()

