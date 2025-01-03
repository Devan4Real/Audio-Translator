# Audio Translation and Evaluation Tool

This repository provides a Python-based application that performs audio transcription, translation, text-to-speech, and translation evaluation using BLEU and ROUGE scores. The tool is designed for converting audio content in English to Hindi (or other languages) and evaluating the quality of the translation.

## Features

- **Audio Transcription**: Converts audio files into text using OpenAI's Whisper API.
- **Text Translation**: Translates the transcribed text into a target language (default: Hindi) using GPT-4.
- **Text-to-Speech Conversion**: Converts translated text into speech and saves it as an audio file.
- **Translation Quality Evaluation**: Calculates BLEU and ROUGE scores to evaluate the quality of the translation.

## Prerequisites

- Python 3.7+
- pip (Python package manager)
- OpenAI API key (required for Whisper and GPT-4 usage)
- Environment variables set up for `OPENAI_API_KEY`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-Devan4Real/Audio-Translator.git
   cd Audio-Translator
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install requests pydub sacrebleu rouge-score pyttsx3
   ```

4. Set up your OpenAI API key as an environment variable:

## Recommended Project Structure

```plaintext
.
├── main.py                # Main script for running the process
├── README.md              # Project documentation
├── requirements.txt       # Python dependencies
├── audio                  # Directory for audio files (input and output)
│   ├── Test.wav           # Example input audio file
│   └── dubbed_audio.wav   # Output audio file (translated and dubbed)
├── utils                  # Utility functions (future modularization)
└── .env                   # (Optional) Environment file for storing API keys
```

## How to Run the Project

1. Ensure you have completed the installation steps and have the necessary API key set up.

2. Place your source audio file in the `audio` directory and name it `Test.wav` (or update the script with your filename).

3. Run the main script:
   ```bash
   python main.py
   ```

4. Follow the console output to track the process:
   - Transcription of the audio file.
   - Translation into the target language.
   - Conversion of translated text to speech.
   - Playback of the dubbed audio.
   - Evaluation of the translation quality.

5. Check the `audio` directory for the output dubbed audio file (`dubbed_audio.wav`).

## API Usage

- **OpenAI Whisper API**: Used for transcribing audio files into text.
- **OpenAI GPT-4 API**: Used for translating text to the target language.
- **Pyttsx3**: Used for text-to-speech conversion.

## Translation Quality Metrics

- **BLEU (Bilingual Evaluation Understudy)**: Measures how closely the translation matches the reference text.
- **ROUGE (Recall-Oriented Understudy for Gisting Evaluation)**: Measures overlap between the candidate and reference text.

## Limitations

- Requires a stable internet connection for API calls.
- Quality of transcription and translation depends on the APIs used.
- Limited to languages supported by OpenAI Whisper and GPT-4.

## Contribution

Contributions are welcome! Feel free to fork the repository, make changes, and submit a pull request. Ensure your code adheres to the following:

- Proper documentation.
- Adherence to PEP 8 style guidelines.

## Acknowledgements

- [OpenAI](https://openai.com) for providing Whisper and GPT-4 APIs.
- Developers of [Pyttsx3](https://pyttsx3.readthedocs.io/) for the text-to-speech library.
- [SacreBLEU](https://github.com/mjpost/sacrebleu) and [ROUGE](https://github.com/google-research/google-research/tree/master/rouge) developers for evaluation tools.

---

Note: I ran out of open ai credits.... So I will test and update any errors if I ever decide to buy more credits....

**Happy Translating!**
