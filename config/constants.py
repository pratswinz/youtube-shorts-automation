"""
Application constants
"""
from enum import Enum


class JobStatus(Enum):
    """Job status enumeration"""
    PENDING = "pending"
    PROCESSING = "processing"
    ANALYZING_CONTENT = "analyzing_content"
    GENERATING_SCRIPT = "generating_script"
    GENERATING_VOICE = "generating_voice"
    GENERATING_AUDIO = "generating_audio"
    GENERATING_IMAGES = "generating_images"
    ASSEMBLING_VIDEO = "assembling_video"
    GENERATING_THUMBNAIL = "generating_thumbnail"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


# Supported languages
SUPPORTED_LANGUAGES = [
    'hindi', 'english', 'spanish', 'french', 'german', 
    'italian', 'portuguese', 'russian', 'japanese', 
    'korean', 'chinese', 'arabic'
]

# Video styles
VIDEO_STYLES = [
    'cinematic', 'documentary', 'educational', 'entertainment',
    'motivational', 'news', 'tutorial', 'vlog'
]

# Image generation settings
IMAGE_GENERATION = {
    'num_images': 4,
    'image_duration': 15,  # seconds per image
    'min_images': 3,
    'max_images': 6
}

# Script generation settings
SCRIPT_GENERATION = {
    'min_words': 100,
    'max_words': 150,
    'target_duration': 60  # seconds
}
