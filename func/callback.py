from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

from func.utils import create_session, session, ordem, get_ids_with_os, get_ids_my_os
from func.command import menu

import json

async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):    
    query = json.loads(update.callback_query.data)
    id = update.effective_chat.id

    # Avisa que precisa se cadastrar antes de utilizar.
    if query["call"] == 'cadastrando':
        create_session(id)
        await context.bot.delete_message(chat_id=id, message_id=update.callback_query.message.id)
        mes = await context.bot.send_message(chat_id=id, text="Vamos começar então, primeiro digite seu nome e sobrenome:")
        session(id, mes.id, 7, True, False)
        return

    # Caso esteja conversando com alguém ele não deixa utilizar nenhum botão.
    if session(id, "", 6, False, True) != 0:
        return    
    
    # Entrar na fila
    if query["call"] == 'entrando_noc':
        try:
            await context.bot.delete_message(chat_id=id, message_id=update.callback_query.message.id)
            await context.bot.delete_message(chat_id=id, message_id=session(id, "", 7, False, True))
        except:
            ...

        mes = await context.bot.send_message(chat_id=id, text="Você precisa me informar algumas informações para agilizarmos um pouco\\.\n\n*Qual seria a OS?*", parse_mode="MarkdownV2")
        session(id, mes.id, 7, True, False)
        session(id, 1, 4, True, False)
        return

    # Cancelar fila
    if query["call"] == 'cancelar_os':
        if ordem(query['os'], "", 3, False, True) != 0:
            return

        ordem(query['os'], 3, 3, True, False)        
        session(id, 0, 4, True, False)
        await context.bot.send_message(chat_id=id, text="*OS cancelada\\.*", parse_mode="MarkdownV2")
        await menu(update, context)
        return

    # Iniciar atendimento
    if query["call"] == 'atendimento':
        if ordem(query['os'], "", 3, False, True) == 3:
            await context.bot.send_message(chat_id=id, text=f'_OS foi cancelada pelo tecnico\\._', parse_mode="MarkdownV2")
            return
        
        if ordem(query['os'], "", 3, False, True) != 0:
            await context.bot.send_message(chat_id=id, text=f'_OS já foi atendida\\._', parse_mode="MarkdownV2")
            return
        
        tecid = ordem(query['os'], "", 1, False, True)
        name_tec = session(tecid, "", 1, False, True)
        name = session(id, "", 1, False, True)
        
        ordem(query['os'], 1, 3, True, False)
        ordem(query['os'], id, 2, True, False)
        session(tecid, query['os'], 6, True, False)
        session(id, query['os'], 6, True, False)
        session(tecid, 3, 4, True, False)
        session(id, 3, 4, True, False)
        
        message = f"*Atendimento com tecnico {name_tec}, iniciado*"
        await context.bot.send_message(chat_id=id, text=message, parse_mode="MarkdownV2")
        await context.bot.send_message(chat_id=id, text=f'*{name}*\\:\nOlá\\! Meu nome é *{name}*\\, sou do setor NOC\\.\nComo posso ajudá\\-lo referente a OS {query["os"]}\\? ', parse_mode="MarkdownV2")
        await context.bot.send_message(chat_id=tecid, text=f'*{name}*\\:\nOlá\\! Meu nome é *{name}*\\, sou do setor NOC\\.\nComo posso ajudá\\-lo referente a OS {query["os"]}\\? ', parse_mode="MarkdownV2")
        return

    # Listar todos atendimentos abertos.
    if query["call"] == 'list_atendimentos':
        atendimentos = get_ids_with_os()
        await context.bot.delete_message(chat_id=id, message_id=update.callback_query.message.id)

        for i in atendimentos:
            idsTec = ordem(i, "", 1, False, True)
            name = session(idsTec, "", 1, False, True)
            phone = session(idsTec, "", 2, False, True)
            
            MENU = [[InlineKeyboardButton("Atender", callback_data=json.dumps({"call": "atendimento", "os": i}))]]
            await context.bot.send_message(chat_id=id, text=f"*Atendimento*\nOS: *{i}*\nTecnico: *{name}*\nTelefone: *{phone}*", parse_mode="MarkdownV2", reply_markup=InlineKeyboardMarkup(MENU))
            
        await menu(update, context)

    # Listar todos atendimentos do usuario.
    if query["call"] == 'list_meus_atendimentos':
        atendimentos = get_ids_my_os(id)
        await context.bot.delete_message(chat_id=id, message_id=update.callback_query.message.id)
        
        for i in atendimentos:
            idsTec = ordem(i, "", 1, False, True)
            process = ordem(i, "", 3, False, True)
            name = session(idsTec, "", 1, False, True)
            phone = session(idsTec, "", 2, False, True)

            if process == 0:
                MENU = [[InlineKeyboardButton("Cancelar", callback_data=json.dumps({"call": "cancelar_os", "os": i}))]]
            else:
                MENU = [[]]
                
            await context.bot.send_message(chat_id=id, text=f"*Atendimento*\nOS: *{i}*\nTecnico: *{name}*\nTelefone: *{phone}*", parse_mode="MarkdownV2", reply_markup=InlineKeyboardMarkup(MENU))
            
        await menu(update, context)
