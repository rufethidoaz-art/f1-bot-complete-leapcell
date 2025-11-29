# GitHub Upload Preparation Guide

## 🧹 Clean Project for GitHub Upload

This guide helps you prepare a clean, Railway-ready version of your F1 Telegram Bot for GitHub upload.

---

## 📁 Phase 1: Project Cleanup

### Step 1: Rename Main Bot File

Rename your main bot file for clarity:

```bash
# Current file
leapcell_f1_bot.py → f1_bot.py

# Update imports in other files if needed
```

### Step 2: Remove Leapcell-Specific Files

Delete these files (no longer needed):
```
❌ leapcell.yaml (Railway uses railway.toml)
❌ DEPLOYMENT_GUIDE.md (outdated, use Railway guides)
❌ DEPLOYMENT_FIX_GUIDE.md (outdated)
❌ LEAPCELL_SETUP_GUIDE.md (not needed)
❌ validate_deployment.py (create Railway-specific version)
```

### Step 3: Create Clean Project Structure

Your final project should contain:
```
📁 f1-telegram-bot/
├── 📄 f1_bot.py                    # Main bot application
├── 📄 requirements.txt             # Python dependencies
├── 📄 optimized_scraper.py         # Live timing scraper
├── 📄 fallback_scraper.py          # Backup scraper
├── 📄 streams.txt                  # Default stream links
├── 📄 user_streams.json            # User data storage
├── 📄 Dockerfile                   # Container configuration
├── 📄 railway.toml                 # Railway configuration
├── 📄 .gitignore                   # Git ignore file
├── 📄 README.md                    # Updated project documentation
├── 📄 Local_Testing_Guide.md       # Local testing instructions
├── 📄 Railway_Deployment_Guide.md  # Deployment guide
└── 📄 GitHub_Upload_Preparation.md # This file
```

---

## 🔧 Phase 2: Update Configuration Files

### Step 4: Update f1_bot.py

Update references in your main bot file:

```python
# Update any Leapcell-specific references
# Change:
# "Leapcell Test" → "Railway Deployment"
# "leapcell_f1_bot" → "f1_bot"
# Any Leapcell URLs → Railway URLs or remove them
```

### Step 5: Create .gitignore

Create `.gitignore` file:

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual environments
env/
venv/
f1_bot_env/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Logs
*.log
logs/

# Runtime data
pids/
*.pid
*.seed
*.pid.lock

# Coverage directory used by tools like istanbul
coverage/

# nyc test coverage
.nyc_output

# Dependency directories
node_modules/

# Optional npm cache directory
.npm

# Environment variables
.env
.env.local
.env.development
.env.test
.env.production

# User streams data (optional - keep if you want to preserve user data)
# user_streams.json

# Temporary files
*.tmp
*.temp
```

### Step 6: Update README.md

Create a clean README.md:

```markdown
# F1 Telegram Bot

🏎️ **Live Formula 1 updates, standings, race schedules, and live timing for Telegram**

## ✨ Features

- 🏆 **Driver & Constructor Standings** - Current season rankings
- 📅 **Race Schedule** - Upcoming races with weather forecasts
- 🏁 **Live Timing** - Real-time position updates during F1 sessions
- 🎥 **Stream Management** - Personal stream links and sharing
- 🌤️ **Weather Information** - Race weekend weather forecasts
- 📱 **Telegram Integration** - Full Telegram bot with interactive menu

## 🚀 Quick Start

### Local Development

1. **Clone and Setup**
   ```bash
   git clone https://github.com/yourusername/f1-telegram-bot.git
   cd f1-telegram-bot
   
   # Create virtual environment
   python -m venv f1_bot_env
   source f1_bot_env/bin/activate  # Linux/Mac
   # or f1_bot_env\Scripts\activate  # Windows
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

3. **Set Environment Variables**
   Create `.env` file:
   ```env
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   PORT=8080
   ```

4. **Run Locally**
   ```bash
   python f1_bot.py
   ```

5. **Test Your Bot**
   - Find your bot on Telegram: `@YourBotName`
   - Send `/start` to begin

### Railway Deployment (Recommended)

This bot is optimized for **[Railway](https://railway.app)** deployment:

1. **Deploy to Railway**
   [![Deploy on Railway](https://railway-static.s3.us-east-2.amazonaws.com/deploy-button.svg)](https://railway.app/button/clone)

2. **Set Environment Variables**
   - `TELEGRAM_BOT_TOKEN`: Your bot token from @BotFather
   - `PORT`: `8080` (default)

3. **Configure Webhook**
   ```bash
   curl -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/setWebhook" \
     -d "url=https://your-service.up.railway.app/webhook"
   ```

## 🤖 Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Welcome message and menu |
| `/menu` | Show interactive menu |
| `/standings` | Driver standings |
| `/constructors` | Constructor standings |
| `/lastrace` | Last race results |
| `/nextrace` | Next race schedule |
| `/live` | Live timing (during sessions) |
| `/streams` | Stream links |
| `/addstream` | Add personal stream |
| `/removestream` | Remove stream |
| `/playstream` | Get stream link |
| `/streamhelp` | Stream management help |

## 🔧 Technical Details

### Architecture
- **Framework**: Flask + python-telegram-bot
- **Database**: JSON files for user data
- **Scraping**: Playwright with Chromium
- **APIs**: OpenF1, Jolpica F1 API, Ergast API
- **Deployment**: Docker container on Railway

### Requirements
- Python 3.11+
- Playwright with Chromium browser
- Telegram Bot Token
- Internet connection for F1 APIs

### File Structure
```
├── f1_bot.py              # Main bot application
├── optimized_scraper.py   # Live timing scraper
├── fallback_scraper.py    # Backup scraper
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container configuration
├── railway.toml          # Railway deployment config
└── streams.txt           # Default stream links
```

## 🧪 Testing

Run comprehensive local tests:

```bash
# Test all components
python comprehensive_test.py

# Test bot functions
python test_bot_functions.py

# Test scraper
python test_scraper.py
```

See [`Local_Testing_Guide.md`](Local_Testing_Guide.md) for detailed testing procedures.

## 📖 Documentation

- [`Local_Testing_Guide.md`](Local_Testing_Guide.md) - Test locally before deployment
- [`Railway_Deployment_Guide.md`](Railway_Deployment_Guide.md) - Complete deployment guide
- [`Railway_Configuration_Files.md`](Railway_Configuration_Files.md) - Configuration details

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Telegram Bot API](https://core.telegram.org/bots/api)
- [OpenF1 API](https://api.openf1.org/)
- [Jolpica F1 API](https://jolpica.com/)
- [python-telegram-bot](https://python-telegram-bot.org/)

---

**Built with ❤️ for F1 fans worldwide** 🏎️💨
```

---

## 📋 Phase 3: Final Verification

### Step 7: Verify File Structure

Check your project structure:

```bash
# List all files (excluding .git)
find . -type f -name "*.py" -o -name "*.txt" -o -name "*.toml" -o -name "*.md" -o -name "Dockerfile" -o -name ".gitignore" | sort
```

Expected output:
```
./Dockerfile
./GitHub_Upload_Preparation.md
./Local_Testing_Guide.md
./Railway_Deployment_Guide.md
./Railway_Configuration_Files.md
./f1_bot.py
./fallback_scraper.py
./optimized_scraper.py
./requirements.txt
./railway.toml
./README.md
./streams.txt
./user_streams.json
./.gitignore
```

### Step 8: Test Local Functionality

Run the comprehensive test:

```bash
# Make sure you're in the project directory
python comprehensive_test.py
```

Ensure all tests pass before proceeding.

### Step 9: Validate Configuration Files

```bash
# Test Docker build
docker build -t f1-bot-test .

# Test railway.toml syntax (basic check)
python -c "import toml; toml.load('railway.toml'); print('railway.toml valid')"

# Test requirements.txt
pip check
```

---

## 🚀 Phase 4: GitHub Upload

### Step 10: Initialize Git Repository

```bash
# Initialize git (if not already done)
git init

# Add remote (replace with your GitHub repository URL)
git remote add origin https://github.com/yourusername/f1-telegram-bot.git

# Check git status
git status
```

### Step 11: Commit Files

```bash
# Add all files
git add .

# Commit with clear message
git commit -m "🚀 Initial commit: F1 Telegram Bot with Railway deployment

✨ Features:
- Live F1 timing with Playwright scraping
- Driver and constructor standings
- Race schedules with weather forecasts
- Stream management for users
- Railway deployment configuration
- Comprehensive testing suite

🔧 Technical:
- Flask + python-telegram-bot
- Docker containerized
- Playwright with Chromium
- Free Railway hosting ready"
```

### Step 12: Upload to GitHub

```bash
# Push to GitHub
git push -u origin main

# Verify upload
git status
```

### Step 13: Create GitHub Repository (if needed)

If repository doesn't exist:

1. Go to [GitHub](https://github.com)
2. Click "New repository"
3. Name: `f1-telegram-bot`
4. Description: "🏎️ F1 Telegram Bot with live timing, standings, and race information"
5. Set to Public (recommended for free plan)
6. Don't initialize with README (you have one)
7. Click "Create repository"
8. Follow the push instructions

---

## 🔗 Phase 5: Post-Upload Setup

### Step 14: Verify GitHub Repository

1. Visit your GitHub repository
2. Verify all files uploaded correctly
3. Check README.md renders properly
4. Ensure no sensitive data is exposed

### Step 15: Set Up Repository Features

1. **Add License** (optional):
   ```bash
   # Create LICENSE file (MIT)
   curl -s https://license.md/license/mit.txt > LICENSE
   git add LICENSE
   git commit -m "Add MIT License"
   git push
   ```

2. **Create Issue Templates** (optional):
   Create `.github/ISSUE_TEMPLATE/bug_report.md`

3. **Add Repository Topics**:
   - `f1`
   - `telegram-bot`
   - `formula-1`
   - `python`
   - `railway`
   - `playwright`

### Step 16: Prepare for Railway Deployment

1. **Copy Repository URL**: `https://github.com/yourusername/f1-telegram-bot.git`

2. **Prepare Environment Variables**:
   - `TELEGRAM_BOT_TOKEN`: Get from @BotFather
   - Other variables (see deployment guide)

3. **Review Deployment Guides**:
   - [`Railway_Deployment_Guide.md`](Railway_Deployment_Guide.md)
   - [`Local_Testing_Guide.md`](Local_Testing_Guide.md)

---

## ✅ Clean Upload Checklist

Before declaring the upload complete:

### File Structure ✅
- [ ] Main bot file renamed to `f1_bot.py`
- [ ] All Leapcell files removed
- [ ] Railway configuration files added
- [ ] Documentation files updated
- [ ] `.gitignore` created
- [ ] `README.md` updated

### Code Quality ✅
- [ ] All imports updated
- [ ] No hardcoded secrets
- [ ] Environment variables used
- [ ] Error handling implemented
- [ ] Comments updated

### Testing ✅
- [ ] Comprehensive tests pass locally
- [ ] Docker build succeeds
- [ ] All bot functions work
- [ ] Playwright scraper functional
- [ ] Health endpoints respond

### GitHub Upload ✅
- [ ] Repository created
- [ ] All files pushed successfully
- [ ] README renders correctly
- [ ] No sensitive data exposed
- [ ] Repository is public (recommended)

### Deployment Ready ✅
- [ ] Railway configuration complete
- [ ] Environment variables documented
- [ ] Deployment guides available
- [ ] Troubleshooting guides provided

---

## 🎉 You're Ready!

Your cleaned F1 Telegram Bot project is now ready for:

1. **GitHub Upload** ✅ Completed
2. **Railway Deployment** 🚀 Next step
3. **Production Use** 🎯 Final goal

**Next Steps:**
1. Follow [`Railway_Deployment_Guide.md`](Railway_Deployment_Guide.md) for deployment
2. Configure your Telegram bot token
3. Set up webhook for live bot functionality
4. Monitor performance and enjoy your F1 bot! 🏎️💨

---

**Clean project, clear documentation, ready for success!** 🚀