# 🤖 JARVIS - DASHBOARD DE METAS + TELEGRAM
!pip install gspread google-auth pandas requests > /dev/null 2>&1

import gspread
from google.colab import auth
from google.auth import default
import pandas as pd
from datetime import datetime
import requests
import time

# ========== CONFIGURAÇÕES ==========
TELEGRAM_BOT_TOKEN = "8256513003:AAHfpBECsu1qaJiKhdE5i3eFWB32AOI_ZDY"
TELEGRAM_CHAT_ID = "8428346208"
GOOGLE_SHEETS_URL = "https://docs.google.com/spreadsheets/d/1UbtJqX8UH5COB2R0F62Hiiw9m7PEbgVrG0O6Q49hXvQ/edit?usp=sharing"

# ========== CONEXÃO GOOGLE SHEETS ==========
auth.authenticate_user()
creds, _ = default()
gc = gspread.authorize(creds)

# ========== FUNÇÕES TELEGRAM ==========
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
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Erro ao enviar para Telegram: {e}")
        return False

def mensagem_jarvis():
    """Mensagem de boas-vindas do Jarvis"""
    mensagem = """
🤖 <b>Olá, Deivid! Eu sou seu Jarvis!</b> 😎

Estou pronto para gerenciar suas metas e acompanhar seu progresso.

<b>Comandos disponíveis:</b>
• 📊 Dashboard completo de metas
• ⚠️ Alertas de prazos
• 📈 Relatórios de progresso

Vamos conquistar seus objetivos! 🚀
    """
    return enviar_telegram(mensagem)

# ========== FUNÇÕES METAS ==========
def ler_metas():
    """Lê metas do Google Sheets"""
    try:
        planilha = gc.open_by_url(GOOGLE_SHEETS_URL)
        worksheet = planilha.sheet1
        todos_dados = worksheet.get_all_values()

        if len(todos_dados) < 2:
            return []

        metas = []
        for i in range(1, len(todos_dados)):
            linha = todos_dados[i]
            if any(linha):
                meta = {
                    'Meta': linha[0] if len(linha) > 0 else '',
                    'Categoria': linha[1] if len(linha) > 1 else '',
                    'Progresso (%)': linha[2] if len(linha) > 2 else '0',
                    'Status': linha[3] if len(linha) > 3 else '',
                    'Data Limite': linha[4] if len(linha) > 4 else ''
                }
                metas.append(meta)

        return metas
    except Exception as e:
        print(f"❌ Erro ao ler planilha: {e}")
        return []

def criar_mensagem_metas(metas):
    """Cria mensagem formatada para Telegram"""
    if not metas:
        return "📭 <b>Nenhuma meta encontrada</b>\n\nAdicione metas na planilha do Google Sheets!"

    # Cabeçalho
    mensagem = f"🚀 <b>DASHBOARD DE METAS - JARVIS</b>\n"
    mensagem += f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}\n"
    mensagem += "─" * 35 + "\n\n"

    # Metas individuais
    for i, meta in enumerate(metas, 1):
        nome = meta.get('Meta', 'Sem nome').strip()
        categoria = meta.get('Categoria', 'Geral').strip()

        # Progresso
        progresso_str = str(meta.get('Progresso (%)', '0')).strip()
        try:
            progresso = int(progresso_str) if progresso_str.isdigit() else 0
        except:
            progresso = 0

        status = meta.get('Status', 'Não definido').strip()
        data_limite = meta.get('Data Limite', '').strip()

        # Emojis e formatação
        if progresso == 100:
            emoji = '✅'
            status_emoji = '🎉'
        elif progresso > 0:
            emoji = '🔄'
            status_emoji = '📈'
        else:
            emoji = '🚀'
            status_emoji = '⏳'

        barra = "█" * (progresso // 5) + "░" * (20 - (progresso // 5))

        mensagem += f"{emoji} <b>{nome}</b>\n"
        mensagem += f"   📁 {categoria}\n"
        mensagem += f"   {barra} <b>{progresso}%</b>\n"
        mensagem += f"   {status_emoji} {status}\n"
        if data_limite:
            mensagem += f"   📅 {data_limite}\n"
        mensagem += "\n"

    # Estatísticas
    total_metas = len(metas)
    progressos = []
    for meta in metas:
        progresso_str = str(meta.get('Progresso (%)', '0')).strip()
        try:
            progressos.append(int(progresso_str) if progresso_str.isdigit() else 0)
        except:
            progressos.append(0)

    progresso_medio = sum(progressos) / len(progressos) if metas else 0
    concluidas = len([p for p in progressos if p == 100])
    andamento = len([p for p in progressos if 0 < p < 100])

    mensagem += "📊 <b>RESUMO GERAL</b>\n"
    mensagem += f"✅ Concluídas: {concluidas}\n"
    mensagem += f"🔄 Em andamento: {andamento}\n"
    mensagem += f"🚀 A iniciar: {total_metas - concluidas - andamento}\n"
    mensagem += f"📋 Total: {total_metas} metas\n"
    mensagem += f"🎯 <b>Progresso geral: {progresso_medio:.1f}%</b>\n\n"

    # Mensagem motivacional
    if progresso_medio >= 80:
        mensagem += "🎉 <b>Excelente progresso! Continue assim!</b>"
    elif progresso_medio >= 50:
        mensagem += "💪 <b>Bom trabalho! Vamos manter o ritmo!</b>"
    else:
        mensagem += "🚀 <b>Vamos começar! Cada passo importa!</b>"

    return mensagem

# ========== FUNÇÕES PRINCIPAIS ==========
def enviar_dashboard_completo():
    """Envia dashboard completo para Telegram"""
    print("📤 Enviando dashboard para Telegram...")
    metas = ler_metas()
    mensagem = criar_mensagem_metas(metas)

    if enviar_telegram(mensagem):
        print("✅ Dashboard enviado com sucesso!")
        return True
    else:
        print("❌ Erro ao enviar dashboard")
        return False

def enviar_alertas_metas():
    """Envia alertas de metas próximas do prazo"""
    print("🔔 Verificando alertas...")
    metas = ler_metas()

    alertas = []
    for meta in metas:
        data_limite = meta.get('Data Limite', '').strip()
        progresso_str = str(meta.get('Progresso (%)', '0')).strip()
        progresso = int(progresso_str) if progresso_str.isdigit() else 0
        nome = meta.get('Meta', '').strip()

        # Alertas para metas com progresso baixo
        if progresso < 30:
            alertas.append(f"⚠️ <b>{nome}</b> - {progresso}% (Progresso baixo)")
        elif progresso < 70 and data_limite:
            alertas.append(f"📅 <b>{nome}</b> - {progresso}% (Prazo: {data_limite})")

    if alertas:
        mensagem_alerta = "🚨 <b>ALERTAS DO JARVIS</b>\n\n" + "\n".join(alertas)
        if enviar_telegram(mensagem_alerta):
            print("✅ Alertas enviados!")
        else:
            print("❌ Erro ao enviar alertas")
    else:
        print("✅ Nenhum alerta necessário")

def relatorio_diario():
    """Envia relatório diário automático"""
    print("📊 Preparando relatório diário...")

    # Mensagem do Jarvis
    mensagem_jarvis()
    time.sleep(2)

    # Dashboard completo
    enviar_dashboard_completo()
    time.sleep(2)

    # Alertas
    enviar_alertas_metas()

# ========== EXECUÇÃO ==========
print("🤖 JARVIS - SISTEMA DE METAS ATIVADO")
print("=" * 50)
print(f"👤 Usuário: Deivid")
print(f"🔗 Google Sheets: Conectado")
print(f"🤖 Telegram: Pronto")
print("=" * 50)

# Menu interativo
print("\n🎯 COMANDOS DISPONÍVEIS:")
print("1. relatorio_diario() - Relatório completo (Jarvis + Dashboard + Alertas)")
print("2. mensagem_jarvis() - Apenas mensagem do Jarvis")
print("3. enviar_dashboard_completo() - Apenas dashboard de metas")
print("4. enviar_alertas_metas() - Apenas alertas")

print(f"\n🚀 Executando relatório completo...")
relatorio_diario()

print(f"\n💡 <b>Jarvis está online!</b> Use os comandos acima a qualquer momento!")
