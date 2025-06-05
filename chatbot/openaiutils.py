import os
from openai import OpenAI

class ManualEnableException(Exception):
    """A simple custom exception."""
    pass  # No need for __init__ or __str__ unless you need more customization


KEY = "OpenAI key"

"Answer the following alexa prompt. if there are multiple possible answers, give the possible answers. Give only the answers. Text: 'To get started, you can get a quote, listen to the daily briefing, or get an account summary'"

response_kill_list = [
    "<Audio only response>",
    "sorry, I'm having trouble understanding right now",
]




def determine_if_question(client, chat_text):

    if any(item in chat_text for item in response_kill_list):
        return "Neither"
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"""Please analyze the following text and identify if it contains a question or instruction, or if neither is present. If a question or instruction is found, return both the classification ('Question' or 'Instruction') and the relevant sentence. If neither is present, return 'Neither'.

Question: A sentence that asks for information, typically ending with a question mark.
Instruction: A sentence that directs someone to do something, often using an imperative verb.
Neither: A sentence that is neither a question nor an instruction.
Provide your result in the following format:

Classification: ('Question', 'Instruction', or 'Neither')
Relevant sentence (or 'Neither' if no question or instruction is found).
If no question or instruction is found, return 'Neither'."

Example 1:
Text: "What time does the meeting start? I will be there soon."

Output:

Classification: 'Question'
Relevant Sentence: "What time does the meeting start?"
Explanation: This sentence is a question asking for information.

Example 2:
Text: "Please email me the report. Let me know if you need anything."

Output:

Classification: 'Instruction'
Relevant Sentence: "Please email me the report."
Explanation: This sentence is an instruction requesting the action of emailing the report.

Example 3:
Text: "It was a great day yesterday."

Output:

Classification: 'Neither'
Relevant Sentence: 'Neither'
Explanation: This is a statement providing information, not a question or instruction.

Example 4:
Text: "Can you help me with this? I will wait here."

Output:

Classification: 'Question'
Relevant Sentence: "Can you help me with this?"
Explanation: This is a question asking for assistance.

Now analyze the following text: {chat_text}"""
    ,
            }
        ],
        model="gpt-4o",
    )
    
    # Skip audio responses not handled by the developer portal
    if "<Audio only response>"in chat_text:
        return "Neither"
    
    return parse_determine_if_question(chat_completion)

def generate_alexa_answers(client, chat_text):

    #Automatically re anable skills.
    line = "Do you want to enable it again?"
    if line in chat_text:
            return(["Yes"])
    line2 = "please take a look to enable."
    if line2 in chat_text:
        raise ManualEnableException
    
    is_question = determine_if_question(client, chat_text)
    if "classification: 'question'" in is_question.lower() or "classification: 'instruction'" in is_question.lower() or "is a question" in is_question.lower() or "is an instruction" in is_question.lower():
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"Provide the answer(s) to the following Alexa prompt. If there are multiple possible answers, list all the possible answers, separated by semicolons. Provide only the answers and nothing else. Answers should be in a single line with no extra explanation or formatting. Text: {chat_text}"
        ,
                }
            ],
            model="gpt-4o",
        )
        return parse_generated_alexa_answers(chat_completion)
    else: 
        # return no good answer
        return ["nga"]

def parse_generated_alexa_answers(response):
    """Parses the response from OpenAI's Chat Completions API."""

    messages = []
    for choice in response.choices:
        message = choice.message
        messages.append({
            "role": message.role,
            "content": message.content
        })
    return messages[0]["content"].split(";")


def parse_determine_if_question(response):
    """Parses the response from OpenAI's Chat Completions API."""

    messages = []
    for choice in response.choices:
        message = choice.message
        messages.append({
            "role": message.role,
            "content": message.content
        })
    return messages[0]["content"]