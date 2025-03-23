import os

import google.generativeai
import google.generativeai as genai
import google.ai.generativelanguage as genl1
import config
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.prompts import PromptTemplate
os.environ["HTTP_PROXY"] = config.HTTP_PROXY
os.environ["HTTPS_PROXY"] = config.HTTPS_PROXY
api_key = config.API_KEY
genai.configure(api_key = api_key)
gemini_pro = genai.GenerativeModel("gemini-pro")
# PaLm = genai.GenerativeModel("PaLM")
# llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=api_key)
# for m in genai.list_models():
#   if 'generateContent' in m.supported_generation_methods:
#     print(m.name)
# print(
#     llm.invoke(
#         "What are some of the pros and cons of Python as a programming language?"
#     )
# )
