from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from func.utils import session, get_ids_with_os, get_ids_my_os

import json

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    id = update.effective_chat.id
    
    try:
        await context.bot.delete_message(chat_id=id, message_id=update.message.id)
    except:
        ...

    try:
        await context.bot.delete_message(chat_id=id, message_id=session(id, "", 7, False, True))
    except:
        ...

    # Caso não tenha um perfil então só aparece para cadastrar.
    if session(id, "", 0, False, True) == "not found":
        MENU = [[InlineKeyboardButton("Cadastrar", callback_data=json.dumps({"call": "cadastrando"}))]]
        await context.bot.send_message(chat_id=id, text="Você é novo por aqui? Então você precisa primeiro criar seu perfil.", reply_markup=InlineKeyboardMarkup(MENU))

    # Caso não tinha finalizado ainda o cadastro.
    elif session(id, "", 3, False, True) != 3:    
        MENU = [[InlineKeyboardButton("Cadastrar", callback_data=json.dumps({"call": "cadastrando"}))]]
        await context.bot.send_message(chat_id=id, text="Oh, vi que você iniciou um cadastro, mas não finalizou, será preciso recomeçar ele, clique em cadastrar para continuar.", reply_markup=InlineKeyboardMarkup(MENU))
        
    # Mostrando filas disponiveis.
    else:
        if session(id, "", 6, False, True) == 0 and session(id, "", 4, False, True) != 2:
            if session(id, "", 8, False, True) == 'noc':
                count = len(get_ids_with_os())
                MENU = [[InlineKeyboardButton(f"Atendimentos Abertos ({count})", callback_data=json.dumps({"call": "list_atendimentos"}))]]
            else:
                count = len(get_ids_my_os(id))
                MENU = [[InlineKeyboardButton("NOC", callback_data=json.dumps({"call": "entrando_noc"}))], [InlineKeyboardButton(f"Meus Atendimentos ({count})", callback_data=json.dumps({"call": "list_meus_atendimentos"}))]]                
            mes = await context.bot.send_message(chat_id=id, text="Selecione :", reply_markup=InlineKeyboardMarkup(MENU))
            session(id, mes.id, 7, True, False)
