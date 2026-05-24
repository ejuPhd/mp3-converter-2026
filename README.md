# MP4 to MP3 Converter for macOS

A lightweight, Python-based tool to extract audio from MP4 video files and convert them to MP3 format. Optimized for Apple Silicon (M1/M2/M3/M4) Macs and compatible with iTunes/Apple Music.

---

## Table of Contents

1. [Features](#features)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [Project Setup](#project-setup)
5. [Usage](#usage)
6. [Troubleshooting](#troubleshooting)
7. [GitHub Upload](#github-upload)
8. [License](#license)

---

## Features

- **Single file conversion**: Convert one MP4 to MP3
- **Batch conversion**: Convert entire folders of MP4 files at once
- **Recursive processing**: Include subdirectories in batch mode
- **Quality presets**: Choose from Standard (192k), Music (256k), Archive (320k), or Voice (128k)
- **iTunes optimized**: 44.1kHz sample rate, stereo, ID3v2.3 metadata tags
- **Apple Silicon native**: Uses ARM64-optimized ffmpeg via Homebrew
- **Progress tracking**: Visual progress bar for batch operations
- **Metadata preservation**: Copies artist/title/album info from source

---

## Requirements

| Component | Version | Purpose |
|-----------|---------|---------|
| macOS | 14.0+ (Tahoe 26.5 tested) | Operating system |
| Python | 3.13.5 | Runtime environment |
| VS Code | 1.119.0+ | Code editor |
| ffmpeg | Latest (via Homebrew) | Audio/video conversion engine |
| tqdm | 4.67.3+ | Progress bar library |

**Hardware tested on**: MacBook Pro M4 Pro, 16GB RAM

---

## Installation

### Step 1: Install Homebrew (if not already installed)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Step 2: Install ffmpeg

```bash
brew install ffmpeg
```

Verify installation:
```bash
ffmpeg -version
```

### Step 3: Verify Python 3.13.5

```bash
python3 --version
```

Should output: `Python 3.13.5`

If you need to install it:
```bash
brew install python@3.13
```

---

## Project Setup

### Step 1: Create Project Directory

```bash
mkdir -p ~/WebApps/mp3-converter
cd ~/WebApps/mp3-converter
```

### Step 2: Create Virtual Environment

```bash
python3 -m venv .venv
```

### Step 3: Activate Virtual Environment

```bash
source .venv/bin/activate
```

Your prompt should now show `(.venv)` at the beginning.

### Step 4: Upgrade pip

```bash
pip install --upgrade pip
```

### Step 5: Install Python Dependencies

```bash
pip install tqdm
```

Verify installation:
```bash
pip list | grep tqdm
```

Expected output: `tqdm 4.67.3`

### Step 6: Create Project Files

Create the following files in your project directory:

1. `mp4_to_mp3.py` — Main converter script (see code below)
2. `.vscode/settings.json` — VS Code workspace settings
3. `.gitignore` — Git ignore rules
4. `requirements.txt` — Dependency list

---

## File Structure

```
mp3-converter/
├── .venv/                  # Virtual environment (not tracked by Git)
├── .vscode/
│   └── settings.json       # VS Code interpreter configuration
├── .gitignore              # Files to ignore in Git
├── requirements.txt        # Python dependencies
├── mp4_to_mp3.py          # Main conversion script
└── README.md              # This file
```

---

## Usage

### Single File Conversion

```bash
python mp4_to_mp3.py song.mp4
```

Output: `song.mp3` in the same directory.

### Custom Output Location

```bash
python mp4_to_mp3.py concert.mp4 ~/Music/
```

Output: `~/Music/concert.mp3`

### Batch Conversion (All MP4s in a Folder)

```bash
python mp4_to_mp3.py --batch ~/Downloads/rips/
```

### Recursive Batch Conversion (Include Subfolders)

```bash
python mp4_to_mp3.py --batch ~/Downloads/rips/ --recursive
```

### Quality Presets

```bash
python mp4_to_mp3.py --preset archive symphony.mp4    # 320kbps max quality
python mp4_to_mp3.py --preset voice podcast.mp4        # 128kbps for speech
python mp4_to_mp3.py --preset music track.mp4          # 256kbps (default)
```

### View Help

```bash
python mp4_to_mp3.py --help
```

---

## Adding to iTunes/Apple Music

1. Open the **Music** app (or iTunes on older macOS)
2. Go to **File → Add to Library...** (or press `Cmd+O`)
3. Select your converted `.mp3` files
4. Or simply **drag and drop** the files into the Music app window

---

## Troubleshooting

### Issue: "Import 'tqdm' could not be resolved" (Pylance Error)

**Cause**: VS Code is using the wrong Python interpreter.

**Solution**:
1. Press `Cmd+Shift+P`
2. Type: `Python: Select Interpreter`
3. Choose: `Python 3.13.5 ('.venv': venv)`
4. If not listed, select "Enter interpreter path" and paste:
   ```
   /Users/YOUR_USERNAME/WebApps/mp3-converter/.venv/bin/python
   ```
5. Reload VS Code: `Cmd+Shift+P` → `Developer: Reload Window`

### Issue: "ffmpeg not found"

**Cause**: ffmpeg is not installed or not in PATH.

**Solution**:
```bash
brew install ffmpeg
```

Verify:
```bash
which ffmpeg
```

### Issue: "No such file or directory: mp4_to_mp3.py"

**Cause**: You're not in the project directory or the file doesn't exist.

**Solution**:
```bash
cd ~/WebApps/mp3-converter
ls -la mp4_to_mp3.py
```

If missing, create it (see Project Setup above).

### Issue: Permission Denied

**Solution**:
```bash
chmod +x mp4_to_mp3.py
```

---

## GitHub Upload Instructions

### Step 1: Initialize Git Repository

```bash
cd ~/WebApps/mp3-converter
git init
```

### Step 2: Configure Git (if not already done)

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Step 3: Create .gitignore

Create a file named `.gitignore` with this content:

```
# Virtual environment
.venv/

# Python cache
__pycache__/
*.pyc
*.pyo
*.pyd
.Python

# OS files
.DS_Store
Thumbs.db

# IDE
.vscode/settings.json
.idea/

# Output files
*.mp3
```

### Step 4: Stage Files

```bash
git add mp4_to_mp3.py
git add README.md
git add requirements.txt
git add .gitignore
git add .vscode/
```

### Step 5: Commit

```bash
git commit -m "Initial commit: MP4 to MP3 converter for macOS"
```

### Step 6: Create GitHub Repository

1. Go to https://github.com/ejuPhd
2. Click **New** (green button) or go to https://github.com/new
3. Repository name: `mp3-converter`
4. Description: `Python MP4 to MP3 converter optimized for macOS Apple Silicon`
5. Visibility: **Public** or **Private** (your choice)
6. **DO NOT** initialize with README, .gitignore, or license (we already have these)
7. Click **Create repository**

### Step 7: Link Local to Remote

```bash
git remote add origin https://github.com/ejuPhd/mp3-converter.git
```

### Step 8: Push to GitHub

```bash
git branch -M main
git push -u origin main
```

Enter your GitHub username and personal access token when prompted.

### Step 9: Verify

Visit `https://github.com/ejuPhd/mp3-converter` in your browser. Your files should be there.

---

## Creating a GitHub Personal Access Token

If you get an authentication error, you need a token:

1. Go to https://github.com/settings/tokens
2. Click **Generate new token (classic)**
3. Note: `mp3-converter push`
4. Expiration: 30 days (or as preferred)
5. Scopes: Check **repo** (full control of private repositories)
6. Click **Generate token**
7. **Copy the token immediately** (you can't see it again!)
8. Use this token as your password when `git push` asks

---

## Quick Reference Card

| Task | Command |
|------|---------|
| Activate venv | `source .venv/bin/activate` |
| Deactivate venv | `deactivate` |
| Run single conversion | `python mp4_to_mp3.py file.mp4` |
| Run batch conversion | `python mp4_to_mp3.py --batch ~/folder/` |
| Check ffmpeg | `ffmpeg -version` |
| Check Python | `python --version` |
| Check installed packages | `pip list` |
| Freeze dependencies | `pip freeze > requirements.txt` |
| Git status | `git status` |
| Git commit | `git commit -am "message"` |
| Git push | `git push origin main` |

---

## Credits

- **ffmpeg**: The universal media conversion tool (https://ffmpeg.org)
- **tqdm**: Fast, extensible progress bar (https://tqdm.github.io)
- **Python**: Programming language (https://python.org)
- **VS Code**: Editor (https://code.visualstudio.com)

---

## License

MIT License — Free for personal and commercial use.
# mp3-converter-2026
