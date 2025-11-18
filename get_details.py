"""
Ask Gemini to provide all the details of content in a formatted way that'll be then saved into a "details.json" file.
"""

import google.generativeai as genai
from personal_data import gemini_api_key as api_key  # GET YOUR OWN KEY (╯▔皿▔)╯
import json
import os


genai.configure(api_key=api_key)  # GET YOUR OWN KEY :D
model = genai.GenerativeModel(model_name='gemini-2.5-flash')

base_prompt = """Give me the following pieces of data about the media/content I will inform you of shortly.

I need the:
Title
Author(s) (give me only one if there are way too many, you can also give me two with a '&' between them)
Artist(s) (GIVE ME THE NAME OF THE STUDIO(s) THAT PRODUCED THE CONTENT)
Description (or like a spoiler-less synopsis) (ONLY IN ONE LINE, TRY TO MAKE IT LOOK LIKE AN OFFICIAL SYNOPSIS)
A list of Genres (like a minimum of 4 and a maximum of like 15, depends of what you think is suitable SEPARATED BY COMMAS, ON ONE LINE)
Status number, (0 = Unknown, 1 = Ongoing, 2 = Completed, 3 = Licensed, 4 = Publishing finished, 5 = Cancelled, 6 = On hiatus) Most of the time it's gona be a number 2

I need you to send this data in a well formatted way LINE BY LINE just like this:

TITLE
AUTHOR
ARTIST
DESCRIPTION
GENRES
STATUS

Exxample of what you could end up sending me:

Attack On Titan
Hajime Isayama
Wit Studio & MAPPA
Attack on Titan is a dark fantasy anime series where humanity is on the brink of extinction, forced to live within walled cities to protect themselves from giant, humanoid creatures called Titans that devour humans. The story follows Eren Yeager, who vows revenge after a Titan breach destroys his hometown and kills his mother. He joins the military to fight the Titans and uncover their origins, along with his childhood friends Mikasa Ackerman and Armin Arlert. The series explores themes of survival, freedom, and the nature of humanity as Eren and his comrades confront not only the Titans but also the complex secrets of their world.
Action, Dark, Fantasy, Super Natural, Post-apocaliptic, Horror, Mystery
2


STICK TO THIS FORMAT VERY VERY STRICTLY BECAUSE YOUR RESPONSE WILL BE USED BY A PROGRAM THAT WILL USE THIS DATA TO BUILD A "details.json" FILE AND IT CANNOT ACCEPT ANY OTHER FORMAT TO FUNCTION
YOU MUST SEND ONLY 6 LINES OF TEXT. DO NOT INCLUDE ANYTHING ELSE IN YOUR RESPONSE AT ALL.

MAKE SURE YOU STICK TO WHAT YOU FIND ON THE WEB. DONT GUESS OR ASSUME WRITERS OR ARTISTS/STUDIOS ON YOUR OWN. EVERYTHING YOU MUST BE SURE OF 100%."""

def ask_prompt(content_name, extra):
    if extra:
        guide = f"{content_name}   Extra information that could help you: {extra}"
    else:
        guide = f"{content_name}"
        print(guide)
    added_piece = f"""The content you will be filling the details in for is:
{guide}

IF YOU FEEL LIKE THERE HAS BEEN A PROBLEM WITH THE GIVEN INFORMATION AND YOU CANNOT FORMULATE THE DETAILS WANTED, THEN SEND THE WORD, FULLY CAPITALIZED, "ISSUE" THEN SKIP A LINE AND IF YOU WOULD LIKE TO ELABORATE ON WHY YOU CANNOT GET THE DETAILS THEN SAY WHAT WENT WRONG BELOW THE "ISSUE". Thanks in advance"""

    prompt = f"""{base_prompt}
    
    {added_piece}"""

    response = model.generate_content(prompt)

    return response.text


#todo: find a way to link folder path of desired content with json creation below

# def create_json():
#     try:
#         file_path = os.path.join(main_folder, "details.json")
#         with open(file_path, "w", encoding="utf-8") as f:
#             json.dump(data, f, ensure_ascii=False, indent=2)
#     except Exception as e:
#         print(f"ERROR: {e}")
#
#   data = {
#               "title": title,
#               "author": author,
#               "artist": artist,
#               "description": description,
#               "genre": genres,
#               "status": str(status_index),
#               "_status values": [
#                   "0 = Unknown",
#                   "1 = Ongoing",
#                   "2 = Completed",
#                   "3 = Licensed",
#                   "4 = Publishing finished",
#                   "5 = Cancelled",
#                   "6 = On hiatus"
#               ]
#           }

def run_demo():
    print("DEMO")
    content_name = input("Content Name: ")
    extra_in = input("Extra Information: ")
    if extra_in == "":
        extra = None
    else:
        extra = f"EXTRA DETAILS TO HELP YOU: {extra_in}"
    details_txt = ask_prompt(content_name, extra)

    print()
    print("Details:")
    print(details_txt)


if __name__ == "__main__":
    run_demo()