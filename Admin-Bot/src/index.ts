import TelegramBot, { type ChatId } from 'node-telegram-bot-api';
import api from './api';
import test from 'node:test';

const token ='7312387046:AAEOMYPTPfiFC184dNGpFWg5m39fHQob8rw'; //'6895848546:AAEt6Yo4Ub7uSI7LX8oS2bmphA5Y5epF7g8';
const bot = new TelegramBot(token, { polling: true });

let firstNumber: number,
  secondNumber = 0;
let longMessage=false;
let message="";
let _chatId=0;

let isChangeSettings=0;
let botsThreads=-1;
let botsMaxMessages=-1;



let state = "start"

bot.onText(/\/start/, async msg => {
  state="start"
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
  state="message"
  const chatId = msg.chat.id;
  await bot.sendMessage(
    chatId,
    'which bots you want to choose to spam your message (like 1,10)',
  );
});

bot.onText(/\/show_groups/, async msg => {
  state = "show_groups"
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
  state="join_group"
  const chatId = msg.chat.id;
  await bot.sendMessage(
    chatId,
    'Enter Group link',
  );
});


bot.onText(/\/delete_group/, async msg => {
  state = "delete_group"
  const chatId = msg.chat.id;
  await bot.sendMessage(
    chatId,
    'Enter Group ID',
  );
});

bot.onText(/\/show_settings/, async msg => {
  state = "show_settings"
  const chatId = msg.chat.id;
  const result = await api.getSenderSettings();
  const botsThreads=result['workingBotsAtSameTime']
  const maxMessage=result['botMaxMessages']
  const reply = "The system is currently running ("+botsThreads+") bots at the same time. Each bot will send ("+maxMessage+") message before moving on to the next bot"
  bot.sendMessage(chatId,reply);

});


bot.onText(/\/change_settings/, async msg => {
  state = "change_settings"
  const chatId = msg.chat.id;
  const { data } = await api.getCount();
  let reply="";

  if (data.unavailable == 0){
    reply="Choose bots' speed. \nEnter a number from 1 to "+10+"\n*Note*\n High number will increase the bots banned possibality\n";
  }
  else{
    reply="Choose bots' speed. \nEnter a number from 1 to "+data.unavailable+"\n*Note*\n High number will increase the bots banned possibality\n";

  }
  isChangeSettings=1;
  bot.sendMessage(chatId,reply);

});

bot.on('message', async msg => {
  const chatId = msg.chat.id;
  //console.log("chat id"+chatId)
  const text = msg.text;
  if (text?.startsWith('/')) {
    return;
  }
  if (state=="delete_group"){
    const result = await api.deleteGroup(text??"")
    console.log(result)
    bot.sendMessage(chatId,result['message']);
  }
  else if(state == "change_settings" && isChangeSettings==1 && botsThreads == -1){
    botsThreads=Number(text)
    const reply="Now choose bots' Time before taking a rest . \n\nEnter a number of messages The bot will send before taking the rest and changing to another bot to work";
    isChangeSettings=2;
    bot.sendMessage(chatId,reply);
  }

  else if(state == "change_settings" &&isChangeSettings == 2 && botsMaxMessages == -1){
    botsMaxMessages = Number(text)
    const reply="Great each bot now will work from "+3*botsMaxMessages+" sec to"+5*botsMaxMessages+" sec then we move to next bot ";
    isChangeSettings=3;
    bot.sendMessage(chatId,reply);
    const result = await api.changeSenderSettings(botsThreads,botsMaxMessages)
    bot.sendMessage(chatId,result['message']);
    botsMaxMessages=-1;
    botsThreads=-1;
    isChangeSettings=0;
  }

  else if (state == "message" && text?.match(/^\d+,\d+$/)) {
    //validate the input

    [firstNumber, secondNumber] = String(text).split(',').map(Number);
    bot.sendMessage(chatId, 'now you can forward the message you want to spam');
  } 
  else if (state == "message" && firstNumber !== 0 && secondNumber !== 0) {
    
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
  else if (state == "join_group" && text?.startsWith("https://t.me")){
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

/*
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
*/
console.log('Bot is running!');
