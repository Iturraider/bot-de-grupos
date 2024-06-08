from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, ConversationHandler, filters, CallbackContext, CallbackQueryHandler
import random



TOKEN = "7442684904:AAF0JtIzYB4zoff6B-STm9ndvUGmkvq3OPM"

OBTENER_GRUPOS, PRUEBA_OTRA_VEZ = range(2)


async def say_bay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Adiós")


def crear_grupos(numero_grupos, lista_nombres):
        """
        Función que crea grupos a partir de una lista de nombres.
        Args:
            numero_grupos: El número de grupos a crear.
            lista_nombres: Una lista de nombres.
        Returns:
            Una lista de listas, donde cada sublista representa un grupo.
        """
        random.shuffle(lista_nombres)  # Mezclamos los nombres aleatoriamente
        grupos = []
        for i in range(numero_grupos):
            grupos.append([])
        # Distribuimos los nombres en los grupos
        for i, nombre in enumerate(lista_nombres):
            grupo_index = i % numero_grupos
            grupos[grupo_index].append(nombre)
        return grupos








async def say_hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
        
        keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(text="Quiero hacer 3 grupos", callback_data=3)],
        [InlineKeyboardButton(text="Quiero hacer 4 grupos", callback_data=4)],
        [InlineKeyboardButton(text="Quiero hacer 5 grupos", callback_data=5)]
    ])

        await update.message.reply_text("Hola, bienvenido al bot para crear grupos de la comunidad")
        await update.message.reply_text("¿Cuantos grupos quieres Hacer?", reply_markup=keyboard)

async def boton_callback(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    numero = update.callback_query.data
    message = ""
    lista = ["Jose y Laura", "Andrés y Salut", "Javi y Salut", "Luján y Sergio"," Enan y Pilar", "David y Sandra", "Marcos y Maria", "Ana María y Salva", "Joan", "Cristina", "Maria"]

    mensaje = f"Vale, voy a hacer {numero} grupos de comunidad"
    await update.callback_query.message.reply_text(mensaje)

    grupos_creados = crear_grupos(int(numero), lista)
                
    for i, grupo in enumerate(grupos_creados):
        message += f"Grupo {i+1}: {', '.join(grupo)}\n"
    await update.callback_query.message.reply_text(message)
    # await update.callback_query.message.reply_text(numero)


async def cancel_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Has dejado la conversación")
        return ConversationHandler.END
async def numero_grupos(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("¿Cuantos grupos quieres hacer?")
        return OBTENER_GRUPOS
    
async def obtener_grupos(update: Update, context: ContextTypes.DEFAULT_TYPE):
        context.user_data["groups"] = update.message.text

        try:
            numero = int(context.user_data['groups'])
        
            mensaje = ""
            message = ""
            lista = ["Jose y Laura", "Andrés y Salut", "Javi y Salut", "Luján y Sergio"," Enan y Pilar", "David y Sandra", "Marcos y Maria", "Ana María y Salva", "Joan", "Cristina", "Maria"]
            
            if numero >= 0:
                mensaje = f"Vale, voy a hacer {numero} grupos de comunidad"
                await update.message.reply_text(mensaje)

                grupos_creados = crear_grupos(numero, lista)
                
                for i, grupo in enumerate(grupos_creados):
                    message += f"Grupo {i+1}: {', '.join(grupo)}\n"
                await update.message.reply_text(message)
        except ValueError:
            await update.message.reply_text("Por favor, ingresa un número válido.")
            return 

# Suggested code may be subject to a license. Learn more: ~LicenseLog:910095168.
        return ConversationHandler.END
    

application = ApplicationBuilder().token(TOKEN).build()
application.add_handler( CommandHandler( "start", say_hello) )
application.add_handler( CommandHandler( "ciao", say_by) )
application.add_handler( CallbackQueryHandler(boton_callback) )



grupos_conversation_handler = ConversationHandler(
        entry_points=[ CommandHandler("crear", numero_grupos)],
        states={
            OBTENER_GRUPOS: [MessageHandler(filters.TEXT & ~filters.COMMAND, obtener_grupos)],
# Suggested code may be subject to a license. Learn more: ~LicenseLog:3306488876.
            PRUEBA_OTRA_VEZ: [MessageHandler(filters.TEXT & ~filters.COMMAND, numero_grupos)]

        },
        fallbacks=[ CommandHandler("cancel", cancel_conversation)]
    )

application.add_handler(grupos_conversation_handler)

application.run_polling(allowed_updates=Update.ALL_TYPES)



