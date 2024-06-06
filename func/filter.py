from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from func.utils import session, get_ids_with_noc_sector, create_ordem, ordem
from func.command import menu

import json

async def filter_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    id = update.effective_chat.id
    text = update.message.text
    os = session(id, "", 6, False, True)
    
    # Delete Menssagem caso esteja esperando ser atendido.
    if session(id, "", 0, False, True) == 'not found':
        await context.bot.delete_message(chat_id=id, message_id=update.message.id)
        return
    
    # Deleta todas mensagems que não são necessarias para o atendimento.
    if session(id, "", 4, False, True) == 2 or session(id, "", 4, False, True) == 0:
        if session(id, "", 4, False, True) != 0 and session(id, "", 4, False, True) != 1:
            await context.bot.delete_message(chat_id=id, message_id=update.message.id)
            return
    
    # Comandos
    if text.lower() == "/sair":
        os = session(id, "", 6, False, True)
        if os == 0:
            return
        
        await context.bot.delete_message(chat_id=id, message_id=update.message.id)
        tecid = ordem(os, "", 1, False, True)
        ateid = ordem(os, "", 2, False, True)
        
        ordem(os, 2, 3, True, False)
        
        session(tecid, 0, 6, True, False)
        session(ateid, 0, 6, True, False)

        await context.bot.send_message( chat_id=tecid, text="Conversa finalizada.")
        await context.bot.send_message( chat_id=ateid, text="Conversa finalizada.")

    # Durante DM
    elif os != 0:
        otherid = ordem(os, "", 1, False, True)
        if otherid == id:
            otherid = ordem(os, "", 2, False, True)
            
        name = session(id, "", 1, False, True)
        escaped_text = text.replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("]", "\\]").replace("(", "\\(").replace(")", "\\)").replace("~", "\\~").replace("`", "\\`").replace(">", "\\>").replace("#", "\\#").replace("+", "\\+").replace("-", "\\-").replace("=", "\\=").replace("|", "\\|").replace("{", "\\{").replace("}", "\\}").replace(".", "\\.").replace("!", "\\!")

        await context.bot.send_message(chat_id=otherid, text=f'*{name}*\\:\n{escaped_text}', parse_mode="MarkdownV2")

    # Cadastro
    elif session(id, "", 3, False, True) == 1:
        session(id, text, 1, True, False)
        session(id, 2, 3, True, False)
        await context.bot.delete_message(chat_id=id, message_id=update.message.id)
        await context.bot.delete_message(chat_id=id, message_id=session(id, "", 7, False, True))
        mes = await context.bot.send_message( chat_id=id, text="Tudo certo, agora digite seu número de telefone.")
        session(id, mes.id, 7, True, False)
    elif session(id, "", 3, False, True) == 2:
        session(id, 3, 3, True, False)
        session(id, text, 2, True, False)
        await context.bot.delete_message(chat_id=id, message_id=update.message.id)
        await context.bot.delete_message(chat_id=id, message_id=session(id, "", 7, False, True))
        mes = await context.bot.send_message( chat_id=id, text="Agora temos suas informações salvas e você pode acessar as funções de fila.")
        session(id, mes.id, 7, True, False)
        await menu(update, context)
        
    # Solicitando Atendimento
    elif session(id, "", 4, False, True) == 1:
        await context.bot.delete_message(chat_id=id, message_id=session(id, "", 7, False, True))
        await context.bot.delete_message(chat_id=id, message_id=update.message.id)
        session(id, 2, 4, True, False)
        MENU = [
            [InlineKeyboardButton("Cancelar", callback_data=json.dumps({"call": "cancelar_os", "os": text}))],
        ]
        await context.bot.send_message(chat_id=id, text=f"*Atendimento para a OS {text} gerado*\n\n_Em breve alguém irá te atender_", parse_mode="MarkdownV2", reply_markup=InlineKeyboardMarkup(MENU))
        create_ordem(text, id)
        ids_noc = get_ids_with_noc_sector()
        for i in ids_noc:
            name = session(id, "", 1, False, True)
            phone = session(id, "", 2, False, True)
            MENU = [[InlineKeyboardButton("Atender", callback_data=json.dumps({"call": "atendimento", "os": text}))],]
            await context.bot.send_message(chat_id=i, text=f"*Novo Atendimento*\nOS: *{text}*\nTecnico: *{name}*\nTelefone: *{phone}*", parse_mode="MarkdownV2", reply_markup=InlineKeyboardMarkup(MENU))
