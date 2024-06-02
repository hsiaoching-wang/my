def apply_modifications(request):
    work = request["word"]
    article = request["content"]

    for task in work:
        modification = modifications.get(task, "")
        if modification:
            article = f"{article}\n\n{modification}"

    return article

# 定义你的结构
structure = [
    {
        "value": "edit or review",
        "label": "Edit or review",
        "children": [
            {"value": "improve writing", "label": "improve writing"},
            {"value": "make shorter", "label": "make shorter"},
            {"value": "simplify language", "label": "simplify language"}
        ]
    },
    {
        "value": "generate form selection",
        "label": "Generate form selection",
        "children": [
            {"value": "summarize", "label": "summarize"},
            {"value": "continue", "label": "continue"}
        ]
    },
    {
        "value": "change tone",
        "label": "Change tone",
        "children": [
            {"value": "profesional", "label": "profesional"},
            {"value": "casual", "label": "casual"},
            {"value": "direct", "label": "direct"},
            {"value": "confident", "label": "confident"},
            {"value": "friendly", "label": "friendly"}
        ]
    },
    {
        "value": "change style",
        "label": "Change style",
        "children": [
            {"value": "busuness", "label": "busuness"},
            {"value": "legal", "label": "legal"},
            {"value": "journalism", "label": "journalism"}
        ]
    },
    {
        "value": "translate",
        "label": "Translate",
        "children": [
            {"value": "translate to English", "label": "translate to English"},
            {"value": "translate to Tradionnal Chinese", "label": "translate to Tradionnal Chinese"},
            {"value": "translate to Simplified Chinese", "label": "translate to Simplified Chinese"},
            {"value": "translate to Japanese", "label": "translate to Japanese"}
        ]
    }
]

# 定义每个节点的文章段落
modifications = {
    "edit or review": (
        "Goal: To receive detailed feedback and edits on the provided article, focusing on improving clarity, coherence, grammar, and overall quality.\n\n"
        "Instructions:\n\n"
        "1. Read the entire article carefully.\n"
        "2. Identify any grammatical errors, including punctuation, spelling, and syntax.\n"
        "3. Evaluate the structure of the article. Ensure that the introduction, body, and conclusion are well-organized and that each section transitions smoothly to the next.\n"
        "4. Check for clarity and coherence. Make sure each paragraph conveys its message clearly and that the ideas flow logically.\n"
        "5. Assess the tone and style. Ensure that the writing style is appropriate for the intended audience and purpose of the article.\n"
        "6. Provide suggestions for improving any weak or unclear sections. If any part of the article is confusing or lacks detail, recommend specific changes or additions.\n"
        "7. Highlight any repetitive content and suggest ways to make the text more concise.\n"
        "8. Ensure factual accuracy. If the article contains any data or factual information, check that it is correct and properly cited.\n\n"
        "Additional Details:\n\n"
        "Include comments or suggestions in the margins or as footnotes.\n"
        "Make direct edits within the text using track changes or a similar feature if possible.\n"
    ),
    "improve writing": "Focus on improving overall readability and engagement of the text.",
    "make shorter": "Summarize each major point in a brief, clear sentence.",
    "simplify language": "Make direct edits within the text using track changes or a similar feature if possible.",
    "generate form selection": "Generating a form selection involves several steps.",
    "summarize": "First, summarize the key points of the text.",
    "continue": "Then, continue with additional relevant information.",
    "change tone": "Changing the tone of the text can alter its impact.",
    "profesional": "For a professional tone, use formal language and avoid slang.",
    "casual": "A casual tone can include contractions and colloquial expressions.",
    "direct": "A direct tone is straightforward and to the point.",
    "confident": "A confident tone conveys certainty and assurance.",
    "friendly": "A friendly tone is warm and approachable.",
    "change style": "Changing the style of the text can make it suitable for different audiences.",
    "busuness": "A business style is formal and focused on professional matters.",
    "legal": "A legal style includes precise terminology and thorough explanations.",
    "journalism": "A journalistic style is clear, concise, and aimed at informing the public.",
    "translate": "Translation involves converting text from one language to another.",
    "translate to English": "Translating to English can make the text accessible to a global audience.",
    "translate to Tradionnal Chinese": "Traditional Chinese is used in Taiwan and Hong Kong.",
    "translate to Simplified Chinese": "Simplified Chinese is used in mainland China.",
    "translate to Japanese": "Japanese translation requires understanding of kanji, hiragana, and katakana."
}
