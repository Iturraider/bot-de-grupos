from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, ConversationHandler, filters, CallbackContext, CallbackQueryHandler
from Controlers.Funciones import crear_grupos
import math

OBTENER_GRUPOS, PRUEBA_OTRA_VEZ, VER_BROS = range(3)


diccionario = diccionario = {"Jose y Laura": 2, "Andrés y Salut": 2, "Javi y Salut": 2, "Luján y Sergio": 2, 
               "Enan y Pilar": 2, "David y Sandra": 2, "Marcos y Maria": 2, "Ana María y Salva": 2, 
               "Joan": 1, "Cristina": 1, "Maria": 1}
lista = ""

class ListaComunidad:

    @staticmethod
    async def see_bros(update: Update, context: ContextTypes.DEFAULT_TYPE):
        lista_keys = list(diccionario.keys())  # Obtener una lista de las claves
        mensaje = "\n".join(lista_keys)  # Unir las claves en un solo string con saltos de línea
        await update.message.reply_text("Esta es la Lista de Hermanos:")
        await update.message.reply_text(mensaje) 
        return mensaje


    @staticmethod
    async def obtener_grupos(update: Update, context: ContextTypes.DEFAULT_TYPE):
        context.user_data["groups"] = update.message.text

        try:
            numero = int(context.user_data['groups'])
        
            mensaje = ""
            message = ""
            
            if numero >= 0:
                mensaje = f"Vale, voy a hacer {numero} grupos de comunidad"
                await update.message.reply_text(mensaje)

                grupos_creados = crear_grupos(numero, diccionario)
                
                for i, grupo in enumerate(grupos_creados):
                    message += f"Grupo {i+1}: "
                    message += ", ".join(grupo) + "\n"
                await update.message.reply_text(message)
        except ValueError:
            await update.message.reply_text("Por favor, ingresa un número válido.")
            return 

# Suggested code may be subject to a license. Learn more: ~LicenseLog:910095168.
        return ConversationHandler.END

    @staticmethod
    async def cancel_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Has dejado la conversación")
        return ConversationHandler.END

    # @staticmethod
    # async def boton_callback_inicio(update: Update, context: CallbackContext):
    #     await update.callback_query.answer()
        
    #     if update.callback_query.data == "see_bros":
    #         await update.callback_query.message.reply_text("Esta es la Lista de Hermanos:")
    #         return VER_BROS
    #     elif update.callback_query.data == "hacer_grupos":
    #         await update.callback_query.message.reply_text("¿Cuantos grupos te gustaría Hacer?")
    #         return OBTENER_GRUPOS

    @staticmethod
    async def boton_callback(update: Update, context: CallbackContext):
        await update.callback_query.answer()
        
        numero = update.callback_query.data
        message = ""
        mensaje = f"Vale, voy a hacer {numero} grupos de comunidad"
        await update.callback_query.message.reply_text(mensaje)

        grupos = crear_grupos(int(numero), diccionario)

        for i, grupo in enumerate(grupos):
            message += f"Grupo {i+1}: "
            message += ", ".join(grupo) + "\n"
        await update.callback_query.message.reply_text(message)
# Suggested code may be subject to a license. Learn more: ~LicenseLog:1919231081.
        return 
        
    @staticmethod
    async def say_hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
        # keyboard = InlineKeyboardMarkup([
        # [InlineKeyboardButton(text="Consultar Lista de Hermanos", callback_data="see_bros")],
        # [InlineKeyboardButton(text="Crear grupos de comunidad", callback_data="hacer_grupos")]
        # ])

        await update.message.reply_text("Hola, bienvenido al bot para crear grupos de la comunidad")
        # await update.message.reply_text("¿Que te gustaría hacer?", reply_markup=keyboard)
        return

    @staticmethod
    async def numero_grupos(update: Update, context: ContextTypes.DEFAULT_TYPE):
        
        keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(text="Quiero hacer 2 grupos", callback_data=2),InlineKeyboardButton(text="Quiero hacer 3 grupos", callback_data=3)],
        [InlineKeyboardButton(text="Quiero hacer 4 grupos", callback_data=4),InlineKeyboardButton(text="Quiero hacer 5 grupos", callback_data=5)]
        ])

        await update.message.reply_text("¿Cuantos grupos te gustaría Hacer?", reply_markup=keyboard)
        return ConversationHandler.END

grupos_conversation_handler = ConversationHandler(
        entry_points=[ CommandHandler("crear", ListaComunidad.numero_grupos)],
        states={
            OBTENER_GRUPOS: [MessageHandler(filters.TEXT & ~filters.COMMAND, ListaComunidad.obtener_grupos)],
# Suggested code may be subject to a license. Learn more: ~LicenseLog:3306488876.
            PRUEBA_OTRA_VEZ: [MessageHandler(filters.TEXT & ~filters.COMMAND, ListaComunidad.numero_grupos)],
            # VER_BROS: [MessageHandler(filters.TEXT & ~filters.COMMAND, ListaComunidad.see_bros)]

        },
        fallbacks=[ CommandHandler("cancel", ListaComunidad.cancel_conversation)]
    )    