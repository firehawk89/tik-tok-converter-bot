import Telegram from 'node-telegram-bot-api'
import request from 'request'
import config from './config.js'

const token = config.botToken
if (!token) {
  throw new Error('BOT_TOKEN is not set')
}

const bot = new Telegram(token, {
  polling: true,
})

const sleep = time => new Promise(resolve => setTimeout(resolve, time))

const listenToMessages = message => {
  const { text: messageText, chat } = message

  if (messageText == '/start') {
    bot.sendMessage(chat.id, '👋 Hi, I am a bot for downloading TikTok videos.')

    sleep(500).then(() =>
      bot.sendMessage(chat.id, '✨ Please send the video link'),
    )
  } else if (messageText.includes('tiktok.com')) {
    bot.sendMessage(chat.id, '⏳Please wait...')

    const tikTokApiUrl =
      'https://www.tikwm.com/api/?url=' + messageText + '&hd=1'

    request(tikTokApiUrl, function (error, response, body) {
      const json = JSON.parse(body)

      if (json.data == undefined) {
        bot.sendMessage(
          chat.id,
          "😔 Sorry, I can't download this video right now. Please try again later.",
        )
      } else {
        sleep(500).then(() => bot.sendVideo(chat.id, json.data.hdplay))
      }
    })
  } else {
    bot.sendMessage(msg.chat.id, '🧐 Please send a valid video link')
  }
}

bot.on('message', listenToMessages)
