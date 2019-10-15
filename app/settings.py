import os

import dotenv
dotenv.load_dotenv()


HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT'))
