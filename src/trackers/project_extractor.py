"""
Enhanced browser tracker with project name extraction
"""

from urllib.parse import urlparse
import re


def extract_project_name(url, page_title=None):
    """
    Extract project name from URL or page title
    
    Args:
        url (str): Website URL
        page_title (str): Page title
    
    Returns:
        str: Project name or None
    """
    if not url:
        return None
    
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.replace('www.', '')
        path = parsed.path
        
        # Kognity - extract subject/course from URL
        if 'kognity.com' in domain:
            # Example: https://app.kognity.com/study/app/ibdp-chemistry-2016/sid-123/cid-456
            # or: https://app.kognity.com/study/app/ibdp-biology-2016/...
            match = re.search(r'/app/([^/]+)', url)
            if match:
                course = match.group(1)
                # Clean up the course name: "ibdp-chemistry-2016" -> "IB Chemistry"
                course = course.replace('ibdp-', 'IB ').replace('ibmyp-', 'IB MYP ').replace('-2016', '').replace('-', ' ')
                return course.title()
            
            # Fallback: check page title
            if page_title:
                # Kognity titles often include the subject
                for subject in ['Chemistry', 'Biology', 'Physics', 'Mathematics', 'Math', 'English', 'History', 'Economics']:
                    if subject.lower() in page_title.lower():
                        return f"IB {subject}"
            
            return "Kognity"
        
        # GitHub - extract repo name
        elif 'github.com' in domain:
            parts = path.strip('/').split('/')
            if len(parts) >= 2:
                return f"{parts[0]}/{parts[1]}"
            return "GitHub"
        
        # Google Docs/Drive
        elif 'docs.google.com' in domain:
            if '/document/' in url:
                # Try to extract document name from title
                if page_title and page_title != 'Google Docs':
                    # Remove " - Google Docs" suffix
                    doc_name = page_title.replace(' - Google Docs', '').strip()
                    if doc_name and len(doc_name) < 50:
                        return doc_name
                return "Google Docs"
            elif '/presentation/' in url:
                if page_title and page_title != 'Google Slides':
                    slide_name = page_title.replace(' - Google Slides', '').strip()
                    if slide_name and len(slide_name) < 50:
                        return slide_name
                return "Google Slides"
            elif '/spreadsheets/' in url:
                if page_title and page_title != 'Google Sheets':
                    sheet_name = page_title.replace(' - Google Sheets', '').strip()
                    if sheet_name and len(sheet_name) < 50:
                        return sheet_name
                return "Google Sheets"
            return "Google Drive"
        
        # Notion
        elif 'notion.so' in domain:
            # Try to extract page name from title
            if page_title and 'Notion' in page_title:
                # Remove "| Notion" suffix
                page_name = page_title.split('|')[0].strip()
                if page_name and len(page_name) < 50:
                    return page_name
            return "Notion"
        
        # Overleaf
        elif 'overleaf.com' in domain:
            match = re.search(r'/project/[^/]+/([^/?]+)', url)
            if match:
                project_name = match.group(1).replace('-', ' ').title()
                return project_name
            if page_title and 'Overleaf' in page_title:
                proj_name = page_title.replace('- Overleaf', '').strip()
                if proj_name and len(proj_name) < 50:
                    return proj_name
            return "Overleaf"
        
        # Canvas LMS
        elif 'canvas.instructure.com' in domain or 'canvas' in domain:
            if page_title and 'Canvas' not in page_title:
                return page_title[:50]
            return "Canvas LMS"
        
        # Moodle
        elif 'moodle' in domain:
            if page_title and 'Moodle' not in page_title:
                return page_title[:50]
            return "Moodle"
        
        # ManageBac
        elif 'managebac.com' in domain:
            if page_title and 'ManageBac' not in page_title:
                return page_title[:50]
            return "ManageBac"
        
        # IB Documents
        elif 'ibdocuments.com' in domain:
            return "IB Documents"
        
        # Stack Overflow
        elif 'stackoverflow.com' in domain:
            return "Stack Overflow"
        
        # Wikipedia
        elif 'wikipedia.org' in domain:
            match = re.search(r'/wiki/([^#?]+)', url)
            if match:
                topic = match.group(1).replace('_', ' ')
                if len(topic) < 50:
                    return f"Wikipedia: {topic}"
            return "Wikipedia"
        
        # Khan Academy
        elif 'khanacademy.org' in domain:
            return "Khan Academy"
        
        # Coursera
        elif 'coursera.org' in domain:
            if page_title and 'Coursera' not in page_title:
                return page_title[:50]
            return "Coursera"
        
        # Default: use domain name
        return domain.split('.')[0].title()
    
    except Exception as e:
        print(f"Error extracting project name: {e}")
        return None
