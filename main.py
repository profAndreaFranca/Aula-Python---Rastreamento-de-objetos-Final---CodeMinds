import cv2
import math

#definindo as coordenadas do cesta
px = 530
py = 300

#criando listas para armazenar as coordenadas x e y do centro da bola
tx = [] 
ty = []

tracker = cv2.TrackerCSRT_create()

cap = cv2.VideoCapture("bb3.mp4")
success, frame = cap.read()

bbox = cv2.selectROI("tracking",frame,False)
tracker.init(frame, bbox)

def goal_track(img,bbox):
    x,y,w,h = int(bbox[0]),int(bbox[1]),int(bbox[2]),int(bbox[3]) #extrai as coordenadas do retângulo de rastreamento
    cx = int(x + w/2) #calcula a coordenada x do centro da bola
    cy = int(y + h/2) #calcula a coordenada y do centro da bola
    cv2.circle(img,(cx,cy),5,(0,255,0),3) #desenha um circulo no centro da bola
    
    cv2.circle(img,(px,py),2,(0,0,255),3) #desenha um circulo no centro da cesta
    
    dist = math.sqrt((cx-px)**2 + (cy-py)**2) #calcula a distância entre o centro da bola e o centro da cesta
    if dist < 20: #se a distância for menor que 20 pixels, considera que a bola entrou na cesta
        cv2.putText(img,"CESTA",(75,120),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,255),2) #exibe a mensagem "CESTA" na tela

    tx.append(cx) #adiciona a coordenada x do centro da bola na lista tx
    ty.append(cy) #adiciona a coordenada y do centro da bola na lista ty
    
    for i in range(len(tx)-1): #desenha uma linha conectando os pontos anteriores do centro da bola
        cv2.circle(img,(tx[i],ty[i]),2,(255,0,0),2) #desenha um circulo em cada ponto do centro da bola

def drawBox(img,bbox):
    x,y,w,h = int(bbox[0]),int(bbox[1]),int(bbox[2]),int(bbox[3])
    cv2.rectangle(img,(x,y),((x+w),(y+h)),(255,0,255),3,1)
    cv2.putText(img,"Rastreando",(75,90),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)

while True:
    check, img = cap.read()
    success, bbox = tracker.update(img)
    
    if success:
        drawBox(img,bbox)
        goal_track(img,bbox)
    else:
        cv2.putText(img,"Errou",(75,90),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
    
    cv2.imshow("resultado",img)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break


cap.release()
cv2.destroyALLwindows() 

#para casa

# 1- carregar outro vídeo e rastrear novos objetos nesse vídeo.
# 2 - Mudem a cor dos textos e a posição do textos na tela
# 3 - Mudar a cor da caixa de ratreamento (obs. testar as outras opções de desenho)
# 4 - Tente desenhar um círculo no centro da bola
