def generate_reply_draft(subject: str, body: str) -> str:
    """
    メール本文を解析し、返信文を生成するダミー関数。
    実際には OpenAI API などを利用する。
    """
    # TODO: 後でAI連携に差し替え
    draft = f"""件名: Re: {subject}

いつもお世話になっております。

ご連絡ありがとうございます。以下について確認いたしました。
{body[:80]}...

詳細については追ってご連絡いたします。
よろしくお願いいたします。
"""
    return draft

