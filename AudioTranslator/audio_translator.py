import os
import requests
import json
import base64
from pydub import AudioSegment
from pydub.playback import play
from io import BytesIO
import sacrebleu
from rouge_score import rouge_scorer
import pyttsx3

# Load API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")

# Transcribe audio to text using Whisper
def transcribe_audio_with_whisper(audio_path, language="English"):
    url = "https://api.openai.com/v1/audio/transcriptions"
    headers = {"Authorization": f"Bearer {api_key}"}
    files = {"file": open(audio_path, "rb")}
    data = {"model": "whisper-1", "language": language}
    response = requests.post(url, headers=headers, files=files, data=data)
    if response.status_code == 200:
        return response.json()["text"]
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

# Translate text using GPT-4
def translate_text(text, target_language="Hindi"):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    prompt = (
        f"Translate the following text from English to {target_language}, "
        "keeping the terms 'Turbo', 'OpenAI', 'token', 'GPT', 'Dall-e', 'Python' in English:\n\n"
        f"{text}"
    )
    data = {
        "model": "gpt-4",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

# Convert text to speech and save as audio
def text_to_speech(text, output_audio_path="dubbed_audio.wav"):
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 25)
    voices = engine.getProperty('voices')
    hindi_voice = None
    for voice in voices:
        if 'hindi' in voice.name.lower() or 'hi' in voice.languages:
            hindi_voice = voice.id
            break
    if hindi_voice:
        engine.setProperty('voice', hindi_voice)
    else:
        print("Hindi voice not found. Using default voice.")
    engine.save_to_file(text, output_audio_path)
    engine.runAndWait()
    print(f"Audio saved to {output_audio_path}")
    return output_audio_path

# Evaluate translation quality using BLEU and ROUGE scores
def evaluate_translation(reference_text, candidate_text):
    bleu = sacrebleu.corpus_bleu([candidate_text], [[reference_text]])
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)
    scores = scorer.score(reference_text, candidate_text)
    results = {
        "BLEU": bleu.score,
        "ROUGE-1": scores['rouge1'].fmeasure,
        "ROUGE-L": scores['rougeL'].fmeasure
    }
    print("Evaluation Results:")
    print("-------------------")
    for metric, score in results.items():
        print(f"{metric} Score: {score:.2f}")
    print("-------------------\n")
    return results

# Interpret BLEU and ROUGE scores
def interpret_scores(bleu, rouge1, rougeL):
    print("Interpreting BLEU Score:")
    if bleu < 10:
        print("Score indicates poor quality translation; significant errors and lack of fluency.")
    elif 10 <= bleu < 20:
        print("Score indicates low quality; understandable in parts but contains many errors.")
    elif 20 <= bleu < 30:
        print("Score indicates fair quality; conveys the general meaning but lacks precision and fluency.")
    elif 30 <= bleu < 40:
        print("Score indicates good quality; understandable and relatively accurate with minor errors.")
    elif 40 <= bleu < 50:
        print("Score indicates very good quality; accurate and fluent with very few errors.")
    else:
        print("Score indicates excellent quality; closely resembles human translation.")
    print()
    print("Interpreting ROUGE-1 Score:")
    if 0.5 <= rouge1 <= 0.6:
        print("Score is generally considered good for unigram overlap.")
    else:
        print("ROUGE-1 score interpretation depends on the specific task domain.")
    print()
    print("Interpreting ROUGE-L Score:")
    if 0.4 <= rougeL <= 0.5:
        print(
            "Score is often regarded as good, reflecting the model's ability to capture the structure of the reference text.")
    else:
        print("ROUGE-L score interpretation depends on the specific task domain.")
    print()

# Main process for audio translation and evaluation
def main():
    source_audio_path = "Test.wav"
    glossary_terms = "Turbo, OpenAI, token, GPT, Dall-e, Python"
    target_language = "Hindi"
    dubbed_audio_path = "dubbed_audio.wav"
    print("=== Step 1: Transcribing Source Audio ===")
    transcript = transcribe_audio_with_whisper(source_audio_path, language="English")
    if transcript:
        print("Transcription Successful.\n")
        print("Transcribed Text:")
        print("-----------------")
        print(transcript)
        print("-----------------\n")
    else:
        raise Exception("Audio transcription failed.")
    print("=== Step 2: Translating Text to Target Language ===")
    translated_text = translate_text(transcript, target_language=target_language)
    if translated_text:
        print("Translation Successful.\n")
        print("Translated Text:")
        print("-----------------")
        print(translated_text)
        print("-----------------\n")
    else:
        raise Exception("Translation failed.")
    print("=== Step 3: Converting Translated Text to Speech ===")
    text_to_speech(translated_text, output_audio_path=dubbed_audio_path)
    print("=== Playing Dubbed Audio ===")
    audio_segment = AudioSegment.from_file(dubbed_audio_path, format="wav")
    play(audio_segment)
    print("=== Step 4: Evaluating Translation Quality ===")
    print("Translating dubbed Hindi audio back to English for evaluation...\n")
    re_transcript = transcribe_audio_with_whisper(dubbed_audio_path, language="Hindi")
    if re_transcript:
        print("Re-transcription Successful.\n")
        print("Re-transcribed English Text:")
        print("---------------------------")
        print(re_transcript)
        print("---------------------------\n")
    else:
        raise Exception("Re-transcription failed.")
    evaluation_scores = evaluate_translation(transcript, re_transcript)
    print("=== Step 5: Interpreting the Scores ===\n")
    interpret_scores(evaluation_scores["BLEU"], evaluation_scores["ROUGE-1"], evaluation_scores["ROUGE-L"])
    print("=== Process Completed Successfully ===")

if __name__ == "__main__":
    main()
