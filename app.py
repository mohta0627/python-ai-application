import streamlit as st
from utils.gemini_client import generate
from utils.prompts import (
    blog_prompt,
    email_reply_prompt,
    summarize_prompt,
    sns_prompt,
    proofread_prompt,
    title_prompt,
)

st.set_page_config(
    page_title="AI ライティングツール",
    page_icon="✍️",
    layout="wide",
)

# ---- サイドバー: APIキー設定 ----
with st.sidebar:
    st.title("⚙️ 設定")
    api_key_input = st.text_input(
        "Gemini API キー",
        type="password",
        placeholder="AIza...",
        help="Google AI Studio からAPIキーを取得してください",
    )
    if api_key_input:
        st.session_state["gemini_api_key"] = api_key_input
        st.success("APIキーが設定されました")
    elif st.session_state.get("gemini_api_key"):
        st.success("APIキーが設定済みです")
    else:
        st.warning("APIキーを入力してください")

    st.divider()
    st.caption("Powered by Gemini 2.0 Flash")

# ---- メインUI ----
st.title("✍️ AI ライティングツール")
st.caption("Gemini AIがあなたの文章作成をサポートします")

tool = st.selectbox(
    "使用するツールを選択",
    [
        "📝 ブログ記事作成",
        "📧 メール返信文作成",
        "📋 文章要約",
        "📱 SNS投稿文作成",
        "🔍 文章校正・改善",
        "💡 タイトル・見出し生成",
    ],
    label_visibility="collapsed",
)

st.divider()

# ---- ブログ記事作成 ----
if tool == "📝 ブログ記事作成":
    st.subheader("📝 ブログ記事作成")
    st.caption("テーマや条件を入力すると、SEOを意識した読みやすいブログ記事を生成します")

    col1, col2 = st.columns(2)
    with col1:
        topic = st.text_area("記事のテーマ・内容 *", placeholder="例: 初心者向けPythonプログラミング入門", height=100)
        keywords = st.text_input("含めたいキーワード（任意）", placeholder="例: Python, 入門, 初心者")
    with col2:
        tone = st.selectbox("文体", ["親しみやすい・カジュアル", "丁寧・フォーマル", "情報的・客観的", "熱意・エネルギッシュ"])
        length = st.selectbox("文字数の目安", ["1000〜1500文字", "1500〜2000文字", "2000〜3000文字", "3000文字以上"])

    if st.button("記事を生成する", type="primary", use_container_width=True):
        if not topic:
            st.error("テーマを入力してください")
        else:
            with st.spinner("記事を生成中..."):
                result = generate(blog_prompt(topic, tone, length, keywords))
            if result:
                st.success("生成完了！")
                st.markdown(result)
                st.download_button("テキストをダウンロード", result, file_name="blog_article.txt", mime="text/plain")

# ---- メール返信文作成 ----
elif tool == "📧 メール返信文作成":
    st.subheader("📧 メール返信文作成")
    st.caption("受信したメールを貼り付けると、適切な返信文を作成します")

    original = st.text_area("受信メールの内容 *", placeholder="ここに返信したいメールの内容を貼り付けてください", height=200)
    col1, col2 = st.columns(2)
    with col1:
        intent = st.text_area("返信の意図・伝えたいこと *", placeholder="例: 来週の会議に参加できない旨を伝え、別日程を提案したい", height=100)
    with col2:
        tone = st.selectbox("文体・トーン", ["丁寧なビジネス文体", "カジュアルな敬語", "フォーマル（社外向け）", "社内向け・簡潔に"])

    if st.button("返信文を生成する", type="primary", use_container_width=True):
        if not original or not intent:
            st.error("メールの内容と返信の意図を入力してください")
        else:
            with st.spinner("返信文を生成中..."):
                result = generate(email_reply_prompt(original, intent, tone))
            if result:
                st.success("生成完了！")
                st.markdown(result)
                st.download_button("テキストをダウンロード", result, file_name="email_reply.txt", mime="text/plain")

# ---- 文章要約 ----
elif tool == "📋 文章要約":
    st.subheader("📋 文章要約")
    st.caption("長い文章を貼り付けると、要点を整理して簡潔にまとめます")

    text = st.text_area("要約したい文章 *", placeholder="ここに要約したい文章を貼り付けてください", height=250)
    col1, col2 = st.columns(2)
    with col1:
        length = st.selectbox("要約の長さ", ["3〜5行の短い要約", "100〜200文字", "200〜400文字", "箇条書き5〜10項目"])
    with col2:
        style = st.selectbox("要約スタイル", ["簡潔な文章", "箇条書き", "見出し付きの構造化まとめ", "小学生にもわかる言葉で"])

    if st.button("要約する", type="primary", use_container_width=True):
        if not text:
            st.error("要約する文章を入力してください")
        else:
            with st.spinner("要約中..."):
                result = generate(summarize_prompt(text, length, style))
            if result:
                st.success("生成完了！")
                st.markdown(result)
                st.download_button("テキストをダウンロード", result, file_name="summary.txt", mime="text/plain")

# ---- SNS投稿文作成 ----
elif tool == "📱 SNS投稿文作成":
    st.subheader("📱 SNS投稿文作成")
    st.caption("各プラットフォームに最適化した投稿文を生成します")

    col1, col2 = st.columns(2)
    with col1:
        topic = st.text_area("投稿のテーマ・内容 *", placeholder="例: 新しいカフェをオープンした告知、週末の旅行レポート", height=100)
        platform = st.selectbox("プラットフォーム", ["X (Twitter)", "Instagram", "Facebook", "LinkedIn"])
    with col2:
        tone = st.selectbox("トーン", ["フレンドリー・親しみやすい", "プロフェッショナル", "ユーモア・面白い", "感動的・共感を呼ぶ", "情報提供・教育的"])
        hashtags = st.checkbox("ハッシュタグを提案してもらう", value=True)

    if st.button("投稿文を生成する", type="primary", use_container_width=True):
        if not topic:
            st.error("投稿のテーマを入力してください")
        else:
            with st.spinner("投稿文を生成中..."):
                result = generate(sns_prompt(topic, platform, tone, hashtags))
            if result:
                st.success("生成完了！")
                st.markdown(result)
                st.download_button("テキストをダウンロード", result, file_name="sns_post.txt", mime="text/plain")

# ---- 文章校正・改善 ----
elif tool == "🔍 文章校正・改善":
    st.subheader("🔍 文章校正・改善")
    st.caption("書いた文章を貼り付けると、誤字脱字の修正から文章の改善まで行います")

    text = st.text_area("校正・改善したい文章 *", placeholder="ここに校正・改善したい文章を貼り付けてください", height=250)
    level = st.radio(
        "修正レベル",
        ["軽微な修正（誤字・脱字のみ）", "文章改善（読みやすさ向上）", "大幅リライト（内容強化）"],
        horizontal=True,
    )

    if st.button("校正・改善する", type="primary", use_container_width=True):
        if not text:
            st.error("校正する文章を入力してください")
        else:
            with st.spinner("校正・改善中..."):
                result = generate(proofread_prompt(text, level))
            if result:
                st.success("生成完了！")
                st.markdown(result)
                st.download_button("テキストをダウンロード", result, file_name="proofread.txt", mime="text/plain")

# ---- タイトル・見出し生成 ----
elif tool == "💡 タイトル・見出し生成":
    st.subheader("💡 タイトル・見出し生成")
    st.caption("記事やコンテンツの内容を入力すると、魅力的なタイトルや見出しを提案します")

    col1, col2 = st.columns(2)
    with col1:
        content = st.text_area("記事・コンテンツの内容 *", placeholder="例: Pythonを使ったWebスクレイピングの入門記事。初心者向けで、requests と BeautifulSoup の使い方を解説する", height=150)
    with col2:
        style = st.selectbox("生成するタイトルのスタイル", [
            "ブログ記事タイトル（SEO重視）",
            "ブログ記事タイトル（クリック重視）",
            "メールの件名",
            "SNS投稿タイトル",
            "プレゼン・資料タイトル",
        ])
        count = st.slider("提案する数", min_value=3, max_value=10, value=5)

    if st.button("タイトルを生成する", type="primary", use_container_width=True):
        if not content:
            st.error("内容を入力してください")
        else:
            with st.spinner("タイトルを生成中..."):
                result = generate(title_prompt(content, count, style))
            if result:
                st.success("生成完了！")
                st.markdown(result)
                st.download_button("テキストをダウンロード", result, file_name="titles.txt", mime="text/plain")
