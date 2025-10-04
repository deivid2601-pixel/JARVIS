import requests
import schedule
import time
from datetime import datetime

# ========== CONFIGURAÇÕES ==========
TELEGRAM_BOT_TOKEN = "8256513003:AAHfpBECsu1qaJiKhdE5i3eFWB32AOI_ZDY"
TELEGRAM_CHAT_ID = "8428346208"

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
• 💰 Economizar - 30%
• 📚 Estudar - 90%
• ❤️ Saúde - 60%

📈 <b>Progresso Geral: 61.0%</b>

💪 <b>Continue evoluindo! Cada passo importa!</b> 🚀

⚡ <i>Relatório automático do sistema</i>
    """
    
    sucesso = enviar_telegram(mensagem)
    if sucesso:
        print("🎉 Relatório enviado com sucesso!")
    else:
        print("❌ Falha ao enviar relatório")
    
    return sucesso

def agendar_tarefas():
    """Agenda as execuções automáticas"""
    # Todo dia às 9:00 AM
    schedule.every().day.at("09:00").do(relatorio_jarvis)
    
    print("⏰ Agendamento configurado: 09:00 todo dia")
    
    # Manter o script rodando
    while True:
        schedule.run_pending()
        time.sleep(60)  # Verificar a cada minuto

if __name__ == "__main__":
    print("🚀 Jarvis Iniciado!")
    print("⚡ Testando envio de mensagem...")
    relatorio_jarvis()  # Executar imediatamente para teste
    print("🔧 Iniciando agendador...")
    agendar_tarefas()   # Manter rodando para agendamentos
