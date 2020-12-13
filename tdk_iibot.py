from pyrogram import (
    Client, 
    Filters, 
    InlineQueryResultArticle, 
    InputTextMessageContent, 
    InlineKeyboardMarkup, 
    InlineKeyboardButton
)

import requests

TDK_Bot = Client(
    api_id="", #https://core.telegram.org/ buradan alın
    api_hash="", #https://core.telegram.org/ 
    session_name="", #sallayın burayı
    bot_token="", #tokeninizi girin
)

def tdk_fonk(kelime):
    r = requests.get(f"http://sozluk.gov.tr/gts?ara={kelime}")
    kelime_anlamlari = r.json()
    gonder = []

    if "error" in kelime_anlamlari:
        mesaj = f"{kelime} Kelimesi Bulunamadı"
        
        gonder.append(False)
        gonder.append(mesaj)
        return gonder

    else:

        mesaj = f"**Kelime:** `{kelime}`\n"
        anlamlar_liste = kelime_anlamlari[0]["anlamlarListe"]
        cogul_mu = kelime_anlamlari[0]["cogul_mu"]
        ozel_mi = kelime_anlamlari[0]["ozel_mi"]
        
        anlamlar = []
        sadece_anlam = []
        for i in anlamlar_liste:
            if "ozelliklerListe" in i:
                anlamlar.append(
                    f'(__{i["ozelliklerListe"][0]["tam_adi"]}__) `{i["anlam"]}`'
                )
                sadece_anlam.append(i["anlam"])
            else:
                anlamlar.append(
                    f'`{i["anlam"]}`'
                )
                sadece_anlam.append(i["anlam"])

        if int(cogul_mu): cogul_mu = "✅"
        else: cogul_mu = "❌"
        if int(ozel_mi): ozel_mi = "✅"
        else: ozel_mi = "❌"

        mesaj += f"\n**Çoğul:** {cogul_mu}\n**Özel:** {ozel_mi}\n\n**Anlamlar:**\n "

        sayac = 0
        for i in anlamlar:
            sayac += 1
            mesaj += f"**{sayac}-** {i} \n"

        gonder.append(True)
        gonder.append(mesaj)
        gonder.append(sadece_anlam)

        return gonder

@TDK_Bot.on_message(Filters.command(["start"]))
def start(client, message):
    client.send_message(
        message.chat.id,
        "Botu kullanmak için lütfen /yardim alınız.",
        reply_to_message_id=message.message_id,
    )

@TDK_Bot.on_message(Filters.command(["yardim"]))
def yardim(client, message):
    mesaj = """
Botu 2 yöntemle kullanabilirsiniz;

1-) __/tdk [kelime]__

2-) Inline modda @tdk_iibot'tan sonra kelime yazarak. Inline moda geçmek için mesajın altındaki butonu kullanın. 

"""
    
    client.send_message(
        message.chat.id,
        mesaj,
        reply_to_message_id=message.message_id,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="İnline Moda Geç",
                        switch_inline_query_current_chat="görmek"
                    )
                ]
            ]
        )
    )



@TDK_Bot.on_message(Filters.command(["tdk"]))
def tdk_komut(client, message):
    kelime = message.text[5:]
    if len(kelime) == 0:
        client.send_message(
            message.chat.id,
            "Lütfen /tdk komutundan sonra bir kelime giriniz.",
            reply_to_message_id=message.message_id,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="İnline Moda Geç",
                            switch_inline_query_current_chat="görmek"
                        )
                    ]
                ]
            )
        )

    else:
        fonk = tdk_fonk(kelime)
        if fonk[0] == False:
            client.send_message(
                message.chat.id,
                f"`{kelime}` isminde bir kelime bulunamadı.",
                reply_to_message_id=message.message_id,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="İnline Moda Geç",
                                switch_inline_query_current_chat="görmek"
                            )
                        ]
                    ]
                )
            )

        elif fonk[0] == True:
            client.send_message(
                message.chat.id,
                fonk[1],
                reply_to_message_id=message.message_id,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="İnline Moda Geç",
                                switch_inline_query_current_chat=kelime
                            )
                        ]
                    ]
                )
            )




@TDK_Bot.on_inline_query()
def inelene(client, i_q):
    kelime = i_q.query

    if len(kelime) == 0:
        client.answer_inline_query(
            i_q.id,
            results=[
                InlineQueryResultArticle(
                    "Lütfen Kelime Giriniz",
                    InputTextMessageContent("Lütfen kelime giriniz"),
                    thumb_url="https://i.imgur.com/2kVCU8Z.jpeg",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    text="İnline Moda Geç",
                                    switch_inline_query_current_chat=""
                                )
                            ]
                        ]
                    )
                )
            ]
        )
    
    else:
        fonk = tdk_fonk(kelime)

        if fonk[0] == False:
            client.answer_inline_query(
                i_q.id,
                results=[
                    InlineQueryResultArticle(
                        fonk[1],
                        InputTextMessageContent("Kelime Bulunamadı."),
                        thumb_url="https://i.imgur.com/2kVCU8Z.jpeg",
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton(
                                        text="İnline Moda Geç",
                                        switch_inline_query_current_chat=""
                                    )
                                ]
                            ]
                        )
                    )
                ]
            )
    
        elif fonk[0]:
            client.answer_inline_query(
                i_q.id,
                results=[
                    InlineQueryResultArticle(
                        kelime,
                        InputTextMessageContent(fonk[1]),
                        description=fonk[2][0],
                        thumb_url="https://i.imgur.com/2kVCU8Z.jpeg",
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton(
                                        text="İnline Moda Geç",
                                        switch_inline_query_current_chat=""
                                    )
                                ]
                            ]
                        )
                    )
                ]
            )


TDK_Bot.run()
