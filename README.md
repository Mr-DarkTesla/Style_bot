# Style_Bot
@style_dls_fall_bot
## Description
Simple style transferring telegram bot. Takes two pictures and transfer style from one to another. Output image is 256x256.

Language: Python

Libs: torch, torchvision, telebot, flask, vedis

Deployed on: Heroku.

Somtimes the bot crushes deu to memory limitation on heroku.
In that case you need to /reset and wait a little.
It is permanently exceeding memory quota.
## Bot commands
/start - To start the conversation!

/reset - To reset (almost) everything

/help - To receive help I guess...

## Model Used
I used some of pre-trained VGG19 layers to extract "style" features from image
and transfer it. Then fine-tune model to properly display content of the origin picture. 
I used MSE as a content loss funktion and the style loss of layer is the squared error
between the gram matrices of the intermediate representation of the style image
and the input base image. Combined losses with coefficients is total loss.
Lastly I train my model with adam optimizer and transferring is done.

## Contacts
My name: George Yakushev (Георгий Якушев)

Telegram: @MrDarkTesla

E-mail: yakushev.ga@phystech.edu

