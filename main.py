from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, ConversationHandler, filters, CallbackContext, CallbackQueryHandler
import random
from Controlers.ControlesComu import OBTENER_GRUPOS, PRUEBA_OTRA_VEZ, ListaComunidad, grupos_conversation_handler


TOKEN = "7442684904:AAF0JtIzYB4zoff6B-STm9ndvUGmkvq3OPM"



application = ApplicationBuilder().token(TOKEN).build()
application.add_handler( CommandHandler( "start", ListaComunidad.say_hello) )
application.add_handler( CommandHandler( "respo", ListaComunidad.respo) )
application.add_handler( CommandHandler( "miracolo", ListaComunidad.miracolo) )
application.add_handler( CommandHandler( "ver_hermanos", ListaComunidad.see_bros) )
# application.add_handler( CallbackQueryHandler(ListaComunidad.boton_callback_inicio) )
application.add_handler( CallbackQueryHandler(ListaComunidad.boton_callback) )


application.add_handler(grupos_conversation_handler)

application.run_polling(allowed_updates=Update.ALL_TYPES)



