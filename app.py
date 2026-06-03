"""
YouTube Video Summarizer - Flask Application
Handles transcript extraction, summarization, and database operations
"""

from flask import Flask, render_template, request, jsonify
from utils.transcript import get_transcript, extract_video_id

from youtube_transcript_api import (  # type: ignore
    CouldNotRetrieveTranscript,
    NoTranscriptFound,
    TranscriptsDisabled,
    VideoUnavailable,
)


from utils.summarizer import summarize_text, calculate_statistics
from database.db import (init_db, save_summary, get_all_summaries, 
                        delete_summary, get_summary_by_id, get_analytics)
import logging
import os
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['DATABASE'] = 'summaries.db'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max request size

# Initialize database
init_db(app)

@app.route('/')
def index():
    """Render the main page"""
    logger.info("User accessed index page")
    try:
        analytics = get_analytics()
        return render_template('index.html', analytics=analytics)
    except Exception as e:
        logger.error(f"Error loading index: {e}")
        return render_template('index.html', analytics=None)

@app.route('/api/summarize', methods=['POST'])
def summarize():
    """
    Handle video summarization endpoint
    
    Expected JSON:
    {
        "url": "https://youtube.com/watch?v=...",
        "model": "facebook/bart-large-cnn"  (optional)
    }
    """
    try:
        data = request.get_json()
        url = data.get('url', '').strip()
        
        if not url:
            logger.warning("Summarize request without URL")
            return jsonify({'error': 'URL is required', 'status': 'error'}), 400
        
        # Validate YouTube URL
        video_id = extract_video_id(url)
        if not video_id:
            logger.warning(f"Invalid YouTube URL provided: {url}")
            return jsonify({
                'error': 'Invalid YouTube URL. Please provide a valid youtube.com URL.',
                'status': 'error'
            }), 400
        
        logger.info(f"Processing video: {video_id}")
        
        # Get transcript
        logger.info(f"Extracting transcript for {video_id}")
        transcript = get_transcript(url)
        
        if not transcript:
            logger.error(f"Failed to extract transcript for {video_id}")
            return jsonify({
                'error': 'Could not extract transcript. Video may not have captions, captions may be disabled, or the video may be private/region restricted. Check app.log for details.',
                'status': 'error'
            }), 400

        
        if len(transcript.split()) < 50:
            logger.warning(f"Transcript too short for {video_id}")
            return jsonify({
                'error': 'Transcript too short for summarization. Minimum 50 words required.',
                'status': 'error'
            }), 400
        
        # Calculate transcript statistics
        transcript_stats = calculate_statistics(transcript)
        logger.info(f"Transcript stats - Words: {transcript_stats['word_count']}, Chars: {transcript_stats['char_count']}")
        
        # Summarize
        logger.info(f"Generating summary for {video_id}")
        summary = summarize_text(transcript)
        
        if not summary:
            logger.error(f"Summarization failed for {video_id}")
            return jsonify({
                'error': 'Failed to generate summary. Please try again.',
                'status': 'error'
            }), 500
        
        # Calculate summary statistics
        summary_stats = calculate_statistics(summary)
        
        # Save to database
        summary_data = save_summary(
            url=url,
            video_id=video_id,
            transcript=transcript,
            summary=summary,
            transcript_length=transcript_stats['word_count'],
            summary_length=summary_stats['word_count'],
            compression_ratio=round((1 - len(summary.split()) / len(transcript.split())) * 100, 2)
        )
        
        logger.info(f"Summary saved successfully - ID: {summary_data.get('id')}")
        
        return jsonify({
            'success': True,
            'status': 'success',
            'data': {
                'summary': summary,
                'transcript': transcript,
                'statistics': {
                    'transcript': transcript_stats,
                    'summary': summary_stats,
                    'compression_ratio': round((1 - len(summary.split()) / len(transcript.split())) * 100, 2),
                    'processing_time': 'N/A'
                }
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error in summarize endpoint: {str(e)}", exc_info=True)
        return jsonify({
            'error': f'Server error: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/api/history')
def get_history():
    """Get all summaries as JSON API"""
    try:
        summaries = get_all_summaries()
        logger.info(f"Retrieved {len(summaries)} summaries from history")
        return jsonify({
            'success': True,
            'count': len(summaries),
            'data': summaries
        }), 200
    except Exception as e:
        logger.error(f"Error fetching history: {str(e)}")
        return jsonify({'error': str(e), 'status': 'error'}), 500

@app.route('/history')
def history():
    """Render history page"""
    logger.info("User accessed history page")
    try:
        summaries = get_all_summaries()
        analytics = get_analytics()
        return render_template('history.html', summaries=summaries, analytics=analytics)
    except Exception as e:
        logger.error(f"Error loading history page: {e}")
        return render_template('history.html', summaries=[], analytics=None)

@app.route('/api/summary/<int:summary_id>')
def get_summary_detail(summary_id):
    """Get detailed summary information"""
    try:
        summary = get_summary_by_id(summary_id)
        if not summary:
            return jsonify({'error': 'Summary not found', 'status': 'error'}), 404
        
        logger.info(f"Retrieved summary detail - ID: {summary_id}")
        return jsonify({
            'success': True,
            'data': summary
        }), 200
    except Exception as e:
        logger.error(f"Error fetching summary detail: {str(e)}")
        return jsonify({'error': str(e), 'status': 'error'}), 500

@app.route('/api/delete/<int:summary_id>', methods=['DELETE'])
def delete(summary_id):
    """Delete a summary"""
    try:
        delete_summary(summary_id)
        logger.info(f"Summary deleted - ID: {summary_id}")
        return jsonify({'success': True, 'status': 'success'}), 200
    except Exception as e:
        logger.error(f"Error deleting summary: {str(e)}")
        return jsonify({'error': str(e), 'status': 'error'}), 500

@app.route('/api/analytics')
def analytics():
    """Get application analytics"""
    try:
        stats = get_analytics()
        logger.info("Analytics retrieved")
        return jsonify({
            'success': True,
            'data': stats
        }), 200
    except Exception as e:
        logger.error(f"Error fetching analytics: {str(e)}")
        return jsonify({'error': str(e), 'status': 'error'}), 500

@app.route('/result')
def result():
    """Render result page"""
    return render_template('result.html')

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()}), 200

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    logger.warning(f"404 error: {error}")
    return jsonify({'error': 'Resource not found', 'status': 'error'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"500 error: {error}", exc_info=True)
    return jsonify({'error': 'Internal server error', 'status': 'error'}), 500

if __name__ == '__main__':
    logger.info("Starting YouTube Summarizer application")
    app.run(debug=True, host='0.0.0.0', port=5000)
