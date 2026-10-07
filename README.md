# Personal Values Layer (PVL) — POC

An add-on for openJiuwen agents that remembers a user's long-term goals, brings them up at the right time, and stays quiet otherwise.

## Setup

The Python environment lives outside `Documents` (a Windows security policy blocks compiled packages there):

```bash
python -m venv C:/Users/A2306101770/venvs/pvl
C:/Users/A2306101770/venvs/pvl/Scripts/python -m pip install -r requirements.txt
```

Then put your DeepSeek API key in `.env` (copy `.env.example` if `.env` doesn't exist).

## Run the baseline agent

```bash
C:/Users/A2306101770/venvs/pvl/Scripts/python chat.py
```
