# New use case - Audio player with AI generated notes
Play local files and press button when you want AI to generate summary of that part of the audio.

## Currently implemented
- Very basic Python audio player with button that triggers note creation
- Transcription and summarization of the note via Azure AI

## Goal
Android application that will allow offline listening to downloaded podcasts and will locally save user-selected interest points in the podcasts.
Once connected to the internet, summary of the selected interest points will be generated.

---

# Sumarize content of an audio file
Place the mp3 file to `data` folder and execute the notebook `summarize_audio.ipynb`.
At this moment, whole process is covered in that notebook, including Python libraries and there is no `requirements.txt` file.

## Transcription
Transcription is done via local Whisper model. It requires 7GB of VRAM. As the transcription is usually fine on first go, it is cached to `transcription.json` file, what allows repeated summarization later.

## Summarization
Summarization is done via remote GPT-4.1 model hosted on Azure via free GitHub models. Place `GITHUB_TOKEN` with read authorization on Models into `.env` file.
You can specify topics of interest you want to see in the summary.
Each transcription is split with overlap to fit the 8K token context window of free GitHub models.
Summaries from all chunks from a single audio files are collected together and stored in markdown file the the same name.

### Notes
Specific summarization model (BART) was tested but did not produce good result due to small context window and no options to make the summary creation customizable.
