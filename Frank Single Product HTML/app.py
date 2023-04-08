
from flask import Flask
import sys
sys.path.append('/Users/aka_nubi/Desktop/411Pro/pro/myApp')

from sites.routes import bp
app = Flask(__name__)

app.register_blueprint(bp)


@app.route('/')
def index():
    return 'index'


if (__name__ == '__main__'):
    app.run(port=5000, debug=True)

