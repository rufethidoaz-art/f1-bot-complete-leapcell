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
