from google.cloud import texttospeech
from bs4 import BeautifulSoup
import pandas as pd
import requests
import re


def scrappy():
    # Scrape the website and get list of titles
    url = 'https://www.bbc.com/afrique/popular/read'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    titles = soup.findAll('span', {'class': 'most-popular-list-item__headline'})

    # text cleaning
    result = []
    for title in titles:
        title = re.sub(r'[^\w\s]','',title.text)
        words = title.split()
        result += words

    # Return the unique words
    return set(result)

def audiofy(text, language='fr-CA'):
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.types.SynthesisInput(text=text)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.types.VoiceSelectionParams(language_code='fr-CA',ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)

    # Select the type of audio file you want returned
    audio_config = texttospeech.types.AudioConfig(audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(synthesis_input, voice, audio_config)

    # The response's audio_content is binary.
    with open('audio/{}.mp3'.format(text), 'wb') as out:
        # Write the response to the output file.
        out.write(response.audio_content)



if __name__ == "__main__":
    # Get list of french words and get the audio for each word
    words = scrappy()

    for word in words:
        audiofy(word)

    # Create the dataframe of words and save it as .csv file
    dictionary = pd.DataFrame(words, columns=['word'])
    dictionary.to_csv('dictionary.csv', index=False)
