# UserInfoBot

A simple and powerful Telegram bot to fetch user, group, and channel information easily.

---

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/AmirKenzo/UserInfoBot.git && cd UserInfoBot
```

### 2. Configure Environment Variables

Rename `.env.example` to `.env` and edit it:

```bash
mv .env.example .env && nano .env
```

Fill in your own `API_ID`, `API_HASH`, `BOT_TOKEN`, and `USERNAME_BOT` in the `.env` file.

---

## ⚡ Install uv (Fast Python Runner)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh && source $HOME/.local/bin/env
```

`uv` is a modern Python package manager and runner, much faster than pip.

---

## 🛠️ Run the Bot

After setting up the environment:

```bash
uv run main.py
```

---

## 🔥 Auto Start Bot on Server (Systemd)

To make the bot auto-run on reboot:

1. Create a new service file:

```bash
nano /etc/systemd/system/UserInfoBot.service
```

Paste the following content inside:

```ini
[Unit]
Description=UserInfoBot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/UserInfoBot
ExecStart=/root/.local/bin/uv run main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

> Make sure the `WorkingDirectory` and `ExecStart` paths match your setup.

---

### 2. Enable & Start the Service

```bash
sudo systemctl enable UserInfoBot.service
sudo systemctl start UserInfoBot.service
```

If you want to manually manage the service:

```bash
sudo systemctl restart UserInfoBot.service
sudo systemctl stop UserInfoBot.service
```

---

## 📜 Logs

To view real-time logs of the bot:

```bash
journalctl -u UserInfoBot.service -f
```

---

## 📢 Credits

- Developed by [Amir Kenzo](https://github.com/AmirKenzo)
- Powered by [Telethon](https://docs.telethon.dev/)

---

## 🌟 Star this repo if you like it!
