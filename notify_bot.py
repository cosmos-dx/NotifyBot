from telegram import Update, Bot
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, CommandHandler, ConversationHandler
import logging


BOT_TOKEN = 'YOUR_BOT_TOKEN'

TARGET_TEXT = range(1)

class NotifyBot:
    """
    /start : for activating user_id
    /name : target text
    /delete : reset text
    """
    def __init__(self):
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.YOUR_USER_ID = 0
        self.targetText = ""
        self.updater = Updater(BOT_TOKEN, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.__bootloading()
        

    def __bootloading(self):
        """
            Required Loading CommandHandler('YOUR_COMMAND', 'BINDED_FUNCTION')
        """
        self.dispatcher.add_handler(CommandHandler('start', self.start))
        self.dispatcher.add_handler(CommandHandler('delete', self.delete))
        self.dispatcher.add_handler(CommandHandler('seek', self.seek))
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('name', self.name)],
            states={
                TARGET_TEXT: [MessageHandler(Filters.text & ~Filters.command, self.set_target_text)]
            },
            fallbacks=[]
        )

        self.dispatcher.add_handler(conv_handler)
        self.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, self.monitor_group))
        
        self.updater.start_polling()
        self.updater.idle()

    def start(self, update: Update, context: CallbackContext):
        self.YOUR_USER_ID = update.message.chat_id
        update.message.reply_text(f'Hello! Your chat ID is {self.YOUR_USER_ID}')
        self.logger.info(f'Chat ID: {self.YOUR_USER_ID}')

    def name(self, update: Update, context: CallbackContext):
        update.message.reply_text('Please provide the target text:')
        return TARGET_TEXT

    def set_target_text(self, update: Update, context: CallbackContext):
        self.targetText = update.message.text.lower().replace(" ", "")
        update.message.reply_text(f'Target text set to: {self.targetText}')
        return ConversationHandler.END

    def delete(self, update: Update, context: CallbackContext):
        self.targetText = 'delete'
        update.message.reply_text('Target text is reset')

    def seek(self, update: Update, context: CallbackContext):
        update.message.reply_text(f'Your Target text is {self.targetText}')

    def monitor_group(self, update: Update, context: CallbackContext):
        message_text = update.message.text.lower().replace(" ", "")
        if self.targetText in message_text:
            try:
                bot: Bot = context.bot
                bot.send_message(chat_id=self.YOUR_USER_ID, text=f"Alert! Mentioned in group: {update.message.text}")
            except Exception as e:
                self.logger.error(f"Error sending message: {e}")

if __name__ == '__main__':
    NotifyBot()

