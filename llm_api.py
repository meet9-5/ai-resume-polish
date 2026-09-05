import requests
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()
API_KEY = os.getenv("ZHIPU_API_KEY")
API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"


def polish_resume(resume_text: str, style: str = "简洁干练", timeout: int = 15):
    """
    调用智谱AI接口做简历润色
    :param resume_text: 用户原始简历文本
    :param style: 润色风格
    :param timeout: 请求超时时间
    :return: 元组 (code, msg, data)
    """
    if not API_KEY:
        return 500, "未配置ZHIPU_API_KEY环境变量", ""

    prompt = f"""你是专业简历优化师，按照{style}的风格润色以下简历内容，优化表述、提升专业度，保留原有信息，不要编造经历：
{resume_text}
"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "glm-4-flash",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3
    }

    try:
        resp = requests.post(API_URL, headers=headers, json=payload, timeout=timeout)
        resp.raise_for_status()
        result = resp.json()
        polished = result["choices"][0]["message"]["content"]
        return 200, "成功", polished

    except requests.exceptions.Timeout:
        return 500, "接口请求超时，请稍后重试", ""
    except Exception as e:
        print(f"大模型调用出错：{e}")
        return 500, "服务器异常", ""