import requests
import schedule
import time
from datetime import datetime
from flask import Flask

# ========== CONFIGURAÇÕES ==========
TELEGRAM_BOT_TOKEN = "8256513003:AAHfpBECsu1qaJiKhdE5i3eFWB32AOI_ZDY"
TELEGRAM_CHAT_ID = "8428346208"

app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Jarvis está rodando! " + datetime.now().strftime('%d/%m/%Y %H:%M')

def enviar_telegram(mensagem):
    """Envia mensagem para o Telegram"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': mensagem,
            'parse_mode': 'HTML'
        }
        response = requests.post(url, json=payload)
        print(f"✅ Mensagem enviada")
        return True
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def relatorio_jarvis():
    """Função principal do Jarvis"""
    mensagem = f"""
🤖 <b>Olá, Deivid! Jarvis aqui!</b> 😎
📊 <b>Relatório Automático de Metas</b>
📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}

🎯 <b>Status das Metas:</b>
• ✅ Aprender Python - 75%
• 🔄 Promoção no Trabalho - 50%

📈 <b>Progresso: 62.5%</b>

💪 <b>Vamos com tudo hoje!</b> 🚀
    """
    
    return enviar_telegram(mensagem)

def agendar_tarefas():
    """Agenda as execuções automáticas"""
    schedule.every().day.at("09:00").do(relatorio_jarvis)
    schedule.every().day.at("18:00").do(relatorio_jarvis)
    
    print("⏰ Agendamentos: 09:00 e 18:00")
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    print("🚀 Jarvis Iniciado!")
    
    # Iniciar agendador em thread separada
    import threading
    thread = threading.Thread(target=agendar_tarefas)
    thread.daemon = True
    thread.start()
    
    # Manter o Flask rodando na porta 10000
    app.run(host='0.0.0.0', port=10000)
