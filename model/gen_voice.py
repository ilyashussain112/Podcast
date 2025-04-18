import edge_tts
from edge_tts import Communicate


class Voice:

    def __init__(self):
        pass
    async def generate_edge_voice(self,text, path):
        print("🔍 type of text:", type(text), " | value:", text)

        communicate = edge_tts.Communicate(text, voice="en-GB-RyanNeural")
        await communicate.save(path)