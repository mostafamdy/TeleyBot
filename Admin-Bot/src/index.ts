import TelegramBot, { type ChatId } from 'node-telegram-bot-api';
import api from './api';
import test from 'node:test';

const token ='7312387046:AAEOMYPTPfiFC184dNGpFWg5m39fHQob8rw'; //'6895848546:AAEt6Yo4Ub7uSI7LX8oS2bmphA5Y5epF7g8';
const bot = new TelegramBot(token, { polling: true });

let firstNumber: number,
  secondNumber = 0;
let longMessage=false
let message="";
let _chatId=0;
let isDeleteGroup=false

bot.onText(/\/start/, async msg => {
  isDeleteGroup=false
  const { data } = await api.getCount();
  const chatId = msg.chat.id;
  await bot.sendMessage(
    chatId,
    'Welcome to admin bot you have ' +
      data.unavailable +
      ' working Bots and ' +
      data.available +
      ' free bots and ' +
      data.banned +
      ' banned bots',
  );
});

bot.onText(/\/message/, async msg => {
  isDeleteGroup=false
  const chatId = msg.chat.id;
  await bot.sendMessage(
    chatId,
    'which bots you want to choose to spam your message (like 1,10)',
  );
});

bot.onText(/\/show_groups/, async msg => {
  isDeleteGroup=false
  
  const chatId = msg.chat.id;

  const data = await api.getGroups();
  const dataString = JSON.stringify(data,null, 2)
  if (dataString.length>4000){
    longMessage=true;
    message=dataString;
    _chatId=chatId
  }
  else{
    await bot.sendMessage(
      chatId,
      dataString
    );
  }

});

setInterval(async ()=>{
  if (longMessage){
    for(let i=0; i< message.length; i+=4000){
      await bot.sendMessage(
        _chatId,
        message.substring(i,i+4000)
      );
    }
    longMessage=false
  }
}, 1000)

bot.onText(/\/join_group/, async msg => {
  isDeleteGroup=false
  const chatId = msg.chat.id;
  await bot.sendMessage(
    chatId,
    'Enter Group link',
  );
});


bot.onText(/\/delete_group/, async msg => {
  const chatId = msg.chat.id;
  isDeleteGroup=true
  await bot.sendMessage(
    chatId,
    'Enter Group ID',
  );
});

bot.on('message', async msg => {
  const chatId = msg.chat.id;
  //console.log("chat id"+chatId)
  const text = msg.text;
  if (text?.startsWith('/')) {
    isDeleteGroup=false
    return;
  }
  if (isDeleteGroup){
    const result = await api.deleteGroup(text??"")
    console.log(result)
    bot.sendMessage(chatId,result['message']);
  }
  if (text?.match(/^\d+,\d+$/)) {
    //validate the input

    [firstNumber, secondNumber] = String(text).split(',').map(Number);
    bot.sendMessage(chatId, 'now you can forward the message you want to spam');
  } 
  else if (firstNumber !== 0 && secondNumber !== 0) {
    
    console.log(msg.text)
    console.log(msg.message_id);

    const { message } = await api.forward(
      firstNumber,
      secondNumber,
      msg.text??"no messages sent",
    );
    bot.sendMessage(chatId, message);
    firstNumber = 0;
    secondNumber = 0;
  }
  else if (text?.startsWith("https://t.me")){
    if (text.includes("addlist")){
      const { message } = await api.joinGroupList(text);
      bot.sendMessage(chatId, message);
    }
    else{
      const { message } = await api.joinGroup(text);
      bot.sendMessage(chatId, message);
    }
  }
});


bot.onText(/\/price/, (msg, match) => {
  const opts = {
      reply_markup: {
          inline_keyboard: [
              [{
                      text: 'EUR',
                      callback_data: JSON.stringify({
                          'command': 'price',
                          'base': 'EUR'
                      })
                  },
                  {
                      text: 'USD',
                      callback_data: JSON.stringify({
                          'command': 'price',
                          'base': 'USD'
                      })
                  }
              ]
          ]
      }
  };
  bot.sendMessage(msg.chat.id, 'Choose currency', opts);
});


bot.on('callback_query', function onCallbackQuery(callbackQuery) {
  const data = JSON.parse(callbackQuery.data??"");
  const opts = {
      chat_id: callbackQuery.message?.chat.id,
      message_id: callbackQuery.message?.message_id,
  };
  if (data.command === 'price') {
    console.log(data.base)
    bot.sendMessage(opts.chat_id??"", `The current price of ETP is: hss ${data.base}`);
    bot.answerCallbackQuery(callbackQuery.id)
          
          
  }
});


bot.on('polling_error', error => console.error('Polling error:', error));

console.log('Bot is running!');
