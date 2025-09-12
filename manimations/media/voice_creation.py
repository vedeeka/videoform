
from murf import Murf

client = Murf(api_key="ap2_84591270-911e-42af-a056-2806ecf5653e")

response = client.text_to_speech.generate(
  text = "In this experiential elearning module, you’ll master the basics of using this Text to Speech widget. Choose a voice, experiment with styles, explore languages, customize text, and play with various use-cases for a view into all that Murf offers.",
  voice_id = "en-US-natalie"
)

print(response.audio_file)
