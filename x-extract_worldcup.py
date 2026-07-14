"""
Extrai do PDF do calendário da Copa do Mundo 2026:
- Times que estão jogando
- Fase (todas: Round 1, Round of 32, Quarter Finals, etc.)
- Horário de início do jogo
- Local (estádio)

Usa a biblioteca natural-pdf: https://jsoma.github.io/natural-pdf/
Não usa regex — só métodos simples de string.
"""

import csv
from datetime import datetime

import natural_pdf as npdf

PDF_PATH = "worldcupcalendar.pdf"   # ajuste o caminho se necessário

ROTULOS = {"Starts on", "Ends on", "Location"}
LIXO_OCR = {"JUN", "JUL", ""}                 # badges de mês que sobram no meio do texto
FASES_VALIDAS = {"Round", "of", "Quarter", "Semi", "Finals"}


def parece_horario(palavra):
    """Considera 'HH:MM:SS', mesmo colado em outro texto tipo '(America/...'."""
    pedaco = palavra.split("(")[0][-8:]
    return pedaco.count(":") == 2, pedaco


def extrair_horario(texto):
    """De 'Thu Jun 11 2026 15:00:00 (America/New_York)' pega só '3:00 PM'."""
    for palavra in texto.split():
        eh_horario, pedaco = parece_horario(palavra)
        if eh_horario:
            try:
                hora = datetime.strptime(pedaco, "%H:%M:%S")
            except ValueError:
                continue
            return hora.strftime("%I:%M %p").lstrip("0")
    return None


def achar_horario_inicio(linhas, i):
    """Às vezes o OCR lê a data ANTES do rótulo 'Starts on', então olhamos
    uma pequena janela para os dois lados, parando ao chegar em outro rótulo."""
    inicio = max(0, i - 1)
    fim = min(len(linhas), i + 4)
    for j in range(inicio, fim):
        if j != i and linhas[j] in ROTULOS:
            break
        horario = extrair_horario(linhas[j])
        if horario:
            return horario
    return None


def limpar_fase(texto):
    """Mantém só palavras da fase (ex: 'Round 1', 'Quarter Finals'),
    parando no primeiro texto estranho que o OCR tenha colado junto."""
    palavras = []
    for p in texto.split():
        p = p.strip(".,()")
        eh_numero = p.isascii() and p.isdigit()   # evita "③", "⑦" etc.
        if p in FASES_VALIDAS or eh_numero:
            palavras.append(p)
        elif palavras:
            break
        if len(palavras) >= 3:   # nenhuma fase real tem mais de 3 palavras
            break
    return " ".join(palavras)


def eh_lixo(texto):
    return (
        texto in LIXO_OCR
        or texto in ROTULOS
        or texto.isdigit()
        or "FIFA World Cup 2026" in texto
    )


def achar_local(linhas, i):
    """Procura o rótulo 'Location' perto do card. O valor normalmente vem
    depois, mas o OCR às vezes inverte a ordem — testamos os dois lados."""
    for j in range(i + 2, min(i + 12, len(linhas) - 1)):
        if linhas[j] != "Location":
            continue
        depois = linhas[j + 1].strip()
        antes = linhas[j - 1].strip()
        if not eh_lixo(depois):
            return depois
        if not eh_lixo(antes):
            return antes
        return None
    return None


def parse_card(linhas, i):
    """A partir do índice `i` onde linhas[i] == 'Starts on', monta um jogo."""

    # Título: normalmente é a linha anterior; às vezes quebra em duas linhas
    titulo = linhas[i - 1]
    if "FIFA World Cup 2026" not in titulo:
        titulo = f"{linhas[i - 2]} {linhas[i - 1]}"

    confronto, _, fase = titulo.partition("FIFA World Cup 2026")
    confronto = confronto.replace(" - ", "").strip()
    fase = limpar_fase(fase)

    horario = achar_horario_inicio(linhas, i)
    local = achar_local(linhas, i)

    return confronto, fase, horario, local


def extract_games(pdf_path):
    pdf = npdf.PDF(pdf_path)
    jogos = []

    for page in pdf.pages:
        page.apply_ocr()  # o PDF é composto de imagens, então precisa de OCR
        linhas = [t.extract_text().strip() for t in page.find_all("text")]

        for i, linha in enumerate(linhas):
            if linha == "Starts on":
                confronto, fase, horario, local = parse_card(linhas, i)
                jogos.append({
                    "confronto": confronto,
                    "fase": fase,
                    "horario_inicio": horario,
                    "local": local,
                })

    pdf.close()
    return jogos


if __name__ == "__main__":
    jogos = extract_games(PDF_PATH)

    print(f"{len(jogos)} jogos encontrados\n")
    for j in jogos:
        print(f"{j['confronto']:35s} | {j['fase']:15s} | {str(j['horario_inicio']):>8} | {j['local']}")

    with open("jogos.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["confronto", "fase", "horario_inicio", "local"])
        writer.writeheader()
        writer.writerows(jogos)
    print("\nSalvo em jogos.csv")
