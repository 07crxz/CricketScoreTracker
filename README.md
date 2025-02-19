# Cricket Score Bot

A Python bot that scrapes live cricket scores from Cricbuzz and sends updates to Discord via webhooks. 

## Features

- 🏏 Real-time cricket score updates from Cricbuzz
- 📊 Formatted score updates in Discord
- ⏱️ Updates every 5 seconds
- 🔄 Automatic retry mechanism for failed requests
- 🚀 Easy to configure and run

## Setup

1. Clone this repository
2. Install the required Python packages:
```py
pip install requests beautifulsoup4
```

3. Configure your Discord webhook URL:
   - Create a webhook in your Discord server
   - Copy the webhook URL
   - Replace the `DISCORD_WEBHOOK_URL` in `score.py` with your webhook URL

## Configuration

The bot can be configured by modifying the following constants in `score.py`:

```py
FETCH_INTERVAL = 5  # Update interval in seconds
MAX_RETRIES = 3     # Number of retries for failed requests
```

## Usage

Run the bot using:

```bash
python score.py
```

The bot will:
1. Fetch live matches from Cricbuzz
2. Continue running until manually stopped
3. Send formatted updates to Discord when scores change


## Example Discord Output

```
# Live Cricket Score Update

> **Gujarat Giants Women vs Mumbai Indians Women**
> *Live*

> **Gujarat Giants Women**: 142/5 (20)
> **Mumbai Indians Women**: 38/2 (5.4)
```

## Project Structure

- `score.py`: Main bot script
- `utils.py`: Helper functions for Discord messaging and score formatting

## Error Handling

The bot includes:
- Automatic retries for failed requests
- Graceful handling of parsing errors
- Detailed logging for troubleshooting

## Contributing

Feel free to:
- Open issues for bugs or feature requests
- Submit pull requests with improvements
- Suggest new features or enhancements

## License

This project is open source and available under the IIT Delhi License.
