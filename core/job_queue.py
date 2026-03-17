"""
Job queue for managing video generation tasks
"""
import asyncio
from typing import Dict, Optional
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from loguru import logger


class JobStatus(Enum):
    """Job status enumeration"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class VideoJob:
    """Video generation job"""
    job_id: str
    user_id: int
    prompt: str
    duration: int = 60
    style: str = "cinematic"
    status: JobStatus = JobStatus.PENDING
    progress: int = 0
    error: Optional[str] = None
    output_path: Optional[Path] = None
    thumbnail_path: Optional[Path] = None
    metadata: Dict = field(default_factory=dict)
    reference_image: Optional[Path] = None


class JobQueue:
    """In-memory job queue"""
    
    def __init__(self):
        self.jobs: Dict[str, VideoJob] = {}
        self.queue: asyncio.Queue = asyncio.Queue()
        self.processing = False
        self._worker_task = None
        self._job_counter = 0
    
    def generate_job_id(self) -> str:
        """Generate unique job ID"""
        import time
        self._job_counter += 1
        timestamp = int(time.time() * 1000)
        return f"job_{timestamp}_{self._job_counter}"
    
    async def add_job(self, job: VideoJob) -> str:
        """Add a job to the queue"""
        self.jobs[job.job_id] = job
        await self.queue.put(job.job_id)
        logger.info(f"Job {job.job_id} added to queue")
        
        # Start worker if not running
        if not self.processing:
            self._worker_task = asyncio.create_task(self._process_queue())
        
        return job.job_id
    
    def get_job(self, job_id: str) -> Optional[VideoJob]:
        """Get job by ID"""
        return self.jobs.get(job_id)
    
    def get_job_status(self, job_id: str) -> Optional[dict]:
        """Get job status as dictionary"""
        job = self.jobs.get(job_id)
        if not job:
            return None
        
        return {
            'job_id': job.job_id,
            'status': job.status.value,
            'progress': job.progress,
            'error': job.error,
            'output_path': str(job.output_path) if job.output_path else None,
            'thumbnail_path': str(job.thumbnail_path) if job.thumbnail_path else None,
            'metadata': job.metadata
        }
    
    def update_job(self, job_id: str, **kwargs):
        """Update job attributes"""
        if job_id in self.jobs:
            job = self.jobs[job_id]
            for key, value in kwargs.items():
                if hasattr(job, key):
                    setattr(job, key, value)
    
    async def _process_queue(self):
        """Process jobs from queue"""
        from core.video_generator import VideoGenerator
        
        self.processing = True
        generator = VideoGenerator()
        
        try:
            while True:
                try:
                    # Get next job (with timeout to allow graceful shutdown)
                    job_id = await asyncio.wait_for(
                        self.queue.get(),
                        timeout=1.0
                    )
                    
                    job = self.jobs.get(job_id)
                    if not job:
                        continue
                    
                    logger.info(f"Processing job {job_id}")
                    job.status = JobStatus.PROCESSING
                    
                    try:
                        # Generate video
                        await generator.generate_video(job)
                        job.status = JobStatus.COMPLETED
                        logger.success(f"Job {job_id} completed")
                        
                    except Exception as e:
                        job.status = JobStatus.FAILED
                        job.error = str(e)
                        logger.error(f"Job {job_id} failed: {e}")
                    
                    self.queue.task_done()
                    
                except asyncio.TimeoutError:
                    # Check if there are more jobs
                    if self.queue.empty():
                        break
                    continue
                    
        finally:
            self.processing = False
            logger.info("Queue worker stopped")
    
    def get_queue_size(self) -> int:
        """Get number of pending jobs"""
        return self.queue.qsize()
    
    def get_all_jobs(self) -> Dict[str, VideoJob]:
        """Get all jobs"""
        return self.jobs


# Global job queue instance
job_queue = JobQueue()
