This repo is the implementation of "AI4Reading: Chinese Audiobook Interpretation System Based on Multi-Agent Collaboration".

## Introduction

AI for Reading Framework is a multi-agent collaboration system designed to transform book content into structured, engaging interpretive manuscripts and high-quality audio outputs. By simulating the workflow of human experts, this framework automates complex processes such as topic identification, preliminary interpretation, oral rewriting, reconstruction and revision. Specialized agents—Topic Researchers , Case Analysts , Proofreaders , Editors , and Narrators —are employed to address specific challenges at each stage, ensuring accuracy, coherence, and engagement in the final output. Additionally, cutting-edge Text-to-Speech technology and carefully designed sound-effect strategies further enhance the auditory experience. 

![Agent](https://github.com/9624219/AI4reading/blob/master/pic/Agent.png)



## Installation

Install the required dependencies

```
conda create -n <your env name> python=3.10
conda activate <your env name>
pip install -r requirement.txt
```

## Quickstart

- For Ollama users, you need to download the corresponding model and change the model in ollama.generate in the utils.chat file. Here is an example

```python
def Qwen_Generate(prompt_text,system_text):
    if system_text == '':
        res = ollama.generate(model="qwen2.5:72b-instruct", prompt=prompt_text, options={"num_ctx": 30720,"num_predict":-1})
    else:
        res = ollama.generate(model="qwen2.5:72b-instruct", prompt=prompt_text, system=system_text,options={"num_ctx": 30720,"num_predict":-1})
    result = res['response']
    return result
```

- For users of other api services, you need to fill in the "api_key" and “base_url” in utils.chat.

```python
client = OpenAI(api_key="", base_url="")
```

- Then run the script：
  input_path: chapter content address, for the txt format, if for pdf and other formats, please turn into txt. e.g. “input.txt”.
  input_path: Address for deposit of interpretative texts, e.g. “output.txt”.

```
python run_agent.py input_path output_path
```

You'll get a manuscript of the corresponding chapter in your output path. 

- For the audio generation section, please refer to [fish-speech](https://github.com/fishaudio/fish-speech) or other speech synthesis frameworks

## Limitations

the current method has been tested exclusively on data from psychology, personal growth, and business management books. This domain constraint limits the system’s applicability, as it cannot yet process or generate interpretations for literature or novels.

## Appreciation

- [fish-speech](https://github.com/fishaudio/fish-speech) for text-to-speech synthesis model.
- [MetaGPT](https://github.com/geekan/MetaGPT) for Multi-Agent Framework

