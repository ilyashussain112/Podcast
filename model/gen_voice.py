import edge_tts


class Voice:
    def __init__(self):
        pass
    async def generate_edge_voice(text, filename):
        communicate = edge_tts.Communicate(text, voice="en-GB-RyanNeural")
        await communicate.save(filename)

