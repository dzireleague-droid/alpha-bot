from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Configuración - CAMBIA ESTOS VALORES
TELEGRAM_TOKEN = "8268551860:AAHBTQxh_Ig3FZuvf3SzNG-PaVMgxTT7s-Q"
TELEGRAM_CHAT_ID = "-1003216167786"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Obtener datos de TradingView
        data = request.json
        if not data:
            app.logger.error("No JSON data received")
            return "No JSON data", 400
        
        message = data.get('text', '')
        if not message:
            app.logger.error("No text in message")
            return "No text in message", 400
        
        app.logger.info(f"Received message: {message}")
        
        # Enviar a Telegram
        telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        
        response = requests.post(telegram_url, json=payload, timeout=10)
        
        if response.status_code == 200:
            app.logger.info("Message sent to Telegram successfully")
            return "OK", 200
        else:
            error_msg = f"Telegram error: {response.status_code} - {response.text}"
            app.logger.error(error_msg)
            return error_msg, 500
            
    except Exception as e:
        error_msg = f"Server error: {str(e)}"
        app.logger.error(error_msg)
        return error_msg, 500

@app.route('/test', methods=['GET'])
def test():
    """Endpoint de prueba"""
    return {
        "status": "running",
        "service": "TradingView-Telegram Bridge",
        "telegram_configured": bool(TELEGRAM_TOKEN and TELEGRAM_CHAT_ID)
    }, 200

@app.route('/send-test', methods=['GET'])
def send_test():
    """Enviar mensaje de prueba a Telegram"""
    try:
        telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": "✅ Servidor funcionando correctamente",
            "parse_mode": "HTML"
        }
        
        response = requests.post(telegram_url, json=payload, timeout=5)
        return {"sent": response.status_code == 200}, 200
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
