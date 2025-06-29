import os
import json

from pydub import AudioSegment

import src.llm as llm


def get_snip_path() -> str:
    """
    Get the path to the snips file.
    """

    folder = os.getenv("DATA_FOLDER", "data")
    file = os.environ.get("SNIP_PATH", "snips.json")

    return os.path.join(folder, file)


# Add snip for audio file at specified time
def add_snip(file_name, current_time):
    """
    Add a snip to the list.
    """

    ### Get saved snips or initialize them

    if os.path.exists(get_snip_path()):
        with open(get_snip_path(), "r") as f:
            snips = json.load(f)
    else:
        snips = {}

    if file_name not in snips.keys():
        snips[file_name] = []

    ### Add a new snip position

    snips[file_name].append({
        "snip_time": current_time,
        "snip_summary": ""
    })

    ### Save the updated snips back to the file

    with open(get_snip_path(), "w") as f:
        json.dump(snips, f, indent=4)

    print(f"Snip saved at: {current_time:.2f} seconds")


def process_snips() -> None:
    """
    Process all snips that have no summary yet.
    """

    ### Load the snips from the file

    if os.path.exists(get_snip_path()):
        with open(get_snip_path(), "r") as f:
            snips = json.load(f)
    else:
        snips = {}

    ### Loop over all snips and look for those that have no summary yet

    for file_name, snip_list in snips.items():
        for snip in snip_list:
            if not snip["snip_summary"]:

                print(f"Processing snip at {snip['snip_time']} seconds in file {file_name}")

                # Extract audio around the current time
                audio_segment = AudioSegment.from_mp3(os.path.join(os.getenv("DATA_FOLDER", "data"), file_name))

                start_ms = max((snip["snip_time"] - int(os.getenv("SNIP_DURATION_SECONDS", 60)) / 2) * 1000, 0)
                end_ms = min((snip["snip_time"] + int(os.getenv("SNIP_DURATION_SECONDS", 60)) / 2) * 1000, len(audio_segment))

                # Store snip temporarily
                extract = audio_segment[start_ms:end_ms]
                extract_path = os.path.join(os.getenv("DATA_FOLDER", "data"), f"snip_tmp.mp3")
                extract.export(extract_path, format="mp3")

                # Transcribe the snip using LLM
                transcript = llm.transcribe_with_ai(extract_path)

                # Summarize the snip
                snip["snip_summary"] = llm.summarize_with_ai(transcript)

    ### Save the updated snips back to the file

    with open(get_snip_path(), "w") as f:
        json.dump(snips, f, indent=4)

    print("Snips processed and summaries updated.")

    # Delete the temporary snip file
    if os.path.exists(extract_path):
        os.remove(extract_path)
