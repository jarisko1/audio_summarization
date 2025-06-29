import os
from dotenv import load_dotenv

from openai import AzureOpenAI


def get_ai_client() -> AzureOpenAI:
    """
    Sets up the Azure OpenAI client with the necessary credentials.
    """

    load_dotenv()

    return AzureOpenAI(
        azure_endpoint=os.environ["AZURE_URI"],
        api_key=os.environ["AZURE_TOKEN"],
        api_version=os.environ.get("AZURE_API_VERSION"),
    )


def transcribe_with_ai(audio_file_path: str) -> str:
    """
    Transcribes the given audio file using an AI model.
    """

    client = get_ai_client()

    with open(audio_file_path, "rb") as audio_file:

        transcription = client.audio.transcriptions.create(
            file=audio_file,
            model=os.getenv("TRANSCRIPTION_MODEL", "whisper"),
        )

    return transcription.text


def summarize_with_ai(text:str) -> str | None:
    """
    Summarizes the given text using an AI model.
    """

    client = get_ai_client()

    # Summarize text
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Summarize the following text. "
                        "Focus on practical information, key points, and actionable insights. "
                        "Ignore any personal opinions, anecdotes, or irrelevant details. "
                        "Do not add introductory phrases like 'In this text' or 'The text discusses'. "
                        "Do not mention that this is a summary. "
                        "Do not mention anything, that will stand out if I connect multiple summaries together. "
                        "Do not format the text in any way, just produce plain text without any formatting. "
                        "Be very concise and to the point. "
                        "Extract only 1-2 key lessons. "
            },
            {
                "role": "user",
                "content": text,
            }
            ],
        temperature=1.0,
        top_p=1.0,
        model=os.environ.get("SUMMARIZATION_MODEL", "gpt-4.1"),
    )

    return response.choices[0].message.content
