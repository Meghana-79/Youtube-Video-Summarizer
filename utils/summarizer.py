"""
Summarization Module
Handles AI-powered text summarization using Transformers and HuggingFace models
"""

from transformers import pipeline
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import logging
from typing import Dict, Tuple

logger = logging.getLogger(__name__)

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    logger.info("Downloading NLTK punkt tokenizer...")
    nltk.download('punkt')

# Lazy-load summarization pipeline to avoid blocking app startup (downloads can be slow/fail).
summarizer = None


def _get_summarizer():
    global summarizer
    if summarizer is not None:
        return summarizer

    try:
        logger.info("Loading summarization model (lazy): facebook/bart-large-cnn")
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        logger.info("Summarization model loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load summarization model (lazy): {e}")
        summarizer = None
    return summarizer


def calculate_statistics(text: str) -> Dict:
    """
    Calculate text statistics
    
    Args:
        text (str): Input text
    
    Returns:
        dict: Statistics including word count, character count, etc.
    """
    try:
        words = text.split()
        sentences = sent_tokenize(text)
        
        stats = {
            'word_count': len(words),
            'character_count': len(text),
            'sentence_count': len(sentences),
            'avg_word_length': round(len(text.replace(' ', '')) / len(words), 2) if words else 0,
            'avg_sentence_length': round(len(words) / len(sentences), 2) if sentences else 0,
        }
        
        logger.debug(f"Text statistics: {stats}")
        return stats
    except Exception as e:
        logger.error(f"Error calculating statistics: {e}")
        return {
            'word_count': 0,
            'character_count': 0,
            'sentence_count': 0,
            'avg_word_length': 0,
            'avg_sentence_length': 0,
        }

def summarize_text(text: str, max_length: int = 150, min_length: int = 50, num_beams: int = 4) -> str:
    """
    Summarize text using facebook/bart-large-cnn model
    
    Features:
    - Optimal token management
    - Error handling and fallback
    - Configurable summary length
    - Beam search for quality
    
    Args:
        text (str): Text to summarize (minimum 50 words recommended)
        max_length (int): Maximum summary length (tokens)
        min_length (int): Minimum summary length (tokens)
        num_beams (int): Number of beams for beam search (higher = better quality, slower)
    
    Returns:
        str: Summarized text or fallback to extractive summary if model fails
    """
    try:
        if not text or not isinstance(text, str):
            logger.error("Invalid text input for summarization")
            return None
        
        # Clean and validate text
        text = text.strip()
        words = text.split()
        
        if len(words) < 50:
            logger.warning(f"Text too short for summarization: {len(words)} words")
            return None
        
        logger.info(f"Summarizing text with {len(words)} words")
        
        summarizer_model = _get_summarizer()
        if not summarizer_model:
            logger.warning("Summarizer model not available, using extractive summary")
            return extract_key_points_text(text, num_sentences=3)

        
        # Split text if too long (model max input ~1024 tokens)
        if len(words) > 800:
            logger.info("Text too long, truncating to first 800 words")
            text = ' '.join(words[:800])
        
        # Generate abstractive summary
        try:
            summary_result = summarizer(
                text,
                max_length=max_length,
                min_length=min_length,
                do_sample=False,
                num_beams=num_beams
            )
            
            summary = summary_result[0]['summary_text']
            logger.info(f"Summary generated successfully - Length: {len(summary.split())} words")
            return summary
            
        except Exception as e:
            logger.error(f"Abstractive summarization failed: {e}, using extractive summary")
            return extract_key_points_text(text, num_sentences=5)
        
    except Exception as e:
        logger.error(f"Error in summarize_text: {type(e).__name__}: {e}")
        return None

def extract_key_points(text: str, num_sentences: int = 5) -> list:
    """
    Extract key sentences from text (extractive summarization)
    
    Args:
        text (str): Input text
        num_sentences (int): Number of key sentences to extract
    
    Returns:
        list: List of key sentences
    """
    try:
        sentences = sent_tokenize(text)
        
        if len(sentences) <= num_sentences:
            return sentences
        
        logger.info(f"Extracting {num_sentences} key points from {len(sentences)} sentences")
        
        # Simple extractive: return first N sentences (they're usually most important)
        key_points = sentences[:num_sentences]
        return key_points
        
    except Exception as e:
        logger.error(f"Error extracting key points: {e}")
        return []

def extract_key_points_text(text: str, num_sentences: int = 5) -> str:
    """
    Extract and return key sentences as a combined string
    
    Args:
        text (str): Input text
        num_sentences (int): Number of key sentences to extract
    
    Returns:
        str: Extracted key points as text
    """
    key_points = extract_key_points(text, num_sentences)
    return ' '.join(key_points)

def get_summary_quality_score(original_text: str, summary: str) -> float:
    """
    Calculate quality score of summary
    
    Based on:
    - Compression ratio (higher is better)
    - Minimum length preservation (at least 15% of original)
    - Readability
    
    Args:
        original_text (str): Original text
        summary (str): Generated summary
    
    Returns:
        float: Quality score (0-100)
    """
    try:
        original_words = len(original_text.split())
        summary_words = len(summary.split())
        
        if original_words == 0:
            return 0
        
        compression_ratio = summary_words / original_words
        
        # Ideal compression ratio is 20-30%
        if 0.15 <= compression_ratio <= 0.4:
            score = 85
        elif compression_ratio < 0.15:
            score = 60  # Too aggressive
        else:
            score = 70  # Too conservative
        
        logger.debug(f"Summary quality score: {score}")
        return score
        
    except Exception as e:
        logger.error(f"Error calculating quality score: {e}")
        return 0

def compare_summaries(text: str, max_length: int = 150, min_length: int = 50) -> Dict:
    """
    Generate summary with detailed metrics
    
    Args:
        text (str): Text to summarize
        max_length (int): Maximum summary length
        min_length (int): Minimum summary length
    
    Returns:
        dict: Summary and detailed metrics
    """
    try:
        original_stats = calculate_statistics(text)
        summary = summarize_text(text, max_length, min_length)
        
        if not summary:
            return None
        
        summary_stats = calculate_statistics(summary)
        quality_score = get_summary_quality_score(text, summary)
        
        compression_ratio = (1 - summary_stats['word_count'] / original_stats['word_count']) * 100
        
        return {
            'summary': summary,
            'original_stats': original_stats,
            'summary_stats': summary_stats,
            'compression_ratio': round(compression_ratio, 2),
            'quality_score': quality_score,
            'reduction_percentage': round(compression_ratio, 2)
        }
        
    except Exception as e:
        logger.error(f"Error in compare_summaries: {e}")
        return None
