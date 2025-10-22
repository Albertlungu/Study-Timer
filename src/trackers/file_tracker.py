"""
File Tracker Module

Tracks which specific files are being worked on in various applications.
Provides enhanced file detection for common study apps.
"""

import os
import re
from pathlib import Path


class FileTracker:
    """Enhanced file and document tracking"""
    
    def __init__(self):
        # Common file extensions for study materials
        self.study_extensions = {
            '.md', '.markdown',  # Markdown
            '.txt', '.text',  # Text
            '.doc', '.docx',  # Word
            '.xls', '.xlsx',  # Excel
            '.ppt', '.pptx',  # PowerPoint
            '.pdf',  # PDF
            '.tex', '.bib',  # LaTeX
            '.py', '.js', '.java', '.cpp', '.c',  # Code
            '.ipynb',  # Jupyter
            '.pages', '.numbers', '.key',  # iWork
            '.odt', '.ods', '.odp',  # OpenOffice
        }
    
    def is_study_file(self, filename):
        """
        Check if a file is likely a study-related file
        
        Args:
            filename (str): Name of the file
        
        Returns:
            bool: True if file appears to be study-related
        """
        if not filename:
            return False
        
        # Check extension
        ext = os.path.splitext(filename)[1].lower()
        return ext in self.study_extensions
    
    def clean_filename(self, filename):
        """
        Clean up filename by removing app names and extra info
        
        Args:
            filename (str): Raw filename from window title
        
        Returns:
            str: Cleaned filename
        """
        if not filename:
            return None
        
        # Remove common suffixes (app names, etc.)
        suffixes_to_remove = [
            ' - Obsidian',
            ' - Microsoft Word',
            ' - Microsoft Excel',
            ' - Microsoft PowerPoint',
            ' - Google Docs',
            ' - Google Slides',
            ' - Google Sheets',
            ' - Pages',
            ' - Numbers',
            ' - Keynote',
            ' - Preview',
            ' - Code',
            ' - Visual Studio Code',
        ]
        
        cleaned = filename
        for suffix in suffixes_to_remove:
            if cleaned.endswith(suffix):
                cleaned = cleaned[:-len(suffix)]
        
        return cleaned.strip()
    
    def extract_google_doc_info(self, url, page_title):
        """
        Extract document information from Google Docs/Slides/Sheets URLs
        
        Args:
            url (str): Google Docs URL
            page_title (str): Page title
        
        Returns:
            dict: Document info (name, type, id)
        """
        if not url or 'docs.google.com' not in url:
            return None
        
        # Determine document type
        doc_type = None
        if '/document/' in url:
            doc_type = 'Google Docs'
        elif '/spreadsheets/' in url:
            doc_type = 'Google Sheets'
        elif '/presentation/' in url:
            doc_type = 'Google Slides'
        elif '/forms/' in url:
            doc_type = 'Google Forms'
        
        # Extract document ID from URL
        doc_id = None
        patterns = [
            r'/d/([a-zA-Z0-9-_]+)',
            r'/document/d/([a-zA-Z0-9-_]+)',
            r'/spreadsheets/d/([a-zA-Z0-9-_]+)',
            r'/presentation/d/([a-zA-Z0-9-_]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                doc_id = match.group(1)
                break
        
        # Extract document name from page title
        # Usually format: "Document Name - Google Docs"
        doc_name = page_title
        if ' - Google' in page_title:
            doc_name = page_title.split(' - Google')[0]
        
        return {
            'name': doc_name,
            'type': doc_type,
            'id': doc_id,
            'url': url
        }
    
    def categorize_file_by_name(self, filename):
        """
        Try to categorize what subject/type this file is for
        
        Args:
            filename (str): Name of the file
        
        Returns:
            str: Category or None
        """
        if not filename:
            return None
        
        filename_lower = filename.lower()
        
        # IB Subject detection
        if any(word in filename_lower for word in ['math', 'calc', 'algebra', 'geometry']):
            return 'Mathematics'
        elif any(word in filename_lower for word in ['physics', 'mechanics', 'thermodynamics']):
            return 'Physics'
        elif any(word in filename_lower for word in ['chem', 'chemistry', 'organic', 'inorganic']):
            return 'Chemistry'
        elif any(word in filename_lower for word in ['bio', 'biology', 'anatomy', 'ecology']):
            return 'Biology'
        elif any(word in filename_lower for word in ['english', 'literature', 'essay', 'poem']):
            return 'English'
        elif any(word in filename_lower for word in ['history', 'world war', 'revolution']):
            return 'History'
        elif any(word in filename_lower for word in ['tok', 'theory of knowledge', 'knowledge question']):
            return 'Theory of Knowledge'
        elif any(word in filename_lower for word in ['ee', 'extended essay', 'research']):
            return 'Extended Essay'
        elif any(word in filename_lower for word in ['cas', 'creativity', 'activity', 'service']):
            return 'CAS'
        elif any(word in filename_lower for word in ['ia', 'internal assessment', 'investigation']):
            return 'Internal Assessment'
        elif any(word in filename_lower for word in ['notes', 'lecture', 'study']):
            return 'Study Notes'
        
        return 'Other'
    
    def get_file_metadata(self, file_path, app_name, window_title, url=None, page_title=None):
        """
        Get comprehensive metadata about a file being worked on
        
        Args:
            file_path (str): Path or name of the file
            app_name (str): Application being used
            window_title (str): Window title
            url (str): URL if it's a web document
            page_title (str): Page title if it's a web document
        
        Returns:
            dict: Comprehensive file metadata
        """
        # Check if it's a Google Doc
        if url and 'docs.google.com' in url:
            google_doc_info = self.extract_google_doc_info(url, page_title or window_title)
            if google_doc_info:
                return {
                    'file_name': google_doc_info['name'],
                    'file_type': google_doc_info['type'],
                    'category': self.categorize_file_by_name(google_doc_info['name']),
                    'is_study_file': True,
                    'source': 'Google Docs',
                    'url': url
                }
        
        # For local files
        if file_path:
            cleaned_name = self.clean_filename(file_path)
            return {
                'file_name': cleaned_name,
                'file_type': app_name,
                'category': self.categorize_file_by_name(cleaned_name),
                'is_study_file': self.is_study_file(cleaned_name),
                'source': 'Local',
                'url': None
            }
        
        return None


# Test function
if __name__ == "__main__":
    print("📄 Testing File Tracker...")
    print()
    
    tracker = FileTracker()
    
    # Test file categorization
    test_files = [
        "Chapter-5-Calculus-Notes.md",
        "Physics-IA-Draft.docx",
        "TOK-Essay-Final.pdf",
        "Extended-Essay-Research.txt",
        "Chemistry-Lab-Report.pages",
        "random-file.xyz",
    ]
    
    print("Testing file categorization:")
    for file in test_files:
        category = tracker.categorize_file_by_name(file)
        is_study = tracker.is_study_file(file)
        print(f"  {file}")
        print(f"    Category: {category}")
        print(f"    Is Study File: {is_study}")
        print()
    
    # Test Google Docs extraction
    print("Testing Google Docs extraction:")
    test_url = "https://docs.google.com/document/d/1ABC123xyz/edit"
    test_title = "My Biology Notes - Google Docs"
    
    google_info = tracker.extract_google_doc_info(test_url, test_title)
    if google_info:
        print(f"  Name: {google_info['name']}")
        print(f"  Type: {google_info['type']}")
        print(f"  ID: {google_info['id']}")
    
    print("\nTest complete!")
