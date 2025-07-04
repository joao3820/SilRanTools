import urllib.request
import smtplib

def get_title_summary(category, results=10):
    url = 'https://export.arxiv.org/api/query?search_query=cat:' + category + '&max_results=' + str(results) + '&sortBy=submittedDate'
    data = urllib.request.urlopen(url)
    resposta = data.read().decode('utf-8')

    start = 0
    resultados = []

    for _ in range(results):
        resposta = resposta[start:]
        resultados.append(resposta[resposta.find("<title>") + 7:resposta.find("<summary>") - 13])
        resultados.append(resposta[resposta.find("<summary>") + 11:resposta.find("</summary>") - 1])
        start = resposta.find("</summary>") + 1
    return resultados


def keywords(resultado):
    have_keywords = []
    for i in range(0, len(resultado), 2):
        # originalmente, quando criei isto em fevereiro de 2022, a lista usada era ["magnet", "spin", "ferro", "phase", "semiconductor"], pois estava numa área de magnetismo
        for item in [" "]:
            if item in (resultado[i].lower() or resultado[i + 1].lower()):
                have_keywords.append(i)
                break
    return have_keywords[:3]  # limitar somente a três artigos


def keywords_print(resultado):
    have_keywords = keywords(resultado)
    nova_lista = []
    for i in have_keywords:
        nova_lista.append(resultado[i].replace('\n ', ''))
        nova_lista.append(resultado[i + 1].replace('\n', ' '))
    return nova_lista


def enviar_email(email, password, meu_email):
    """Enviar email com alguns papers de hoje. Os inputs são text strings normais"""

    # definir o servidor e correr umas funções aleatórias necessárias; depois, dar login (foi necessário ir ao gmail e criar "app password", depois de ativar 2 factor authentication)
    server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(email, password)

    # Começar a escrever a mensagem
    msg = "Subject: Some Relevant ArXiv Articles\n\nHere's some articles from ArXiv from today (sent using a python script that I made). For more, check out http://arxiv.org/\n\n"

    # r1 = get_title_summary(category="cond-mat.mes-hall")
    # lista_mes_hall = keywords_print(r1)
    # r2 = get_title_summary(category="cond-mat.mtrl-sci")
    # lista_mtrl_sci = keywords_print(r2)

    r1 = get_title_summary(category="physics.app-ph")
    lista = keywords_print(r1)
    r2 = get_title_summary(category="physics.optics")
    lista += keywords_print(r2)
    r3 = get_title_summary(category="eess.IV")
    lista += keywords_print(r3)
    r4 = get_title_summary(category="eess.SP")
    lista += keywords_print(r4)
    r5 = get_title_summary(category="eess.SY")
    lista += keywords_print(r5)

    # Remover itens repetidos
    nova_lista = []
    for i in range(0, len(lista), 2):
        if lista[i] not in nova_lista:
            nova_lista.append(lista[i])
            nova_lista.append(lista[i + 1])

    for item in nova_lista:
        msg += item + "\n\n"

    server.sendmail(email, meu_email, msg)
    server.quit()


# enviar_email(inserir aqui os parametros)
