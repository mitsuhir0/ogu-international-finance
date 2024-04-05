import streamlit as st
import datetime

from datetime import datetime

def extract_title(string: str) -> list[str]:
    # カッコの位置を探す
    left_paren = string.index("(")
    right_paren = string.index(")")

    # カッコ以前の文字列とカッコ内の文字列を取り出す
    before = string[:left_paren].strip()
    inside = string[slice(left_paren+1, right_paren)]

    return [before, inside]

today = datetime.today()
st.title("国際金融論B 参考資料")
st.write(f"{today.year}-{today.month}-{today.day}")
