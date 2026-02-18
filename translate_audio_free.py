"""
Audio Translation Pipeline (No API Keys Required)
--------------------------------------------------
Uses:
  - openai-whisper  → Speech-to-Text (runs locally)
  - deep-translator → Translation (free Google Translate wrapper)
  - gTTS            → Text-to-Speech (Google TTS, no key needed)

Install dependencies:
    pip install openai-whisper deep-translator gtts

Then run:
    python translate_audio_free.py --input John_Hapton_vacation_Story.mp3 --language Spanish

Or run without --language to be prompted interactively.
"""
import os
os.environ["PATH"] += r";C:\ffmpeg\ffmpeg-8.0.1-essentials_build\bin"
import argparse
import sys
from pathlib import Path


def check_dependencies():
    missing = []
    for pkg, import_name in [("openai-whisper", "whisper"), ("deep-translator", "deep_translator"), ("gTTS", "gtts")]:
        try:
            __import__(import_name)
        except ImportError:
            missing.append(pkg)
    if missing:
        print("Missing dependencies. Please install them first:\n")
        print(f"    pip install {' '.join(missing)}\n")
        sys.exit(1)


def transcribe(input_path: Path) -> tuple[str, str]:
    """Transcribe audio using Whisper. Returns (transcript, detected_language)."""
    import whisper
    print("  Loading Whisper model (first run downloads ~139 MB) ...")
    model = whisper.load_model("base")
    print(f"  Transcribing '{input_path.name}' ...")
    result = model.transcribe(str(input_path))
    transcript = result["text"].strip()
    detected_lang = result.get("language", "en")
    if not transcript:
        raise RuntimeError("Whisper returned an empty transcript.")
    return transcript, detected_lang


def translate(text: str, target_language: str, source_language: str = "auto") -> str:
    """Translate text using deep-translator (free Google Translate)."""
    from deep_translator import GoogleTranslator
    print(f"  Translating to '{target_language}' ...")
    translator = GoogleTranslator(source=source_language, target=target_language)
    # deep-translator has a 5000 char limit per call; chunk if needed
    if len(text) <= 4999:
        return translator.translate(text)
    chunks = [text[i:i+4999] for i in range(0, len(text), 4999)]
    return " ".join(translator.translate(chunk) for chunk in chunks)


def synthesise(text: str, language: str, output_path: Path) -> None:
    """Convert text to speech MP3 using gTTS."""
    from gtts import gTTS
    print(f"  Synthesising speech ...")
    tts = gTTS(text=text, lang=language, slow=False)
    tts.save(str(output_path))


# Map of common language names → codes used by deep-translator / gTTS
LANGUAGE_MAP = {
    "afrikaans": "af",   "albanian": "sq",   "arabic": "ar",
    "bengali": "bn",     "bosnian": "bs",    "bulgarian": "bg",
    "catalan": "ca",     "chinese": "zh-CN", "mandarin": "zh-CN",
    "croatian": "hr",    "czech": "cs",      "danish": "da",
    "dutch": "nl",       "english": "en",    "estonian": "et",
    "finnish": "fi",     "french": "fr",     "german": "de",
    "greek": "el",       "gujarati": "gu",   "hindi": "hi",
    "hungarian": "hu",   "icelandic": "is",  "indonesian": "id",
    "italian": "it",     "japanese": "ja",   "kannada": "kn",
    "korean": "ko",      "latvian": "lv",    "lithuanian": "lt",
    "malay": "ms",       "malayalam": "ml",  "marathi": "mr",
    "nepali": "ne",      "norwegian": "no",  "polish": "pl",
    "portuguese": "pt",  "punjabi": "pa",    "romanian": "ro",
    "russian": "ru",     "serbian": "sr",    "sinhala": "si",
    "slovak": "sk",      "slovenian": "sl",  "spanish": "es",
    "swahili": "sw",     "swedish": "sv",    "tamil": "ta",
    "telugu": "te",      "thai": "th",       "turkish": "tr",
    "ukrainian": "uk",   "urdu": "ur",       "vietnamese": "vi",
    "welsh": "cy",
}


def resolve_language(user_input: str) -> str:
    """Return the language code for a given name or code."""
    normalised = user_input.strip().lower()
    if normalised in LANGUAGE_MAP:
        return LANGUAGE_MAP[normalised]
    # Already a code?
    if normalised in LANGUAGE_MAP.values():
        return normalised
    # Partial name match
    matches = [code for name, code in LANGUAGE_MAP.items() if name.startswith(normalised)]
    if len(matches) == 1:
        return matches[0]
    print(f"  Warning: '{user_input}' not recognised — passing as-is to the APIs.")
    return user_input.strip()


def prompt_language() -> str:
    print("\nSupported languages:")
    items = sorted(LANGUAGE_MAP.items())
    for i, (name, code) in enumerate(items):
        end = "\n" if (i + 1) % 4 == 0 else "  "
        print(f"  {name.title():<18}({code})", end=end)
    print("\n")
    while True:
        lang = input("Enter target language (name or code): ").strip()
        if lang:
            return lang
        print("  Please enter a value.")


def run_pipeline(input_path: Path, target_language_input: str) -> None:
    lang_code = resolve_language(target_language_input)

    print(f"\n{'='*55}")
    print(f"  Input  : {input_path.name}")
    print(f"  Target : {target_language_input}  →  code='{lang_code}'")
    print(f"{'='*55}\n")

    # 1. Transcribe
    transcript, detected_lang = transcribe(input_path)
    print(f"\n  Detected source language : {detected_lang}")
    print(f"  Transcript:\n  {transcript}\n")

    # 2. Translate
    translated = translate(transcript, target_language=lang_code, source_language=detected_lang)
    print(f"  Translation:\n  {translated}\n")

    # 3. Synthesise
    output_path = input_path.parent / f"{input_path.stem}_translated_{lang_code}.mp3"
    synthesise(translated, language=lang_code, output_path=output_path)

    print(f"\n  ✓ Output saved to: {output_path}")
    print(f"{'='*55}\n")


if __name__ == "__main__":
    check_dependencies()

    parser = argparse.ArgumentParser(description="Audio translation pipeline (no API keys needed)")
    parser.add_argument("--input", "-i", required=True, help="Path to the input MP3 file")
    parser.add_argument(
        "--language", "-l", default=None,
        help="Target language name or code (e.g. 'Spanish' or 'es'). Prompted if omitted."
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: '{input_path}' not found.")
        sys.exit(1)

    target_language = args.language if args.language else prompt_language()
    run_pipeline(input_path, target_language)
