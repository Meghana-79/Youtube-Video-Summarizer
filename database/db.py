"""
Database Module
Handles SQLite database operations for storing and retrieving summaries
"""

import sqlite3
from datetime import datetime
import logging
import os
from contextlib import contextmanager

logger = logging.getLogger(__name__)

DATABASE = 'summaries.db'

@contextmanager
def get_db_connection():
    """
    Context manager for database connections
    
    Ensures connections are properly closed
    
    Yields:
        sqlite3.Connection: Database connection with row factory
    """
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_db(app):
    """
    Initialize database schema
    
    Creates tables if they don't exist:
    - summaries: stores video summaries
    
    Args:
        app: Flask app instance
    """
    try:
        with app.app_context():
            with get_db_connection() as conn:
                cursor = conn.cursor()
                
                # Create summaries table with comprehensive fields
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS summaries (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        url TEXT NOT NULL,
                        video_id TEXT UNIQUE,
                        transcript TEXT NOT NULL,
                        summary TEXT NOT NULL,
                        transcript_length INTEGER DEFAULT 0,
                        summary_length INTEGER DEFAULT 0,
                        compression_ratio REAL DEFAULT 0.0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Create index for faster queries
                cursor.execute('''
                    CREATE INDEX IF NOT EXISTS idx_video_id 
                    ON summaries(video_id)
                ''')
                
                cursor.execute('''
                    CREATE INDEX IF NOT EXISTS idx_created_at 
                    ON summaries(created_at)
                ''')
                
                conn.commit()
                logger.info("Database initialized successfully")
                
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise

def save_summary(url: str, video_id: str, transcript: str, summary: str, 
                 transcript_length: int = 0, summary_length: int = 0, 
                 compression_ratio: float = 0.0) -> dict:
    """
    Save a summary to the database
    
    Args:
        url (str): YouTube video URL
        video_id (str): YouTube video ID
        transcript (str): Full transcript text
        summary (str): Generated summary
        transcript_length (int): Number of words in transcript
        summary_length (int): Number of words in summary
        compression_ratio (float): Compression ratio percentage
    
    Returns:
        dict: Saved summary with ID and timestamp
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO summaries 
                (url, video_id, transcript, summary, transcript_length, summary_length, compression_ratio, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                url, 
                video_id, 
                transcript, 
                summary,
                transcript_length,
                summary_length,
                compression_ratio,
                datetime.now().isoformat(),
                datetime.now().isoformat()
            ))
            
            conn.commit()
            
            summary_id = cursor.lastrowid
            logger.info(f"Summary saved with ID: {summary_id}")
            
            return {
                'id': summary_id,
                'created_at': datetime.now().isoformat(),
                'success': True
            }
            
    except sqlite3.IntegrityError as e:
        logger.warning(f"Duplicate video ID: {video_id}. Updating existing summary.")
        return update_summary(video_id, url, transcript, summary, transcript_length, summary_length, compression_ratio)
    except Exception as e:
        logger.error(f"Error saving summary: {e}")
        raise

def update_summary(video_id: str, url: str, transcript: str, summary: str,
                   transcript_length: int, summary_length: int, compression_ratio: float) -> dict:
    """
    Update an existing summary
    
    Args:
        video_id (str): YouTube video ID
        url (str): YouTube video URL
        transcript (str): Full transcript
        summary (str): Generated summary
        transcript_length (int): Transcript word count
        summary_length (int): Summary word count
        compression_ratio (float): Compression ratio
    
    Returns:
        dict: Updated summary info
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE summaries 
                SET url = ?, transcript = ?, summary = ?, 
                    transcript_length = ?, summary_length = ?, 
                    compression_ratio = ?, updated_at = ?
                WHERE video_id = ?
            ''', (
                url, transcript, summary,
                transcript_length, summary_length,
                compression_ratio,
                datetime.now().isoformat(),
                video_id
            ))
            
            conn.commit()
            logger.info(f"Summary updated for video_id: {video_id}")
            
            return {'success': True, 'updated': True}
            
    except Exception as e:
        logger.error(f"Error updating summary: {e}")
        raise

def get_all_summaries(limit: int = None, offset: int = 0) -> list:
    """
    Get all summaries from database
    
    Args:
        limit (int): Maximum number of summaries to return
        offset (int): Number of summaries to skip
    
    Returns:
        list: List of summaries as dictionaries
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            if limit:
                cursor.execute('''
                    SELECT * FROM summaries 
                    ORDER BY created_at DESC 
                    LIMIT ? OFFSET ?
                ''', (limit, offset))
            else:
                cursor.execute('''
                    SELECT * FROM summaries 
                    ORDER BY created_at DESC
                ''')
            
            summaries = cursor.fetchall()
            result = [dict(row) for row in summaries]
            
            logger.info(f"Retrieved {len(result)} summaries")
            return result
            
    except Exception as e:
        logger.error(f"Error fetching summaries: {e}")
        return []

def get_summary_by_id(summary_id: int) -> dict:
    """
    Get a specific summary by ID
    
    Args:
        summary_id (int): Summary ID
    
    Returns:
        dict: Summary data or None
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM summaries WHERE id = ?', (summary_id,))
            summary = cursor.fetchone()
            
            if summary:
                logger.info(f"Retrieved summary with ID: {summary_id}")
                return dict(summary)
            else:
                logger.warning(f"Summary not found with ID: {summary_id}")
                return None
                
    except Exception as e:
        logger.error(f"Error fetching summary by ID: {e}")
        return None

def get_summary_by_video_id(video_id: str) -> dict:
    """
    Get a summary by video ID
    
    Args:
        video_id (str): YouTube video ID
    
    Returns:
        dict: Summary data or None
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM summaries WHERE video_id = ?', (video_id,))
            summary = cursor.fetchone()
            
            if summary:
                logger.info(f"Retrieved summary for video_id: {video_id}")
                return dict(summary)
            else:
                logger.debug(f"Summary not found for video_id: {video_id}")
                return None
                
    except Exception as e:
        logger.error(f"Error fetching summary by video_id: {e}")
        return None

def delete_summary(summary_id: int) -> bool:
    """
    Delete a summary by ID
    
    Args:
        summary_id (int): Summary ID
    
    Returns:
        bool: True if deleted, False otherwise
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM summaries WHERE id = ?', (summary_id,))
            conn.commit()
            
            if cursor.rowcount > 0:
                logger.info(f"Summary deleted with ID: {summary_id}")
                return True
            else:
                logger.warning(f"No summary found to delete with ID: {summary_id}")
                return False
                
    except Exception as e:
        logger.error(f"Error deleting summary: {e}")
        return False

def get_analytics() -> dict:
    """
    Get application analytics and statistics
    
    Returns:
        dict: Analytics including total summaries, total words, etc.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Total summaries
            cursor.execute('SELECT COUNT(*) as count FROM summaries')
            total_summaries = cursor.fetchone()['count']
            
            # Total words processed
            cursor.execute('SELECT SUM(transcript_length) as total FROM summaries')
            total_words = cursor.fetchone()['total'] or 0
            
            # Average compression ratio
            cursor.execute('SELECT AVG(compression_ratio) as avg FROM summaries')
            avg_compression = round(cursor.fetchone()['avg'] or 0, 2)
            
            # Total summaries generated
            cursor.execute('SELECT SUM(summary_length) as total FROM summaries')
            total_summary_words = cursor.fetchone()['total'] or 0
            
            # Most recent
            cursor.execute('SELECT created_at FROM summaries ORDER BY created_at DESC LIMIT 1')
            last_summary = cursor.fetchone()
            last_summary_time = last_summary['created_at'] if last_summary else None
            
            analytics = {
                'total_summaries': total_summaries,
                'total_words_processed': total_words,
                'average_compression_ratio': avg_compression,
                'total_summary_words': total_summary_words,
                'last_summary_time': last_summary_time,
                'average_summary_length': round(total_summary_words / total_summaries, 0) if total_summaries > 0 else 0
            }
            
            logger.info(f"Analytics retrieved: {analytics}")
            return analytics
            
    except Exception as e:
        logger.error(f"Error retrieving analytics: {e}")
        return {
            'total_summaries': 0,
            'total_words_processed': 0,
            'average_compression_ratio': 0,
            'total_summary_words': 0,
            'last_summary_time': None,
            'average_summary_length': 0
        }

def search_summaries(query: str) -> list:
    """
    Search summaries by URL or summary content
    
    Args:
        query (str): Search query
    
    Returns:
        list: List of matching summaries
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            search_term = f'%{query}%'
            cursor.execute('''
                SELECT * FROM summaries 
                WHERE url LIKE ? OR summary LIKE ? 
                ORDER BY created_at DESC
            ''', (search_term, search_term))
            
            summaries = cursor.fetchall()
            result = [dict(row) for row in summaries]
            
            logger.info(f"Found {len(result)} summaries matching query: {query}")
            return result
            
    except Exception as e:
        logger.error(f"Error searching summaries: {e}")
        return []

def clear_all_summaries() -> bool:
    """
    Clear all summaries from database (use with caution)
    
    Returns:
        bool: True if successful
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM summaries')
            conn.commit()
            logger.warning(f"Cleared all summaries from database")
            return True
    except Exception as e:
        logger.error(f"Error clearing summaries: {e}")
        return False
