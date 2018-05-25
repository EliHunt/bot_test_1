
# coding: utf-8

# In[1]:


import pymysql

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
import json
import boto3
import uuid


host="myfirsttest.cykdq8apu8h8.us-east-2.rds.amazonaws.com"
port=3306
dbname="telegram_db"
user="idarmiakov"
password="leecun12"

conn = pymysql.connect(host, user=user,port=port,passwd=password, db=dbname)
cursor = conn.cursor()

updater = Updater(token='510382787:AAEUmDunqjjC6kfRfOYCs0t8pBPWHD1wfTc')
dispatcher = updater.dispatcher

app = ClarifaiApp(api_key='e950cef735cb4744b0d2a7c3313a629f')
model = app.models.get("general-v1.3")

def start(bot, update):
    print(update)
    print(update.message.chat.username)
    bot.send_message(chat_id=update.message.chat_id, text="Hello, "+update.message.chat.username+" !")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)

def caps(bot, update, args):
    text_caps = ' '.join(args).upper()
    bot.send_message(chat_id=update.message.chat_id, text=text_caps)

caps_handler = CommandHandler('caps', caps, pass_args=True)
dispatcher.add_handler(caps_handler)


def downloadPhoto(bot, update):
    print("test/"+str(update.message.chat.id)+"_"+str(update.update_id))
    str1= "test/"+str(update.message.chat.id)+"_"+str(update.update_id)
    file_id = update.message.photo[-1].file_id
    newFile = bot.getFile(file_id)
    aws_access_key_id_r = 'AKIAIVX6IBHJAWWVXDYA'
    aws_secret_access_key_r = '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'
    s3client = boto3.client('s3',aws_access_key_id=aws_access_key_id_r, aws_secret_access_key=aws_secret_access_key_r)
    s3res = boto3.resource('s3',aws_access_key_id=aws_access_key_id_r, aws_secret_access_key=aws_secret_access_key_r)
    newFile.download("tmp.jpg")
    data = open("tmp.jpg", 'rb')
    s3res.Bucket('telegrambotbucket').put_object(Key=str1+".jpg", Body=data)
    str2 = 'insert into user_picture values '+'('+str(update.message.chat.id)+',"'+str1+'",now())'
    print(str2)
    cursor.execute(str2)
    conn.commit()
    bot.send_message(chat_id=update.message.chat_id, text="Got your push! Recognising...")
    bot.send_message(chat_id=update.message.chat_id, text="It's a "+(json.loads(json.dumps(model.predict([ClImage(file_obj=open('tmp.jpg', 'rb'))])["outputs"][0]))["data"]["concepts"][0]["name"]))
    bot.send_message(chat_id=update.message.chat_id, text="It's a "+(json.loads(json.dumps(model.predict([ClImage(file_obj=open('tmp.jpg', 'rb'))])["outputs"][0]))["data"]["concepts"][1]["name"]))
    bot.send_message(chat_id=update.message.chat_id, text="It's a "+(json.loads(json.dumps(model.predict([ClImage(file_obj=open('tmp.jpg', 'rb'))])["outputs"][0]))["data"]["concepts"][2]["name"]))
    bot.send_message(chat_id=update.message.chat_id, text="It's a "+(json.loads(json.dumps(model.predict([ClImage(file_obj=open('tmp.jpg', 'rb'))])["outputs"][0]))["data"]["concepts"][3]["name"]))
    bot.send_message(chat_id=update.message.chat_id, text="It's a "+(json.loads(json.dumps(model.predict([ClImage(file_obj=open('tmp.jpg', 'rb'))])["outputs"][0]))["data"]["concepts"][4]["name"]))
    bot.send_message(chat_id=update.message.chat_id, text="It's a "+(json.loads(json.dumps(model.predict([ClImage(file_obj=open('tmp.jpg', 'rb'))])["outputs"][0]))["data"]["concepts"][5]["name"]))
    bot.send_message(chat_id=update.message.chat_id, text="It's a "+(json.loads(json.dumps(model.predict([ClImage(file_obj=open('tmp.jpg', 'rb'))])["outputs"][0]))["data"]["concepts"][6]["name"]))
photoDownloadHandler = MessageHandler(Filters.photo, downloadPhoto) 
dispatcher.add_handler(photoDownloadHandler)



updater.start_polling()






