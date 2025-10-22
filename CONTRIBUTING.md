# Contributing to Study Timer

First off, thank you for considering contributing to Study Timer! It's people like you who make this tool better for IB students everywhere. 🎓

## Code of Conduct

Be nice. We're all stressed IB students here. Help each other out, and remember that everyone is learning.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce** the issue
- **Expected behavior** vs. actual behavior
- **Screenshots** if applicable
- **System info**: macOS version, Python version
- **Log files** from `logs/tracker.log`

### Suggesting Features

Feature suggestions are welcome! Before suggesting:

1. Check if it's already suggested in issues
2. Explain **why** this feature would be useful
3. Provide **use cases** (especially IB-related ones!)
4. Be specific about what you want

### Pull Requests

1. Fork the repo
2. Create a branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Test thoroughly
5. Commit: `git commit -m "feat: Add amazing feature"`
6. Push: `git push origin feature/amazing-feature`
7. Open a Pull Request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/Study-Timer.git
cd Study-Timer

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies (optional)
pip install black flake8 pytest

# Initialize database
python src/init_db.py
```

## Coding Standards

### Python Style
- Follow PEP 8 (mostly)
- Use descriptive variable names
- Add docstrings to functions and classes
- Comment complex logic

Example:
```python
def calculate_study_time(sessions):
    """
    Calculate total study time from sessions.
    
    Args:
        sessions (list): List of session dictionaries
        
    Returns:
        int: Total seconds of study time
    """
    return sum(s['duration'] for s in sessions if s['is_study'])
```

### Commit Messages

Use conventional commits:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc.)
- `refactor:` Code refactoring
- `test:` Adding tests
- `chore:` Maintenance tasks

Examples:
```
feat: Add support for Notion app tracking
fix: Browser tracker crashes on empty URL
docs: Update installation guide for macOS Ventura
```

### File Organization

- **Trackers** go in `src/trackers/`
- **Dashboard code** in `src/dashboard/`
- **Config changes** in `src/config.py`
- **Tests** should mirror the structure (e.g., `tests/test_app_tracker.py`)

## Testing

Before submitting:

1. Test your changes manually
2. Run the test script: `./test.sh`
3. Check for any errors in the logs
4. Test on a fresh database if possible

## Adding New Trackers

Want to add a new tracking capability? Here's the structure:

```python
# src/trackers/your_tracker.py

class YourTracker:
    """Brief description of what this tracks"""
    
    def __init__(self):
        # Initialize any needed variables
        pass
    
    def get_data(self):
        """
        Main method to get tracking data
        
        Returns:
            dict: Tracking information
        """
        # Your implementation
        pass
```

Then import it in `src/trackers/__init__.py`:
```python
from .your_tracker import YourTracker
```

## Adding New Dashboard Features

Dashboard endpoints go in `src/dashboard/app.py`:

```python
@app.route('/api/your_endpoint')
def api_your_endpoint():
    """Get your data"""
    conn = get_db_connection()
    # Query database
    # Return JSON
    return jsonify(data)
```

Update the HTML in `src/dashboard/templates/index.html` to display the data.

## Documentation

When adding features, update:

- `README.md` - If it's a major feature
- `FEATURES.md` - Detailed feature description
- `CHANGELOG.md` - Under "Unreleased" section
- Code comments and docstrings

## Ideas for Contributions

Here are some areas that need work:

### Easy (Good First Issues)
- [ ] Add more study apps to default config
- [ ] Add more IB-themed quotes
- [ ] Improve error messages
- [ ] Add more file type detection
- [ ] Fix typos in documentation

### Medium
- [ ] Add export to CSV feature
- [ ] Create weekly email summaries
- [ ] Add dark mode to dashboard
- [ ] Improve subject categorization algorithm
- [ ] Add study goals and reminders

### Hard
- [ ] Windows support
- [ ] Linux support
- [ ] Mobile app for viewing stats
- [ ] Cloud sync (optional)
- [ ] Machine learning for automatic categorization
- [ ] Integration with calendar apps

### IB-Specific Features
- [ ] Subject-specific time tracking
- [ ] CAS hours integration (view, don't inflate!)
- [ ] EE progress tracker with milestones
- [ ] IA deadline reminders
- [ ] Predicted grade calculator based on study time
- [ ] Exam countdown timer

## Questions?

- Open an issue with the "question" label
- Start discussions in GitHub Discussions
- Or just try it and learn as you go - that's the IB way! 😄

## Recognition

Contributors will be added to the README. Major contributors get eternal glory and bragging rights.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Remember: We're all in this IB journey together. Every contribution helps a stressed student somewhere! 

Thank you for making Study Timer better!
