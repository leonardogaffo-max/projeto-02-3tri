import string
import gradio as gr

# ==============================================================================
# DICIONÁRIOS E MAPEAMENTOS
# ==============================================================================

DICIONARIO_MINUSCULO = "qwertyuiopasdfghjklzxcvbnm"
ALFABETO_MINUSCULO   = "abcdefghijklmnopqrstuvwxyz"

DICIONARIO_MAIUSCULO = "QWERTYUIOPASDFGHJKLZXCVBNM"
ALFABETO_MAIUSCULO   = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

DICIONARIO_NUMEROS   = "9876543210"
ALFABETO_NUMEROS     = "0123456789"

# ==============================================================================
# FUNÇÕES DE LÓGICA
# ==============================================================================

def codifica(senha: str) -> str:
    """Criptografa a senha substituindo letras e números."""
    if not senha:
        return ""
    senha_criptografada = ""
    for letra in senha:
        if "a" <= letra <= "z":
            posicao = ord(letra) - ord("a")
            senha_criptografada += DICIONARIO_MINUSCULO[posicao]
        elif "A" <= letra <= "Z":
            posicao = ord(letra) - ord("A")
            senha_criptografada += DICIONARIO_MAIUSCULO[posicao]
        elif "0" <= letra <= "9":
            posicao = ord(letra) - ord("0")
            senha_criptografada += DICIONARIO_NUMEROS[posicao]
        else:
            senha_criptografada += letra
    return senha_criptografada


def decodifica(senha_criptografada: str) -> str:
    """Restaura a senha original a partir da senha criptografada."""
    if not senha_criptografada:
        return ""
    senha_original = ""
    for letra in senha_criptografada:
        if letra in DICIONARIO_MINUSCULO:
            posicao = DICIONARIO_MINUSCULO.find(letra)
            senha_original += ALFABETO_MINUSCULO[posicao]
        elif letra in DICIONARIO_MAIUSCULO:
            posicao = DICIONARIO_MAIUSCULO.find(letra)
            senha_original += ALFABETO_MAIUSCULO[posicao]
        elif letra in DICIONARIO_NUMEROS:
            posicao = DICIONARIO_NUMEROS.find(letra)
            senha_original += ALFABETO_NUMEROS[posicao]
        else:
            senha_original += letra
    return senha_original


def calcula_hash(senha: str) -> str:
    """Calcula o valor hash acumulado baseado na tabela ASCII."""
    if not senha:
        return "0"
    valor_hash = sum(ord(c) for c in senha)
    return f"{valor_hash} (Processo Irreversível)"


def avaliar_forca_senha(senha: str) -> str:
    """Avalia a complexidade da senha fornecida."""
    if not senha:
        return "Insira uma senha para avaliar."
    
    tem_minuscula = any(c.islower() for c in senha)
    tem_maiuscula = any(c.isupper() for c in senha)
    tem_numero    = any(c.isdigit() for c in senha)
    tem_especial  = any(c in string.punctuation for c in senha)
    tamanho       = len(senha)

    pontos = sum([tem_minuscula, tem_maiuscula, tem_numero, tem_especial])

    if tamanho >= 8 and pontos >= 3:
        return "🟢 FORTE (Alta complexidade e bom tamanho)"
    elif tamanho >= 6 and pontos >= 2:
        return "🟡 MÉDIA (Recomendável adicionar mais caracteres variados)"
    else:
        return "🔴 FRACA (Muito curta ou com baixa variedade de caracteres)"

# ==============================================================================
# INTERFACE GRÁFICA (GRADIO)
# ==============================================================================

with gr.Blocks(title="Sistema de Criptografia") as app:
    gr.Markdown("# 🔐 Sistema de Segurança e Criptografia")
    gr.Markdown("Projeto de estudos sobre algoritmos de criptografia e hashing.")

    with gr.Tab("Criptografar & Descriptografar"):
        with gr.Row():
            entrada_texto = gr.Textbox(label="Digite a Senha ou Texto", placeholder="Ex: Marcelo123!")
        
        with gr.Row():
            btn_codificar = gr.Button("🔒 Criptografar", variant="primary")
            btn_decodificar = gr.Button("🔓 Descriptografar")

        saida_cripto = gr.Textbox(label="Resultado da Operação")

        btn_codificar.click(fn=codifica, inputs=entrada_texto, outputs=saida_cripto)
        btn_decodificar.click(fn=decodifica, inputs=entrada_texto, outputs=saida_cripto)

    with gr.Tab("Gerador de Hash"):
        entrada_hash = gr.Textbox(label="Digite a Senha", placeholder="Ex: olecram")
        btn_hash = gr.Button("⚡ Gerar Hash ASCII")
        saida_hash = gr.Textbox(label="Valor Hash Calculado")

        btn_hash.click(fn=calcula_hash, inputs=entrada_hash, outputs=saida_hash)

    with gr.Tab("Analisador de Força"):
        entrada_forca = gr.Textbox(label="Digite a Senha para Testar", type="password")
        btn_forca = gr.Button("📊 Analisar Segurança")
        saida_forca = gr.Textbox(label="Diagnóstico de Segurança")

        btn_forca.click(fn=avaliar_forca_senha, inputs=entrada_forca, outputs=saida_forca)

# Executa a aplicação
if __name__ == "__main__":
    app.launch()