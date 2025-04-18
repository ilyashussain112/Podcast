from api_key import APi


client = APi().api()
class Ask:
    def __init__(self):
        pass

    def ask_groq(self, prompt, user_input,model="gemma2-9b-it"):
        try:
            messages = [
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_input}
            ]

            chat = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7
            )
        except:
            print("❌ Groq API Error:")
            return None


        return chat.choices[0].message.content
