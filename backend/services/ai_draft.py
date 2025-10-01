import os
from openai import OpenAI

def generate_reply_draft(subject: str, body: str) -> str:
    """
    メール本文を解析し、返信文を生成する関数。
    OpenAI APIを利用して自然な返信文を生成します。
    """
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        # API Keyが設定されていない場合はダミー返信を返す
        return f"""件名: Re: {subject}

いつもお世話になっております。

ご連絡ありがとうございます。以下について確認いたしました。
{body[:80]}...

詳細については追ってご連絡いたします。
よろしくお願いいたします。
"""

    try:
        client = OpenAI(api_key=api_key)

        prompt = f"""以下のメールに対して、日本のビジネスマナーに適した丁寧な返信文を作成してください。

件名: {subject}
本文:
{body}

返信文の要件:
- 日本のビジネス文書として適切な敬語を使用
- 簡潔で分かりやすい内容
- 件名は「Re: {subject}」で始める
- 具体的な回答が難しい場合は、確認して後日連絡する旨を記載"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "あなたは日本のビジネスメール作成のエキスパートです。丁寧で適切な返信文を作成してください。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        # エラーが発生した場合はダミー返信を返す
        print(f"OpenAI API error: {e}")
        return f"""件名: Re: {subject}

いつもお世話になっております。

ご連絡ありがとうございます。いただいた内容について確認いたします。

詳細については追ってご連絡いたします。
よろしくお願いいたします。
"""

