# 📢 ArisSuggestion Bot

Telegram bot for user suggestions moderation and publishing

---

## 🌍 Languages

**[English](#english)** | **[Русский](#русский)**

---

## English

### 🚀 Features

- **User-friendly interface** for submitting suggestions
- **Moderation queue** with approve/reject system
- **Automatic publishing** to configured channel
- **SQLite database** for suggestion tracking

### ⚙️ Installation

1. Clone repository:

```bash
git clone https://github.com/yourusername/SuggestionBot.git
cd SuggestionBot
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure environment:

```bash
cp .env.example .env
nano .env  # Edit with your credentials
```

### 🔧 Configuration

`.env` template:

```env
BOT_TOKEN=your_telegram_bot_token
ADMIN_GROUP_ID=-1001234567890
CHANNEL_ID=@your_channel
```

### 🏃♂️ Running

```bash
python run.py
```

### 📚 Project Structure

```
├── app/
│   ├── handlers.py    # Message processors
│   ├── keyboards.py   # Interactive buttons
│   ├── database.py    # DB operations
│   └── config.py      # Configuration loader
├── data/              # Database storage
├── .env               # Secrets
└── run.py             # Entry point
```

---

## Русский

### 🚀 Особенности

- **Удобный интерфейс** для отправки предложений
- **Система модерации** с одобрением/отклонением
- **Автопубликация** в указанный канал
- **SQLite база данных** для отслеживания предложений

### ⚙️ Установка

1. Клонируйте репозиторий:

```bash
git clone https://github.com/yourusername/SuggestionBot.git
cd SuggestionBot
```

2. Установите зависимости:

```bash
pip install -r requirements.txt
```

3. Настройте окружение:

```bash
cp .env.example .env
nano .env  # Отредактируйте параметры
```

### 🔧 Конфигурация

Пример `.env`:

```env
BOT_TOKEN=ваш_токен_бота
ADMIN_GROUP_ID=-1001234567890
CHANNEL_ID=@ваш_канал
```

### 🏃♂️ Запуск

```bash
python run.py
```

### 📚 Структура проекта

```
├── app/
│   ├── handlers.py    # Обработчики сообщений
│   ├── keyboards.py   # Интерактивные кнопки
│   ├── database.py    # Работа с БД
│   └── config.py      # Загрузчик конфигурации
├── data/              # Хранилище базы данных
├── .env               # Секретные данные
└── run.py             # Точка входа
```
