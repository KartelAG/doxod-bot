# Telegram bot for Tinkoff Invest

Simple bot that calculates (in the very naive way) the current income of your portfolio

> *inspired by [Alexey Goloburdin](https://github.com/alexey-goloburdin)*


## Prerequisites:
Environment variables should be set:
```
TOKEN=tinkoff_invest_token

#when broker account was openned
BROKER_ACCOUNT_START=01.08.2020 

TELEGRAM_BOT_API_TOKEN=telegram_bot_api_token
TELEGRAM_ACCESS_ID=your_telegram_id
```

## Usage:
```
python tg_bot.py
```
then give you bot a command ```/income```

or just press a button ```Get income!```