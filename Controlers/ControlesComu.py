from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, ConversationHandler, filters, CallbackContext, CallbackQueryHandler
from Controlers.Funciones import *
import math
import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def decir_bobadas():
    mensaje = "valla bobada"
    return mensaje


OBTENER_GRUPOS, PRUEBA_OTRA_VEZ = range(2)

keyboard = InlineKeyboardMarkup([
# Suggested code may be subject to a license. Learn more: ~LicenseLog:2565311830.
        [InlineKeyboardButton(text="Consultar Lista de Hermanos", callback_data= "ver_hermanos"),InlineKeyboardButton(text="¿Quién es el responsable?", callback_data="respo")],
        [InlineKeyboardButton(text="Crear grupos de comunidad", callback_data="hacer_grupos"), InlineKeyboardButton(text="Miracolo" , callback_data="miracolo")],
        [InlineKeyboardButton(text="Bobada", callback_data="bobada"), InlineKeyboardButton(text="Salir", callback_data="salir")]
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
        await update.message.reply_text(mensaje, reply_markup=keyboard3) 
        return mensaje


    
    @staticmethod
    async def boton_callback(update: Update, context: CallbackContext):
        await update.callback_query.answer()
        
        if update.callback_query.data == "hacer_grupos":
            await update.callback_query.edit_message_text("¿Cuantos grupos te gustaría Hacer?", reply_markup=keyboard2)
            return
        elif update.callback_query.data == "ver_hermanos":
            lista_keys = list(diccionario.keys())  # Obtener una lista de las claves
            mensaje = "\n".join(lista_keys)  # Unir las claves en un solo string con saltos de línea
            await update.callback_query.message.reply_text("Esta es la Lista de Hermanos: \n \n" +  mensaje, reply_markup=keyboard3)
            # await update.callback_query.message.reply_text(mensaje, reply_markup=keyboard3)
            return
        elif update.callback_query.data == "atras":
            # await update.callback_query.answer("ListaComunidad.say_hello")
            await update.callback_query.edit_message_text("¿Que te gustaría hacer?", reply_markup=keyboard)
            return
        elif update.callback_query.data == "respo":
            await update.callback_query.message.reply_voice(voice=open("RoboCorte.mp3", "rb"), reply_markup=keyboard3)
            return
        elif update.callback_query.data == "miracolo":
            await update.callback_query.message.reply_sticker(sticker=open("Miracolo.webp", "rb"), reply_markup=keyboard3)
            return
        elif update.callback_query.data == "salir":
# Suggested code may be subject to a license. Learn more: ~LicenseLog:3769876663.
            await update.callback_query.edit_message_text("Vale! Hasta luego, si querés volver a empezar, escribe /start")
            return
        elif update.callback_query.data == "delete":
            await update.callback_query.message.delete()
            return
        elif update.callback_query.data == "bobada":
            await update.callback_query.message.reply_text(decir_bobadas(), reply_markup=keyboard3)
            return
        else:
            numero = update.callback_query.data
            message = ""
            mensaje = f"Vale, voy a hacer {numero} grupos de comunidad"
            # await update.callback_query.message.reply_text(mensaje)

            grupos = crear_grupos(int(numero), diccionario)

            for i, grupo in enumerate(grupos):
                message += f"Grupo {i+1}: "
                message += ", ".join(grupo) + "\n"
            await update.callback_query.message.reply_text(mensaje + "\n\n" + message, reply_markup= keyboard3)
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

async def conv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola, ¿En que puedo ayudarte?")
    return OBTENER_GRUPOS


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
                    
            return await update.message.reply_text(message)
        
    except ValueError:
        await update.message.reply_text("Por favor, ingresa un número válido.")
        return 
        
    

        


async def cancel_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Conversación cancelada.")
    return ConversationHandler.END

        

 

# pruebaConversacion = ConversationHandler(
#     entry_points=[CommandHandler("conv", conv)],
#     states={
#         OBTENER_GRUPOS: [MessageHandler(filters.TEXT & ~filters.COMMAND, obtener_grupos)]
#     },
#     fallbacks=[ CommandHandler("cancel", cancel_conversation)]
# )

async def inicio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [["Boy", "Girl", "Other"]]

    await update.message.reply_text(
        "Hi! My name is Professor Bot. I will hold a conversation with you. "
        "Send /cancel to stop talking to me.\n\n"
        "Are you a boy or a girl?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Boy or Girl?"
        ),
    )
    return GENDER

async def gender(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    context.user_data["gender"] = update.message.text
    logger.info("Gender of %s: %s", user.first_name, update.message.text)
    await update.message.reply_text(
        "I see! Please send me a photo of yourself, "
        "so I know what you look like, or send /skip if you don't want to.",
        reply_markup=ReplyKeyboardRemove(),
    )

    return PHOTO

async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the photo and asks for a location."""
    user = update.message.from_user
    photo_file = await update.message.photo[-1].get_file()
    await photo_file.download_to_drive("user_photo.jpg")
    logger.info("Photo of %s: %s", user.first_name, "user_photo.jpg")
    await update.message.reply_text(
        "Gorgeous! Now, send me your location please, or send /skip if you don't want to."
    )

    return LOCATION


async def skip_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Skips the photo and asks for a location."""
    user = update.message.from_user
    logger.info("User %s did not send a photo.", user.first_name)
    await update.message.reply_text(
        "I bet you look great! Now, send me your location please, or send /skip."
    )

    return LOCATION


async def location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the location and asks for some info about the user."""
    user = update.message.from_user
    user_location = update.message.location
    logger.info(
        "Location of %s: %f / %f", user.first_name, user_location.latitude, user_location.longitude
    )
    await update.message.reply_text(
        "Maybe I can visit you sometime! At last, tell me something about yourself."
    )

    return BIO


async def skip_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Skips the location and asks for info about the user."""
    user = update.message.from_user
    logger.info("User %s did not send a location.", user.first_name)
    await update.message.reply_text(
        "You seem a bit paranoid! At last, tell me something about yourself."
    )

    return BIO


async def bio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the info about the user and ends the conversation."""
    user = update.message.from_user
    logger.info("Bio of %s: %s", user.first_name, update.message.text)
    await update.message.reply_text("Thank you! I hope we can talk again some day.")

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

GENDER, PHOTO, LOCATION, BIO = range(4)

conv_handler = ConversationHandler(
        entry_points=[CommandHandler("inicio", inicio)],
        states={
            GENDER: [MessageHandler(filters.Regex("^(Boy|Girl|Other)$"), gender)],
            PHOTO: [MessageHandler(filters.PHOTO, photo), CommandHandler("skip", skip_photo)],
            LOCATION: [
                MessageHandler(filters.LOCATION, location),
                CommandHandler("skip", skip_location),
            ],
            BIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, bio)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    