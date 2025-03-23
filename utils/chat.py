import sys
import os
sys.path.append(os.path.dirname(__file__))
import ollama
from openai import OpenAI
client = OpenAI(api_key="", base_url="")

def askQwen(messages):
    res = ollama.chat(model = "qwen2.5:72b-instruct", messages = messages,keep_alive='1h')
    return res['message']['content']


def Qwen_Generate(prompt_text,system_text):
    prompt_text = prompt_text.replace('\n\n', '\n')
    if system_text == '':
        res = ollama.generate(model="qwen2.5:72b-instruct", prompt=prompt_text, keep_alive='1h', options={"num_ctx": 30720,"num_predict":-1})
    else:
        res = ollama.generate(model="qwen2.5:72b-instruct", prompt=prompt_text, system=system_text, keep_alive='1h', options={"num_ctx": 30720,"num_predict":-1})
    result = res['response']
    result = result.replace('\n\n', '\n')
    return result

def Deepseek_Generate(prompt_text,system_text):
    prompt_text = prompt_text.replace('\n\n', '\n')
    if system_text == '':
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": prompt_text},
            ],
            max_tokens=8192,
            stream=False,
            temperature=1.3
        )
    else:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_text},
                {"role": "user", "content": prompt_text},
            ],
            max_tokens=8192,
            stream=False,
            temperature=1.3
        )
    result = response.choices[0].message.content
    result = result.replace('\n\n', '\n')
    return result

def askQwenJson(messages):
    res = ollama.chat(model = "qwen2.5:72b-instruct", messages = messages,keep_alive='1h',format='json')
    return res['message']['content']
