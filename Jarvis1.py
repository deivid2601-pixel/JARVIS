import pandas as pd
import pywhatkit as kit
import time
import pyautogui
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# =============================================
# JARVIS DE VENDAS - ABA NOVA POR BLOCO
# =============================================

class JarvisVendasAbaNova:
    def __init__(self):
        self.ARQUIVO_PLANILHA = r"C:\Users\gameb\Downloads\MENSAGEM.xlsx"
        self.NUMERO_WHATSAPP = "+5531985984350"
        self.META_EQUIPE = 500000
        
    def carregar_dados_limpos(self):
        """Carrega e limpa os dados"""
        try:
            print("🧹 CARREGANDO DADOS...")
            df = pd.read_excel(self.ARQUIVO_PLANILHA)
            
            # Limpeza
            df = df.dropna(how='all')
            df = df[df['NOME'].notna() & (df['NOME'] != '')]
            df = df[df['META'].notna() & (df['META'] != '')]
            
            df['META'] = pd.to_numeric(df['META'], errors='coerce')
            df['LIQUIDO'] = pd.to_numeric(df['LIQUIDO'], errors='coerce')
            df = df[df['META'].notna()]
            df = df.fillna(0)
            
            print(f"✅ {len(df)} vendedores válidos")
            return df
            
        except Exception as e:
            print(f"❌ Erro: {e}")
            return None
    
    def calcular_metricas(self, df):
        """Calcula métricas"""
        try:
            metricas = {
                'total_vendedores': len(df),
                'meta_equipe': self.META_EQUIPE
            }
            
            metricas['vendas_totais'] = df['LIQUIDO'].sum()
            metricas['atingimento_equipe'] = (metricas['vendas_totais'] / self.META_EQUIPE) * 100
            
            df['ATINGIMENTO'] = (df['LIQUIDO'] / df['META']) * 100
            df['FALTANTE'] = df['META'] - df['LIQUIDO']
            
            metricas['atingimento_medio'] = df['ATINGIMENTO'].mean()
            metricas['melhor_vendedor'] = df.loc[df['LIQUIDO'].idxmax()]['NOME'] if not df.empty else "N/A"
            metricas['maior_atingimento'] = df['ATINGIMENTO'].max()
            
            metricas['acima_meta'] = len(df[df['LIQUIDO'] > df['META']])
            metricas['abaixo_meta'] = len(df[df['LIQUIDO'] < df['META']])
            
            metricas['df_completo'] = df
            
            return metricas
            
        except Exception as e:
            print(f"❌ Erro: {e}")
            return {}
    
    def criar_blocos(self, metricas):
        """Cria blocos para envio"""
        df = metricas['df_completo']
        
        # Bloco 1 - Resumo
        bloco1 = "🔥 *JARVIS PREMIUM - RELATÓRIO* 🔥\n\n"
        bloco1 += "🎯 RESUMO EXECUTIVO\n"
        bloco1 += "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
        bloco1 += f"📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n"
        bloco1 += f"👥 Vendedores: {metricas['total_vendedores']}\n"
        bloco1 += f"🎯 Meta Equipe: R$ {metricas['meta_equipe']:,.2f}\n"
        bloco1 += f"💰 Vendas Totais: R$ {metricas['vendas_totais']:,.2f}\n"
        bloco1 += f"📊 Atingimento: {metricas['atingimento_equipe']:.1f}%\n"
        
        if metricas['atingimento_equipe'] >= 100:
            bloco1 += "🎉 META ATINGIDA!\n"
        else:
            faltante = metricas['meta_equipe'] - metricas['vendas_totais']
            bloco1 += f"🎯 Faltam: R$ {faltante:,.2f}\n"
        
        # Bloco 2 - Performance
        bloco2 = "📊 PERFORMANCE DA EQUIPE\n"
        bloco2 += "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
        bloco2 += f"✅ Acima da Meta: {metricas['acima_meta']}\n"
        bloco2 += f"⚠️ Abaixo da Meta: {metricas['abaixo_meta']}\n"
        bloco2 += f"📈 Atingimento Médio: {metricas['atingimento_medio']:.1f}%\n"
        bloco2 += f"⭐ Melhor Performance: {metricas['melhor_vendedor']}\n"
        bloco2 += f"💎 Maior Atingimento: {metricas['maior_atingimento']:.1f}%\n"
        
        # Bloco 3 - Detalhes
        bloco3 = "📋 DETALHES POR VENDEDOR\n"
        bloco3 += "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
        
        for _, vendedor in df.iterrows():
            status = "✅ ACIMA" if vendedor['LIQUIDO'] >= vendedor['META'] else "⚠️ ABAIXO"
            
            bloco3 += f"👤 {vendedor['NOME']} ({status})\n"
            bloco3 += f"   🎯 Meta: R$ {vendedor['META']:,.2f}\n"
            bloco3 += f"   💰 Realizado: R$ {vendedor['LIQUIDO']:,.2f}\n"
            bloco3 += f"   📊 Atingimento: {vendedor['ATINGIMENTO']:.1f}%\n"
            
            if vendedor['FALTANTE'] > 0:
                bloco3 += f"   📉 Faltante: R$ {vendedor['FALTANTE']:,.2f}\n"
            else:
                bloco3 += f"   🎉 Excedente: R$ {abs(vendedor['FALTANTE']):,.2f}\n"
            bloco3 += "\n"
        
        return [bloco1, bloco2, bloco3]
    
    def enviar_bloco_individual(self, bloco, numero_bloco, total_blocos):
        """Abre uma NOVA aba, envia o bloco e FECHA"""
        try:
            print(f"📤 Abrindo aba {numero_bloco}/{total_blocos}...")
            
            # ABRE NOVA ABA
            kit.sendwhatmsg_instantly(
                phone_no=self.NUMERO_WHATSAPP,
                message=bloco,
                wait_time=15,
                tab_close=False  # Não fecha automaticamente
            )
            
            print("⏳ Aguardando carregamento...")
            time.sleep(10)
            
            # ENVIA MENSAGEM
            pyautogui.press('enter')
            print(f"✅ Bloco {numero_bloco} enviado!")
            time.sleep(3)
            
            # FECHA A ABA
            pyautogui.hotkey('ctrl', 'w')
            print("🗂️ Aba fechada!")
            time.sleep(2)
            
            return True
            
        except Exception as e:
            print(f"❌ Erro no bloco {numero_bloco}: {e}")
            return False
    
    def enviar_todos_blocos(self, blocos):
        """Envia cada bloco em uma ABA SEPARADA"""
        try:
            print("🚀 INICIANDO ENVIO COM ABAS SEPARADAS...")
            
            for i, bloco in enumerate(blocos, 1):
                print(f"\n🔄 Processando bloco {i}/{len(blocos)}...")
                
                sucesso = self.enviar_bloco_individual(bloco, i, len(blocos))
                
                if not sucesso:
                    print(f"💥 Falha no bloco {i}")
                    return False
                
                # Espera entre abas (exceto após o último)
                if i < len(blocos):
                    print("⏳ Aguardando antes da próxima aba...")
                    time.sleep(5)
            
            return True
            
        except Exception as e:
            print(f"❌ Erro geral: {e}")
            return False
    
    def executar_analise(self):
        """Executa análise completa"""
        print("=" * 60)
        print("🤖 JARVIS - ABA NOVA POR MENSAGEM")
        print("=" * 60)
        
        # Carregar dados
        df = self.carregar_dados_limpos()
        if df is None or df.empty:
            return False
        
        # Calcular métricas
        metricas = self.calcular_metricas(df)
        if not metricas:
            return False
        
        # Criar blocos
        blocos = self.criar_blocos(metricas)
        
        # Preview
        print("\n📄 VISUALIZAÇÃO DOS BLOCOS:")
        for i, bloco in enumerate(blocos, 1):
            print(f"\n--- BLOCO {i} ---")
            print(bloco)
        
        # Confirmação
        confirmacao = input(f"\n📲 Enviar {len(blocos)} blocos em ABAS SEPARADAS? (s/n): ")
        if confirmacao.lower() != 's':
            print("❌ Cancelado")
            return False
        
        # Envio
        print("\n🚀 Iniciando envio...")
        print("⚠️  Cada bloco abrirá e fechará uma nova aba")
        
        sucesso = self.enviar_todos_blocos(blocos)
        
        if sucesso:
            print(f"\n🎉 SUCESSO COMPLETO!")
            print(f"📱 {len(blocos)} blocos enviados para: {self.NUMERO_WHATSAPP}")
            print(f"⏰ {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        else:
            print("\n💥 Algum bloco falhou")
        
        return sucesso

# EXECUÇÃO
if __name__ == "__main__":
    jarvis = JarvisVendasAbaNova()
    
    try:
        jarvis.executar_analise()
    except Exception as e:
        print(f"💥 Erro: {e}")
    
    print("\n🤖 Finalizado!")