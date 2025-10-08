## 📌 Overview
A Python-powered Discord bot using discord.py for automated voice channel management. Create hubs that generate sub‑channels on demand, enforce user/channel limits, and auto‑delete empty channels. Also provides useful moderation tools like message purging.

---

## ✨ Features

- 🎧 **Dynamic Voice Channels**
  - Turn any VC into a **VC Hub** that spawns temporary sub-channels.
  - Auto-move users into new sub-VCs on join.
  - Auto-delete sub-VCs when empty.

- ⚙️ **Configurable Limits**
  - `user_limit`: Max users per sub-VC.
  - `channel_limit`: Max sub-VCs per hub.

- 💬 **Slash Commands**
  - `/add-vc-hub` — Make a channel a VC hub.
  - `/remove-vc-hub` — Remove a VC hub.
  - `/list-vc-hubs` — View all active hubs.
  - `/help` — View all commands.

- 🔐 **Permission Control**
  - Requires **Manage Channels**, **Manage Messages**, and **Move Members**.

- 💾 **Persistent Storage**
  - Stores settings in **SQLite**.
  - Data survives restarts.

---

## 🚀 Usage

1. **Add a VC Hub**  
   `/add-vc-hub channel:<hub> user_limit:<n> channel_limit:<n>`

2. **Join the Hub**  
   - Bot creates sub-VC & moves you in.

3. **Automatic Cleanup**  
   - Sub-VCs removed when empty.

4. **Manage**  
   - `/list-vc-hubs` — View hubs.  

---

