#Importando as bibliotecas
import cv2
import numpy as np
from time import sleep

# Função para capturar o centro do objeto (neste caso, os veiculos)
def centro_objeto (posicaox, posicaoy, largura, altura):
    x1 = int(largura // 2)
    y1 = int(altura // 2)
    posicaox = coordenadax + x1
    posicaoy = coordenaday + y1
    return posicaox, posicaoy

# Função para atualizar o contador
def atualizar_contagem(detectar):
    global objeto
    for (coordenadax, coordenaday) in detectar:
        if (linha_referencia + desvio) > coordenaday > (linha_referencia - desvio):
            objeto += 1
            cv2.line(frame1, (25, linha_referencia), (1200, linha_referencia), (255, 0, 0), 3)
            detectar.remove((coordenadax, coordenaday))
            print(f"Número de veículos: {objeto}")

# Função para exibir as informacoes
def exibir_informacoes(frame1, dilatada):
    text = f'Numero de veiculos: {objeto}'
    cv2.putText(frame1, text, (450, 70), cv2.FONT_ITALIC, 1, (0, 255, 0), 3)
    cv2.imshow("Camera", frame1)
    cv2.imshow("Detectar", dilatada)

# variaveis de ajuste conforme a necessidade do video/camera
objeto = 0
linha_referencia = 500
desvio = 5
largura_min = 60
altura_min = 60
delay = 60
detectar = []

#Realiza a captura do video
captura = cv2.VideoCapture(r'file:///C:/Users/souza/Desktop/Projetos/projetoUPXIV/videos.mp4/video_veiculos.mp4')
if not captura.isOpened():
    print("Erro ao tentar abrir o vídeo!")
    exit()

#Subtrai o fundo da imagem
subtrai = cv2.bgsegm.createBackgroundSubtractorMOG()

while True:
    ret, frame1 = captura.read()
    temporizador = float(1 / delay)
    sleep(temporizador)
    cinza = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    limpa = cv2.GaussianBlur(cinza, (3, 3), 5)
    img_sub = subtrai.apply(limpa)
    dilataimg = cv2.dilate(img_sub, np.ones((5, 5)))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    dilatada = cv2.morphologyEx(dilataimg, cv2.MORPH_CLOSE, kernel)

    #verifica o contorno da imagem 
    contorno, img = cv2.findContours(dilatada, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.line(frame1, (25, linha_referencia), (1200, linha_referencia), (255, 127, 0), 3)
    for (i, c) in enumerate(contorno):
        (coordenadax, coordenaday, width, high) = cv2.boundingRect(c)
        validar_contorno = (width >= largura_min) and (high >= altura_min)
        if not validar_contorno:
            continue

        cv2.rectangle(frame1, (coordenadax, coordenaday), (coordenadax + width, coordenaday + high), (0, 255, 0), 2)
        centro = centro_objeto(coordenadax, coordenaday, width, high)
        detectar.append(centro)
        cv2.circle(frame1, centro, 4, (0, 0, 255), -1)

    atualizar_contagem(detectar)
    exibir_informacoes(frame1, dilatada)

    #Para sair apertar a letra "Q"
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    #Fecha as janelas e libera os recursos
cv2.destroyAllWindows()
captura.release()
