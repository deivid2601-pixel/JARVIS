import requests
import schedule
import time
from datetime import datetime
from flask import Flask
import threading

# ========== CONFIGURAÇÕES ==========
TELEGRAM_BOT_TOKEN = "8256513003:AAHfpBECsu1qaJiKhdE5i3eFWB32AOI_ZDY"
TELEGRAM_CHAT_ID = "8428346208"

app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Jarvis está rodando! " + datetime.now().strftime('%d/%m/%Y %H:%M')

def enviar_telegram(mensagem):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': mensagem,
            'parse_mode': 'HTML'
        }
        response = requests.post(url, json=payload)
        print(f"✅ Mensagem enviada: {datetime.now().strftime('%H:%M')}")
        return True
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def relatorio_jarvis():
    mensagem = f"""
🤖 <b>Olá, Deivid! Jarvis aqui!</b> 😎
📊 <b>Relatório Horário</b>
📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}

🎯 <b>Metas em Andamento:</b>
• ✅ Aprender Python - 75%
• 🔄 Promoção no Trabalho - 50%
• 💰 Economizar - 30%
• 📚 Estudar - 90%
• ❤️ Saúde - 60%

📈 <b>Progresso Geral: 61.0%</b>

💡 <b>Lembrete:</b> Cada hora é uma oportunidade para avançar!

⚡ <i>Mensagem automática do sistema</i>
    """
    return enviar_telegram(mensagem)

def relatorio_motivacional():
    mensagens_motivacionais = [
        "💪 <b>Hora de dar o seu melhor!</b> Você está mais perto do que imagina!",
        "🚀 <b>Energia positiva!</b> Esta hora é sua para conquistar!",
        "🎯 <b>Foco total!</b> Cada minuto conta na sua jornada!",
        "🔥 <b>Vamos lá!</b> O sucesso é construído hora a hora!",
        "⭐ <b>Excelência!</b> Faça desta hora a mais produtiva!",
        "🌈 <b>Persistência!</b> Continue avançando, você consegue!"
    ]
    
    mensagem = f"""
🤖 <b>Jarvis Motivacional</b> ⭐
📅 {datetime.now().strftime('%H:%M')}

{mensagens_motivacionais[datetime.now().hour % len(mensagens_motivacionais)]}

🎯 <b>Metas atuais:</b>
• Python: 75% | Trabalho: 50%
• Estudos: 90% | Saúde: 60%

💫 <b>Vamos brilhar nesta hora!</b>
    """
    return enviar_telegram(mensagem)

def iniciar_agendador():
    # 📅 AGENDAMENTOS:
    
    # A CADA 1 HORA (relatório completo)
    schedule.every(1).hours.do(relatorio_jarvis)
    
    # A CADA 2 HORAS (mensagem motivacional)
    schedule.every(2).hours.do(relatorio_motivacional)
    
    # HORÁRIOS FIXOS DIÁRIOS
    schedule.every().day.at("08:00").do(relatorio_jarvis)  # Início do dia
    schedule.every().day.at("12:00").do(relatorio_motivacional)  # Meio-dia
    schedule.every().day.at("18:00").do(relatorio_jarvis)  # Final do dia
    schedule.every().day.at("22:00").do(relatorio_motivacional)  # Boa noite
    
    print("⏰ Agendamentos Configurados:")
    print("   📊 Relatório completo: A CADA 1 HORA")
    print("   💫 Motivacional: A CADA 2 HORAS") 
    print("   🌅 08:00 - Relatório matinal")
    print("   🕛 12:00 - Motivacional meio-dia")
    print("   🌇 18:00 - Relatório vespertino")
    print("   🌙 22:00 - Motivacional boa noite")
    
    # Executar imediatamente ao iniciar
    print("⚡ Executando primeiro relatório...")
    relatorio_jarvis()
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # Verificar a cada minuto

if __name__ == "__main__":
    print("🚀 Jarvis Horário Iniciado!")
    print(f"⏰ Iniciado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    
    # Iniciar agendador em thread separada
    agendador_thread = threading.Thread(target=iniciar_agendador)
    agendador_thread.daemon = True
    agendador_thread.start()
    
    # Manter Flask rodando (para Render Web Service)
    app.run(host='0.0.0.0', port=10000)
