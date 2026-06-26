def blog_prompt(topic: str, tone: str, length: str, keywords: str) -> str:
    kw = f"\n必ず以下のキーワードを含めてください: {keywords}" if keywords else ""
    return f"""あなたはプロのブログライターです。以下の条件でブログ記事を日本語で作成してください。

テーマ: {topic}
文体: {tone}
文字数の目安: {length}
{kw}

以下の構成で作成してください:
- タイトル
- リード文（導入）
- 本文（見出しを使って複数セクション）
- まとめ

読者が最後まで読みたくなる、読みやすい記事を作成してください。"""


def email_reply_prompt(original: str, intent: str, tone: str) -> str:
    return f"""あなたはビジネスメールの専門家です。以下のメールへの返信文を日本語で作成してください。

【受信メール】
{original}

【返信の意図・内容】
{intent}

【文体・トーン】
{tone}

件名と本文を含む、適切なビジネスメールの返信を作成してください。
署名は「（署名）」とプレースホルダーで示してください。"""


def summarize_prompt(text: str, length: str, style: str) -> str:
    return f"""以下の文章を{style}で要約してください。
要約の長さ: {length}

【要約する文章】
{text}

重要なポイントを漏らさず、簡潔にまとめてください。"""


def sns_prompt(topic: str, platform: str, tone: str, hashtags: bool) -> str:
    hashtag_instruction = "関連するハッシュタグも5〜10個提案してください。" if hashtags else "ハッシュタグは不要です。"
    limits = {
        "X (Twitter)": "140文字以内",
        "Instagram": "2200文字以内（短めの2〜3段落推奨）",
        "Facebook": "自由（2〜3段落推奨）",
        "LinkedIn": "ビジネス向け、300〜500文字推奨",
    }
    limit = limits.get(platform, "適切な長さ")
    return f"""あなたはSNSマーケティングの専門家です。以下の条件でSNS投稿文を日本語で作成してください。

投稿テーマ: {topic}
プラットフォーム: {platform}（{limit}）
トーン: {tone}

{hashtag_instruction}

エンゲージメントを高める魅力的な投稿文を作成してください。"""


def proofread_prompt(text: str, level: str) -> str:
    levels = {
        "軽微な修正（誤字・脱字のみ）": "誤字・脱字・句読点のみ修正し、文体は変えないでください。",
        "文章改善（読みやすさ向上）": "誤字脱字の修正に加え、読みやすさを改善してください。文章の流れや表現を自然にしてください。",
        "大幅リライト（内容強化）": "内容はそのままに、プロのライターとして文章を大幅に改善・強化してください。",
    }
    instruction = levels.get(level, levels["文章改善（読みやすさ向上）"])
    return f"""以下の文章を校正・改善してください。
修正レベル: {level}
指示: {instruction}

【元の文章】
{text}

以下の形式で出力してください:
## 修正後の文章
（改善した文章をここに）

## 主な変更点
（変更した箇所と理由を箇条書きで）"""


def title_prompt(content: str, count: int, style: str) -> str:
    return f"""あなたはコピーライターの専門家です。以下の内容に対して、魅力的な{style}を{count}個考えてください。

【内容・テーマ】
{content}

クリックしたくなる、印象に残る、内容を的確に表すタイトル・見出しを提案してください。
番号付きリストで出力してください。"""
