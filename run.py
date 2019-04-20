#!flask/bin/python
from app import app
app.run(debug = True, host='0.0.0.0', port=5000, ssl_context=('../rsa/server.crt','../rsa/server.key'))