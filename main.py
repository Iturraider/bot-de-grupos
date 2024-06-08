from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, ConversationHandler, filters, CallbackContext, CallbackQueryHandler
import random



TOKEN = "7442684904:AAF0JtIzYB4zoff6B-STm9ndvUGmkvq3OPM"

OBTENER_GRUPOS, PRUEBA_OTRA_VEZ = range(2)

def crear_grupos(numero_grupos, diccionario_nombres):
    """
    Función que crea grupos a partir de un diccionario de nombres.
    Intenta que la suma de los valores de cada grupo sea lo más igual posible.
    Args:
        numero_grupos: El número de grupos a crear.
        diccionario_nombres: Un diccionario con nombres como claves y 1 o 2 como valores.
    Returns:
        Una lista de listas, donde cada sublista representa un grupo.
    """
    nombres = list(diccionario_nombres.keys())
    valores = list(diccionario_nombres.values())

    # Mezclamos los nombres aleatoriamente
    combinados = list(zip(nombres, valores))
    random.shuffle(combinados)
    nombres[:], valores[:] = zip(*combinados)

    grupos = [[] for _ in range(numero_grupos)]
    sumas_grupos = [0] * numero_grupos

    # Asignamos nombres a los grupos intentando equilibrar las sumas
    for nombre, valor in zip(nombres, valores):
        # Encontramos el grupo con la suma más baja
        indice_grupo = sumas_grupos.index(min(sumas_grupos))
        grupos[indice_grupo].append(nombre)
        sumas_grupos[indice_grupo] += valor

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
    mensaje = f"Vale, voy a hacer {numero} grupos de comunidad"
    await update.callback_query.message.reply_text(mensaje)

    diccionario = {"Jose y Laura": 2, "Andrés y Salut": 2, "Javi y Salut": 2, "Luján y Sergio": 2, 
               "Enan y Pilar": 2, "David y Sandra": 2, "Marcos y Maria": 2, "Ana María y Salva": 2, 
               "Joan": 1, "Cristina": 1, "Maria": 1}
    grupos = crear_grupos(int(numero), diccionario)

    for i, grupo in enumerate(grupos):
        message += f"Grupo {i+1}: {grupo} \n"
    await update.callback_query.message.reply_text(message)




async def say_by(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Adiós")

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
            diccionario = {"Jose y Laura": 2, "Andrés y Salut": 2, "Javi y Salut": 2, "Luján y Sergio": 2, 
               "Enan y Pilar": 2, "David y Sandra": 2, "Marcos y Maria": 2, "Ana María y Salva": 2, 
               "Joan": 1, "Cristina": 1, "Maria": 1}

            if numero >= 0:
                mensaje = f"Vale, voy a hacer {numero} grupos de comunidad"
                await update.message.reply_text(mensaje)

                grupos_creados = crear_grupos(numero, diccionario)
                
                for i, grupo in enumerate(grupos_creados):
                    message += f"Grupo {i+1}: {grupo} \n"
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



