import Telegram, { type Message } from 'node-telegram-bot-api'
import request from 'request'
import config from './config.js'
import { sleep } from './utils.js'

const token = config.botToken
if (!token) {
  throw new Error('BOT_TOKEN is not set')
}

const bot = new Telegram(token, {
  polling: true,
})

const listenToMessages = (message: Message) => {
  const { text: messageText, chat, from } = message

  if (messageText === '/start') {
    bot.sendMessage(chat.id, '👋 Hi, I am a bot for downloading TikTok videos.')

    sleep(500).then(() =>
      bot.sendMessage(chat.id, '✨ Please send the video link'),
    )
  } else if (messageText?.includes('tiktok.com')) {
    bot.sendMessage(chat.id, '⏳Please wait...').then(waitMessage => {
      const tikTokApiUrl =
        'https://www.tikwm.com/api/?url=' + messageText + '&hd=1'

      request(tikTokApiUrl, function (error, response, body) {
        const json = JSON.parse(body)

        console.log('Received JSON:', json)

        if (!json || !json?.data) {
          bot.deleteMessage(chat.id, waitMessage.message_id)
          bot.sendMessage(
            chat.id,
            "😔 Sorry, I can't download this video right now. Please try again later.",
          )
        } else {
          bot.deleteMessage(chat.id, message.message_id)
          bot.deleteMessage(chat.id, waitMessage.message_id)

          const senderFirstName = from?.first_name ?? 'Unknown'
          const senderLastName = from?.last_name ? ` ${from.last_name}` : ''
          const senderName = `${senderFirstName}${senderLastName}`
          const caption = `📤 Shared by: ${senderName}`

          sleep(500).then(() =>
            bot.sendVideo(chat.id, json.data.hdplay, { caption }),
          )
        }
      })
    })
  }
}

bot.on('message', listenToMessages)
