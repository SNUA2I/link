import streamlit as st
import re
from collections import defaultdict

# 페이지 설정
st.set_page_config(
    page_title="실습 링크",
    page_icon="📚",
    layout="wide"
)

# 비밀번호 설정
PASSWORD = "1111"

# 데이터 준비 함수
def prepare_data():
    """링크 데이터를 파싱하여 카테고리별로 정리합니다."""
    data = """
<<Colab 링크>>
--- 데이터 분석 1 --------------------------------------------------------------
링크가 들어갑니다

<<기타 링크>>
--- 참고 자료 --------------------------------------------------------------
링크가 들어갑니다
    """

    categories = defaultdict(list)
    current_category = None

    lines = data.strip().split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]
        category_match = re.match(r'<<(.+)>>', line)
        if category_match:
            current_category = category_match.group(1).strip()
            i += 1
            continue

        title_match = re.match(r'--- (.+?) -+', line)
        if title_match and current_category:
            title = title_match.group(1).strip()
            content_lines = [line]
            j = i + 1
            while j < len(lines):
                next_line = lines[j]
                if re.match(r'--- .+? -+', next_line) or re.match(r'<<.+>>', next_line):
                    break
                content_lines.append(next_line)
                j += 1
            content = '\n'.join(content_lines)
            categories[current_category].append({
                'title': title,
                'content': content
            })
            i = j
        else:
            i += 1

    return categories

# 비밀번호 확인
def check_password():
    if 'password_verified' not in st.session_state:
        st.session_state.password_verified = False

    if st.session_state.password_verified:
        return True

    st.title("실습 링크")
    st.markdown("A2I 실습 링크 정리")

    password_input = st.text_input(
        "비밀번호를 입력하세요:",
        type="password",
        help="올바른 비밀번호를 입력하면 내용을 볼 수 있습니다."
    )

    if password_input == PASSWORD:
        st.session_state.password_verified = True
        return True
    elif password_input:
        st.error("비밀번호가 일치하지 않습니다.")

    return False

# 프롬프트 표시
def display_prompts():
    categories = prepare_data()
    st.sidebar.title("목차")

    for category, prompts in categories.items():
        st.sidebar.subheader(category)
        for prompt in prompts:
            title = prompt['title']
            anchor = f"{category.replace(' ', '-')}-{title.replace(' ', '-')}"
            st.sidebar.markdown(f"- [{title}](#{anchor})")

    st.title("실습 링크")
    st.markdown("---")

    for category, prompts in categories.items():
        st.header(category)
        for prompt in prompts:
            title = prompt['title']
            content = prompt['content']
            anchor = f"{category.replace(' ', '-')}-{title.replace(' ', '-')}"
            content_lines = content.split('\n')
            actual_content = '\n'.join(content_lines[1:]).strip()
            st.markdown(f"<a name='{anchor}'></a>", unsafe_allow_html=True)
            st.subheader(title)
            st.markdown("```
" + actual_content + "
```")
            st.markdown("---")

# 메인 함수
def main():
    if check_password():
        display_prompts()

if __name__ == "__main__":
    main()
