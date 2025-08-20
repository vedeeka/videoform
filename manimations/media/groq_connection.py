from openai import OpenAI

# Initialize client with your API key
client = OpenAI(api_key="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")

# Example: Chat completion
response = client.chat.completions.create(
    model="gpt-4o-mini",  # or gpt-4.1, gpt-4o, etc.
    messages=[
        {"role": "system", "content": " from manim import * You are a helpful assistant.i want complete minim  just the code to explain cell structure ."},
      
    ]
)

print(response.choices[0].message.content)
