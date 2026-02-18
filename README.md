# 🎙️ MP3 Audio Translator

A Python pipeline that transcribes an MP3 file, translates it into any language, and outputs a new translated MP3 — all for free, no API keys required.

---

## 🔧 How It Works

1. **Transcription** — [OpenAI Whisper](https://github.com/openai/whisper) converts speech to text locally on your machine
2. **Translation** — [deep-translator](https://github.com/nidhaloff/deep-translator) translates the text using free Google Translate
3. **Text-to-Speech** — [gTTS](https://github.com/pndurette/gTTS) converts the translated text back into an MP3 audio file

---

## 📋 Requirements

### 1. Python
Make sure you have Python 3.8+ installed.
👉 https://www.python.org/downloads/

### 2. ffmpeg
Whisper requires ffmpeg to read audio files.

- Download from 👉 https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip
- Extract the ZIP (e.g. to `C:\ffmpeg`)
- Add the `bin` folder to your system PATH:
  ```
  C:\ffmpeg\ffmpeg-8.0.1-essentials_build\bin
  ```
- Restart your terminal and verify:
  ```bash
  ffmpeg -version
  ```

### 3. Python Dependencies
Create a virtual environment and install the required packages:

```bash
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (Mac/Linux)
source .venv/bin/activate

# Install packages
pip install openai-whisper deep-translator gtts
```

---

## 🚀 Usage

```bash
python translate_audio_free.py --input your_audio.mp3 --language Hindi
```

You can use any language name or ISO code:

```bash
python translate_audio_free.py --input your_audio.mp3 --language Spanish
python translate_audio_free.py --input your_audio.mp3 --language fr
python translate_audio_free.py --input your_audio.mp3 --language Japanese
```

Or run without `--language` to be prompted interactively:

```bash
python translate_audio_free.py --input your_audio.mp3
```

---

## 🌍 Supported Languages

Some of the supported languages:

| Language   | Code | Language   | Code |
|------------|------|------------|------|
| Arabic     | ar   | Italian    | it   |
| Bengali    | bn   | Japanese   | ja   |
| Chinese    | zh-CN| Korean     | ko   |
| Dutch      | nl   | Hindi      | hi   |
| French     | fr   | Portuguese | pt   |
| German     | de   | Russian    | ru   |
| Greek      | el   | Spanish    | es   |
| Indonesian | id   | Turkish    | tr   |

And many more — run the script interactively to see the full list.

---

## 📁 Output

The translated MP3 is saved in the same folder as your input file:

```
your_audio_translated_hi.mp3
your_audio_translated_es.mp3
```

---

## ⚠️ Notes

- The first run downloads the Whisper model (~139 MB) automatically
- The FP16 warning on CPU is harmless — the script works fine
- Long audio files may take a few minutes to transcribe
- MP3 files are excluded from this repo — add your own

---

## 📄 License

MIT — free to use and modify.
