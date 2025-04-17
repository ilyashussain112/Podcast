from src.loading import Load
from model.model_loading import Ask
from prompts import Prompts
from model.gen_voice import Voice

import fitz 
import os 
import asyncio
import ast
from pydub import AudioSegment
import imageio_ffmpeg
AudioSegment.converter = imageio_ffmpeg.get_ffmpeg_exe() 
from gtts import gTTS
from pydub import AudioSegment


# import files

voice = Voice()
generate_edge_voice = voice.generate_edge_voice

prompt = Prompts()
SYS_PROMPT, SYSTEM_PROMPT, SYSTEM_PROMPT2 = prompt.get_all()

ask = Ask()
ask_groq = ask.ask_groq

load = Load()
extract_text_from_pdf = load.extract_text_from_pdf

class Poadcast:
    def __init__(self):
        pass
    def generate_podcast_from_pdf(self,pdf_path, chunk_size=5):  # Process 5 pages per chunk
        doc = fitz.open(pdf_path)
        total_pages = len(doc)

        all_cleaned_text = ""  # Store cleaned text from all chunks

        for i in range(0, total_pages, chunk_size):
            start = i
            end = min(i + chunk_size, total_pages)
            print(f"Processing pages {start}-{end}...")

            raw_text = extract_text_from_pdf(pdf_path, start, end)
            cleaned = ask_groq(SYS_PROMPT, raw_text)
            all_cleaned_text += cleaned  # Accumulate cleaned text

        print("🧹 Cleaning text (Prompt 1)...")

        cleaned = all_cleaned_text # Assign the complete cleaned text

        print("✍️ Writing podcast script (Prompt 2)...")
        scripted = ask_groq(SYSTEM_PROMPT, cleaned)

        print("🎭 Rewriting for TTS (Prompt 3)...")
        final_script_raw = ask_groq(SYSTEM_PROMPT2, scripted)

        try:
            dialogue_list = ast.literal_eval(final_script_raw)
        except Exception as e:
            print("⚠️ Could not parse Groq response:", e)
            print("Here’s what it returned:\n", final_script_raw)
            return

        print("🎙️ Generating audio...")
        os.makedirs("audio", exist_ok=True)
        final_podcast = AudioSegment.empty()

        for i, (speaker, line) in enumerate(dialogue_list):
            path = f"audio/{speaker.lower().replace(' ', '_')}_{i}.mp3"

            if speaker.lower() == "speaker 1":
                tts = gTTS(line, lang='en', tld='com')
                tts.save(path)
            else:
                asyncio.run(generate_edge_voice(line, path))

            audio = AudioSegment.from_mp3(path)
            final_podcast += audio + AudioSegment.silent(duration=300)

        final_podcast.export("podcast_episode.mp3", format="mp3")
        print("✅ Podcast Ready!")
        print("🔊 Saved as: podcast_episode.mp3. You can play it from your file explorer.")

if __name__ == "__main__":
    podcast = Poadcast()
    podcast.generate_podcast_from_pdf("Attention-Is-All-You-Need.pdf")
