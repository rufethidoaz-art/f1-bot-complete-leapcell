# F1 Telegram Bot - Leapcell Test Version

☁️ **Leapcell Deployment Test** - Optimized F1 Telegram Bot for Leapcell hosting platform.

## Features

- ✅ **Containerized deployment** with Docker
- ✅ **Scalable architecture** for high availability
- ✅ **Optimized web scraping** for Leapcell environment
- ✅ **Enhanced caching system** with error handling
- ✅ **Health check endpoints** for monitoring

## Leapcell Optimizations

- **Docker Container**: Isolated, reproducible deployments
- **Auto-scaling**: Scale based on demand
- **Global Distribution**: Fast content delivery
- **Built-in Monitoring**: Health checks and metrics
- **Persistent Data**: User streams and settings

## Deployment

1. Create a Leapcell account at [leapcell.io](https://leapcell.io)
2. Connect your Git repository
3. Use the `leapcell.yaml` configuration file
4. Set environment variable: `TELEGRAM_BOT_TOKEN`
5. Deploy your container!

## Environment Variables

- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token from @BotFather
- `PORT`: Port for the application (default: 8080)
- `PYTHON_VERSION`: Python version (3.11.0)
- `PLAYWRIGHT_BROWSERS_PATH`: Browser path for Playwright (0)

## Health Checks

- `GET /` - Basic status and deployment info
- `GET /health` - Health check endpoint

## Commands

All standard F1 bot commands with Leapcell optimizations:
- `/live` - Enhanced live timing with caching
- `/standings` - Driver standings
- `/constructors` - Constructor standings
- `/nextrace` - Next race schedule with weather
- `/lastrace` - Last race results
- `/streams` - Personal stream management

## Differences from Main Version

- Leapcell-specific container configuration
- Optimized for cloud-native deployment
- Enhanced error handling and monitoring
- Container-ready with health checks

## Configuration Files

- `leapcell.yaml` - Leapcell deployment configuration
- `Dockerfile` - Container build instructions
- `requirements.txt` - Python dependencies
- `leapcell_f1_bot.py` - Leapcell-optimized bot code

## Support

For Leapcell deployment issues, check Leapcell documentation or support channels.