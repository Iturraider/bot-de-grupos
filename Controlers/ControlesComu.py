from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, ConversationHandler, filters, CallbackContext, CallbackQueryHandler
from Controlers.Funciones import crear_grupos
import math

OBTENER_GRUPOS, PRUEBA_OTRA_VEZ, VER_BROS = range(3)

keyboard = InlineKeyboardMarkup([
# Suggested code may be subject to a license. Learn more: ~LicenseLog:2565311830.
        [InlineKeyboardButton(text="Consultar Lista de Hermanos", callback_data="see_bros"),InlineKeyboardButton(text="¿Quiés es el responsable?", callback_data="respo")],
        [InlineKeyboardButton(text="Crear grupos de comunidad", callback_data="hacer_grupos"), InlineKeyboardButton(text="Miracolo", callback_data="miracolo")],
        [InlineKeyboardButton(text="Salir", callback_data="salir")]
        ])

keyboard2 = InlineKeyboardMarkup([
        [InlineKeyboardButton(text="Quiero hacer 2 grupos", callback_data=2),InlineKeyboardButton(text="Quiero hacer 3 grupos", callback_data=3)],
        [InlineKeyboardButton(text="Quiero hacer 4 grupos", callback_data=4),InlineKeyboardButton(text="Quiero hacer 5 grupos", callback_data=5)],
        [InlineKeyboardButton(text= "Volver", callback_data="atras")]
        ])
keyboard3 = InlineKeyboardMarkup([
        [InlineKeyboardButton(text="Eliminar", callback_data="delete")]
        ])

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
            return ConversationHandler.PRUEBA_OTRA_VEZ
        
        return ConversationHandler.END

    @staticmethod
    async def boton_callback(update: Update, context: CallbackContext):
        await update.callback_query.answer()
        
        if update.callback_query.data == "hacer_grupos":
            await update.callback_query.edit_message_text("¿Cuantos grupos te gustaría Hacer?", reply_markup=keyboard2)
            return
        elif update.callback_query.data == "see_bros":
            lista_keys = list(diccionario.keys())  # Obtener una lista de las claves
            mensaje = "\n".join(lista_keys)  # Unir las claves en un solo string con saltos de línea
            await update.callback_query.message.reply_text("Esta es la Lista de Hermanos:")
            await update.callback_query.message.reply_text(mensaje)
            return
        elif update.callback_query.data == "atras":
            await update.callback_query.edit_message_text("¿Que te gustaría hacer?", reply_markup=keyboard)
            return
        elif update.callback_query.data == "respo":
            await update.callback_query.message.reply_voice(voice=open("RoboCorte.mp3", "rb"), reply_markup=keyboard3)
            return
        elif update.callback_query.data == "miracolo":
            await update.callback_query.message.reply_sticker(sticker=open("Miracolo.webp", "rb"), reply_markup=keyboard3)
            return
        elif update.callback_query.data == "salir":
            await update.callback_query.message.reply_text("Vale! Hasta luego")
            await update.callback_query.message.delete()
            return
        elif update.callback_query.data == "delete":
            await update.callback_query.message.delete()
            return
        else:
            numero = update.callback_query.data
            message = ""
            mensaje = f"Vale, voy a hacer {numero} grupos de comunidad"
            await update.callback_query.message.reply_text(mensaje)

            grupos = crear_grupos(int(numero), diccionario)

            for i, grupo in enumerate(grupos):
                message += f"Grupo {i+1}: "
                message += ", ".join(grupo) + "\n"
            await update.callback_query.message.reply_text(message)
            return 
        
    @staticmethod
    async def say_hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
                
        await update.message.reply_text("Hola, bienvenido al bot para crear grupos de la comunidad \n ¿Que te gustaría hacer?", reply_markup=keyboard)
        return


    @staticmethod
    async def respo(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_voice("RoboCorte.mp3", reply_markup=keyboard3)
        return
    @staticmethod
    async def miracolo(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_sticker("Miracolo.webp", reply_markup=keyboard3)
        return

 