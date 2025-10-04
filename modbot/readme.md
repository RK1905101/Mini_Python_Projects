# DarogaJi

DarogaJi is a powerful and customizable Discord moderator bot built with Python and the Discord API. It helps server administrators automate moderation tasks, enforce rules, and keep communities safe and welcoming.

## Features

- Automated moderation (kick, ban, mute, warn)
- Customizable command prefix
- Role-based permissions
- Anti-spam and anti-link filters
- Logging of moderation actions
- Easy to extend with new commands

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/anandku06/darogaji.git
   cd darogaji
   ```

2. **Create and activate a virtual environment:**
   ```sh
   python3 -m venv myenv
   source myenv/bin/activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

## Configuration

1. **Create a Discord bot and get your token:**  
   Follow the [Discord Developer Portal](https://discord.com/developers/applications) to create a bot and copy the token.

2. **Set up environment variables or a config file:**  
   Store your bot token securely, for example in a `.env` file:
   ```
   DISCORD_TOKEN=your-bot-token-here
   ```

## Usage

Start the bot with:

```sh
python bot.py
```

The bot will join your server and begin moderating according to the configured rules.

## Commands

| Command         | Description                | Example                |
|-----------------|---------------------------|------------------------|
| `!kick @user`   | Kick a user               | `!kick @spammer`       |
| `!ban @user`    | Ban a user                | `!ban @troll`          |
| `!mute @user`   | Mute a user               | `!mute @noisy`         |
| `!warn @user`   | Warn a user               | `!warn @rulebreaker`   |

*You can customize or add more commands in the source code.*

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License.

---

*Built with [discord.py](https://github.com/Rapptz/discord.py) and Python 3.12.*