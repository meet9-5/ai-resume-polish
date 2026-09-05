from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
# 导入抽出去的大模型函数
from llm_api import polish_resume

load_dotenv()
API_KEY = os.getenv("ZHIPU_API_KEY")

# 密钥校验
if not API_KEY:
    raise ValueError("请在项目根目录新建.env文件并配置ZHIPU_API_KEY")

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/polish", methods=["POST"])
def polish():
    try:
        resume_text = request.json.get("resume_text", "").strip()
        style = request.json.get("style", "简洁干练")

        if not resume_text:
            return jsonify({"code": 400, "msg": "请输入简历内容", "data": ""})

        # 调用llm_api里面的函数
        code, msg, data = polish_resume(resume_text, style)
        return jsonify({"code": code, "msg": msg, "data": data})

    except Exception as e:
        print(f"接口出错：{e}")
        return jsonify({"code": 500, "msg": "服务器异常", "data": ""})


if __name__ == "__main__":
    app.run(debug=True)