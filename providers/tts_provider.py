"""
Text-to-Speech providers
Supports: Edge TTS (free), Google Cloud TTS, ElevenLabs
"""
import asyncio
from pathlib import Path
from dataclasses import dataclass
from loguru import logger
import edge_tts


@dataclass
class TTSResult:
    """Result from TTS generation"""
    audio_path: Path
    duration_seconds: float
    provider: str


def _get_audio_duration(path: Path) -> float:
    """Get audio duration in seconds without ffprobe"""
    try:
        from mutagen.mp3 import MP3
        audio = MP3(str(path))
        return audio.info.length
    except ImportError:
        # Fallback: estimate from file size (~16kbps for speech)
        size = path.stat().st_size
        return size / 16000.0  # rough estimate
    except Exception:
        return 30.0  # default fallback


class EdgeTTSProvider:
    """Free TTS using Microsoft Edge TTS"""
    
    def __init__(self):
        self.voice_map = {
            'english': 'en-US-AriaNeural',
            'hindi': 'hi-IN-SwaraNeural',
            'spanish': 'es-ES-ElviraNeural',
            'french': 'fr-FR-DeniseNeural',
            'german': 'de-DE-KatjaNeural',
            'italian': 'it-IT-ElsaNeural',
            'portuguese': 'pt-BR-FranciscaNeural',
            'russian': 'ru-RU-SvetlanaNeural',
            'japanese': 'ja-JP-NanamiNeural',
            'korean': 'ko-KR-SunHiNeural',
            'chinese': 'zh-CN-XiaoxiaoNeural',
            'arabic': 'ar-SA-ZariyahNeural'
        }
    
    async def generate_speech(self, text: str, output_path: Path, language: str = 'english') -> TTSResult:
        """Generate speech from text"""
        try:
            voice = self.voice_map.get(language, self.voice_map['english'])
            logger.info(f"Generating speech with Edge TTS: {voice}")
            
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(str(output_path))
            
            # Get duration (using mutagen - no ffprobe needed)
            duration = _get_audio_duration(output_path)
            
            logger.info(f"Speech generated: {duration:.2f}s")
            
            return TTSResult(
                audio_path=output_path,
                duration_seconds=duration,
                provider="edge_tts"
            )
        except Exception as e:
            logger.error(f"Edge TTS generation failed: {e}")
            raise


class GoogleTTSProvider:
    """Google Cloud Text-to-Speech"""
    
    def __init__(self, credentials_path: str, project_id: str):
        from google.cloud import texttospeech
        import os
        
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
        self.client = texttospeech.TextToSpeechClient()
        self.project_id = project_id
        
        self.voice_map = {
            'english': ('en-US', 'en-US-Neural2-F'),
            'hindi': ('hi-IN', 'hi-IN-Neural2-A'),
            'spanish': ('es-ES', 'es-ES-Neural2-A'),
            'french': ('fr-FR', 'fr-FR-Neural2-A'),
            'german': ('de-DE', 'de-DE-Neural2-A'),
            'italian': ('it-IT', 'it-IT-Neural2-A'),
            'portuguese': ('pt-BR', 'pt-BR-Neural2-A'),
            'russian': ('ru-RU', 'ru-RU-Wavenet-A'),
            'japanese': ('ja-JP', 'ja-JP-Neural2-B'),
            'korean': ('ko-KR', 'ko-KR-Neural2-A'),
            'chinese': ('zh-CN', 'zh-CN-Wavenet-A'),
            'arabic': ('ar-XA', 'ar-XA-Wavenet-A')
        }
    
    async def generate_speech(self, text: str, output_path: Path, language: str = 'english') -> TTSResult:
        """Generate speech from text"""
        try:
            from google.cloud import texttospeech
            
            lang_code, voice_name = self.voice_map.get(language, self.voice_map['english'])
            
            synthesis_input = texttospeech.SynthesisInput(text=text)
            voice = texttospeech.VoiceSelectionParams(
                language_code=lang_code,
                name=voice_name
            )
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )
            
            logger.info(f"Generating speech with Google TTS: {voice_name}")
            
            response = self.client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )
            
            with open(output_path, 'wb') as out:
                out.write(response.audio_content)
            
            # Get duration (no ffprobe needed)
            duration = _get_audio_duration(output_path)
            
            logger.info(f"Speech generated: {duration:.2f}s")
            
            return TTSResult(
                audio_path=output_path,
                duration_seconds=duration,
                provider="google_tts"
            )
        except Exception as e:
            logger.error(f"Google TTS generation failed: {e}")
            raise


class ElevenLabsTTSProvider:
    """ElevenLabs TTS (premium quality)"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.voice_id = "21m00Tcm4TlvDq8ikWAM"  # Default voice
    
    async def generate_speech(self, text: str, output_path: Path, language: str = 'english') -> TTSResult:
        """Generate speech from text"""
        try:
            import httpx
            
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}"
            
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": self.api_key
            }
            
            data = {
                "text": text,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.5
                }
            }
            
            logger.info(f"Generating speech with ElevenLabs")
            
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=data, headers=headers, timeout=60.0)
                response.raise_for_status()
                
                with open(output_path, 'wb') as f:
                    f.write(response.content)
            
            # Get duration (no ffprobe needed)
            duration = _get_audio_duration(output_path)
            
            logger.info(f"Speech generated: {duration:.2f}s")
            
            return TTSResult(
                audio_path=output_path,
                duration_seconds=duration,
                provider="elevenlabs"
            )
        except Exception as e:
            logger.error(f"ElevenLabs TTS generation failed: {e}")
            raise
