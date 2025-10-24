from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# --- 画面タイトルとアプリ説明 ---
st.title("LLM相談アプリ")
st.write("1) 専門家の役割を選ぶ → 2) 相談内容を入力 → 3) 送信ボタンを押す、の順に操作してください。")

st.divider()

# --- 専門家の役割選択（A/Bでシステムメッセージを切り替え） ---
selected_expert = st.radio(
    "専門家の役割を選択してください（A/B）",
    ["ファッションスタイリスト（A）", "経営戦略コンサルタント（B）"]
)

# --- 入力欄 ---
user_text = st.text_input(
    label="相談内容を入力してください（できるだけ具体的に）",
    placeholder="例：フォーマルな場にふさわしいコーディネートを教えてください。"
)

# --- LLM呼び出し関数（要件：入力テキストと選択値を引数に取り、回答を返す） ---
def generate_answer(user_text, selected_expert):

    # 選択された専門家に応じてシステムメッセージを切り替え
    if selected_expert == "ファッションスタイリスト（A）":
        system_msg = (
            "あなたは優秀なファッションスタイリストです。"
            "相手の体型・TPO・季節・予算を想定し、理由と代替案も添えて、"
            "具体的なアイテム例（トップス/ボトムス/靴/小物）まで提案してください。"
            "回答は日本語で、箇条書きを中心に簡潔に。"
        )
    else:
        system_msg = (
            "あなたは有能な経営戦略コンサルタントです。"
            "課題の構造化（現状→課題→原因→打ち手→KPI）で整理し、"
            "優先度・期待効果・リスクと代替案も提示してください。"
            "回答は日本語で、見出しと箇条書きを用いて論理的に。"
        )


    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    messages = [
        SystemMessage(content=system_msg),
        HumanMessage(content=user_text)
    ]

    try:
        result = llm.invoke(messages)
        return result.content
    except Exception as e:
        return f"LLM呼び出し中にエラーが発生しました: {e}"

# --- 送信ボタン ---
if st.button("送信"):
    st.divider()
    if user_text:
        answer = generate_answer(user_text, selected_expert)
        st.write("**回答**")
        st.write(answer)
    else:
        st.error("相談内容を入力してから「送信」ボタンを押してください。")

# --- 注意書き ---
st.divider()
st.write("※ 個人情報や機密情報の入力は避けてください。出力内容の最終判断はご自身で行ってください。")