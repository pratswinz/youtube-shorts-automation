"""
Content Safety Module
Checks content for safety and compliance
"""
import re
from typing import Dict, Any, List
from loguru import logger


class ContentSafety:
    """Content safety checker"""
    
    def __init__(self):
        # Unsafe keywords (basic list - expand as needed)
        self.unsafe_keywords = [
            'violence', 'hate', 'explicit', 'nsfw', 'adult',
            'weapon', 'drug', 'illegal', 'harmful'
        ]
        
        # Sensitive topics that need careful handling
        self.sensitive_topics = [
            'politics', 'religion', 'medical', 'financial advice',
            'legal advice', 'health claims'
        ]
    
    def check_prompt(self, prompt: str) -> Dict[str, Any]:
        """
        Check if prompt is safe
        
        Returns:
            dict with keys: is_safe, issues, warnings
        """
        issues = []
        warnings = []
        
        prompt_lower = prompt.lower()
        
        # Check for unsafe keywords
        for keyword in self.unsafe_keywords:
            if keyword in prompt_lower:
                issues.append(f"Contains potentially unsafe keyword: {keyword}")
        
        # Check for sensitive topics
        for topic in self.sensitive_topics:
            if topic in prompt_lower:
                warnings.append(f"Contains sensitive topic: {topic}")
        
        # Check length
        if len(prompt) < 10:
            warnings.append("Prompt is very short - may not generate good content")
        
        if len(prompt) > 500:
            warnings.append("Prompt is very long - may be truncated")
        
        is_safe = len(issues) == 0
        
        if not is_safe:
            logger.warning(f"Content safety check failed: {issues}")
        elif warnings:
            logger.info(f"Content safety warnings: {warnings}")
        else:
            logger.info("Content safety check passed")
        
        return {
            'is_safe': is_safe,
            'issues': issues,
            'warnings': warnings
        }
    
    def check_script(self, script: str) -> Dict[str, Any]:
        """Check if generated script is safe"""
        return self.check_prompt(script)
    
    def check_image_prompts(self, prompts: List[str]) -> Dict[str, Any]:
        """Check if image prompts are safe"""
        all_issues = []
        all_warnings = []
        
        for i, prompt in enumerate(prompts):
            result = self.check_prompt(prompt)
            if not result['is_safe']:
                all_issues.extend([f"Prompt {i+1}: {issue}" for issue in result['issues']])
            if result['warnings']:
                all_warnings.extend([f"Prompt {i+1}: {warning}" for warning in result['warnings']])
        
        is_safe = len(all_issues) == 0
        
        return {
            'is_safe': is_safe,
            'issues': all_issues,
            'warnings': all_warnings
        }
    
    def sanitize_text(self, text: str) -> str:
        """Remove potentially unsafe content from text"""
        # Remove URLs
        text = re.sub(r'http[s]?://\S+', '', text)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove phone numbers (basic pattern)
        text = re.sub(r'\d{3}[-.]?\d{3}[-.]?\d{4}', '', text)
        
        return text.strip()
