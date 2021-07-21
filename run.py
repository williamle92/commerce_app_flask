from app import app, db
from app.models import User, Item, Cart, Info
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Item': Item, 'Cart': Cart, 'Info': Info}