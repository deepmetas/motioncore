import os
import json
from dotenv import load_dotenv
from openai import OpenAI
import httpx
import time

# 加载项目根目录的 .env
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")

# ====================== 通用客户端创建 ======================
def _create_client(api_key, base_url=None):
    """统一创建 OpenAI 兼容客户端"""
    timeout = httpx.Timeout(connect=30.0, read=300.0, write=30.0, pool=30.0)
    kwargs = {"api_key": api_key, "timeout": timeout, "max_retries": 0}
    if base_url:
        kwargs["base_url"] = base_url
    return OpenAI(**kwargs)

# ====================== 统一流式生成器 ======================
def _stream_chat(client, model, messages):
    """通用流式聊天生成器（chat.completions）"""
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True,
        max_tokens=4096
    )
    for chunk in response:
        if chunk.choices and chunk.choices[0].delta:
            content = chunk.choices[0].delta.content
            if content:
                yield content

# ====================== 核心接口 ======================
def analyze_videos_stream(video1_json, video2_json, prompt_template, user_text="", lang="zh", model=None):
    """
    流式舞蹈分析。
    参数：
        lang: 'zh' 或 'en'，控制系统指令语言
        model: 可强制指定模型，否则使用 .env 中的默认值
    """
    prompt = prompt_template.replace('{video1_json}', video1_json).replace('{video2_json}', video2_json).replace('{user_text}', user_text)

    # 根据语言设置系统指令
    if lang == "en":
        instructions = "You are a world-class dance instructor, transitions, and key players from data. You must reply in English."
    else:
        instructions = "你是一位世界顶级的舞蹈导师。"

    # 构建消息列表
    messages = [
        {"role": "system", "content": instructions},
        {"role": "user", "content": prompt}
    ]

    # 根据 provider 选择客户端和模型
    provider = os.getenv("LLM_PROVIDER", "openai").lower()

    if provider == "deepseek":
        client = _create_client(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com"
        )
        model_name = model or os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
    elif provider == "gemma4":
        client = _create_client(
            api_key=os.getenv("GEMMA_API_KEY", "ollama"),
            base_url=os.getenv("GEMMA_BASE_URL", "http://localhost:11434/v1")
        )
        model_name = model or os.getenv("GEMMA_MODEL", "gemma2:9b")
    else:  # openai
        client = _create_client(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        )
        model_name = model or os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

    # 带重试的流式输出
    last_error = None
    for attempt in range(3):
        try:
            for chunk in _stream_chat(client, model_name, messages):
                yield chunk
            return
        except Exception as e:
            last_error = e
            if attempt < 2:
                time.sleep(2)
    raise last_error