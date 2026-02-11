import pygame, sys, smtplib, ssl, random
import pandas as pd
import numpy as np
from pygame import *
from time import sleep
from email.message import EmailMessage
import cv2
import face_recognition
import os
import shutil

pygame.init()
pygame.mixer.init()
pygame.font.init()

# language
language = 1
music = 0

#Sound
startSound = pygame.mixer.Sound(r'sound\startgame.mp3')
mouseClick = pygame.mixer.Sound(r'sound\mouseclick.mp3')
mouseClick.set_volume(5)
ingameSound = pygame.mixer.Sound(r'sound\ingame.mp3')
item1 = pygame.mixer.Sound(r'sound\item1.mp3')
item2 = pygame.mixer.Sound(r'sound\item2.mp3')
item3 = pygame.mixer.Sound(r'sound\item3.mp3')
item4 = pygame.mixer.Sound(r'sound\item4.mp3')
item5 = pygame.mixer.Sound(r'sound\item5.mp3')
inraceSound = pygame.mixer.Sound(r'sound\inrace.mp3')
clapSound = pygame.mixer.Sound(r'sound\clap.mp3')

#Class for Player Information
class User():
    def __init__(Player, username, money, numItem, bet, countItem, numRace, lSite):
        Player.username = username
        Player.money = money
        Player.bet = bet
        Player.numItem = numItem
        Player.countItem = countItem
        Player.numRace = numRace
        Player.lSite = lSite

Player = User

#from this is the define for game statistics
FPS = 120
fpsClock = pygame.time.Clock()
numberKey = [ord('1'), ord('2'), ord('3'), ord('4'), ord('5'),
             ord('6'), ord('7'), ord('8'), ord('9'), ord('0')]
characterKey = [ord('A'), ord('B'), ord('C'), ord('D'), ord('E'),
                ord('F'), ord('G'), ord('H'), ord('I'), ord('J'),
                ord('K'), ord('L'), ord('M'), ord('N'), ord('O'),
                ord('P'), ord('Q'), ord('R'), ord('S'), ord('T'),
                ord('U'), ord('V'), ord('W'), ord('X'), ord('Y'),
                ord('a'), ord('b'), ord('c'), ord('d'), ord('e'),
                ord('f'), ord('g'), ord('h'), ord('i'), ord('j'),
                ord('k'), ord('l'), ord('m'), ord('n'), ord('o'),
                ord('p'), ord('q'), ord('r'), ord('s'), ord('t'),
                ord('u'), ord('v'), ord('w'), ord('x'), ord('y')]

# access to database
database = 'database.csv'
data = pd.read_csv(database)
quantity = int(data.iloc[0, 4]) #number of account at this time
site = None

# windows statics
WINDOWSIZE = (1080, 720)
pygame.display.set_caption('Lucky Race')
DISPLAYSURFACE = pygame.display.set_mode(WINDOWSIZE)
screen = pygame.display.set_mode(WINDOWSIZE)
icon = pygame.image.load(r'img\menu\Car_icon.jpg')
pygame.display.set_icon(icon)

#fonts
font = pygame.font.SysFont(None, 20, bold = True, italic = False) #set font for drawing
userNameFont = pygame.font.SysFont('Asap', 30, bold = True, italic = True)
mediumFont = pygame.font.SysFont('Asap', 16, bold = True, italic = False)
bigFont = pygame.font.SysFont('Asap', 20, bold = True, italic = False)
passwordFont = pygame.font.SysFont('Asap', 22, bold = True, italic = False)

# color
coinColor = (255, 215, 0)

# end define the game statistics

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
    return 1

def Save():
    global Player
    data.iloc[Player.lSite, 2] = int(Player.money)
    data.iloc[Player.lSite, 5] = int(Player.numItem)
    data.iloc[Player.lSite, 6] = int(Player.countItem)
    data.iloc[Player.lSite, 7] = int (Player.numRace)
    data.to_csv(database, index = False)

def saveBet(betmoney):
    global Player
    data.iloc[Player.lSite, Player.numRace + 8] = betmoney
    data.to_csv(database, index = False)

def saveGame(lSite, money):
    data.iloc[lSite, 2] = int(money)
    data.to_csv(database, index = False)

def buyItem(lSite):
    global Player
    data.iloc[lSite, 5] = Player.numItem
    data.iloc[lSite, 6] = Player.countItem
    data.to_csv(database, index = False)

def checkExistAccount1(username, password):
    global quantity
    exist = -1
    cSite = None
    for i in range(0, quantity):
        if data.iloc[i, 0] != None and data.iloc[i, 1] != None:
            if username == data.iloc[i, 0]:
                exist = 0
                cSite = i
                if password == data.iloc[i, 1]:
                    exist = 1
                else:
                    exist = 0
    return exist, cSite

def checkExistAccount(username, password, email):
    global quantity
    exist = -1
    cSite = None
    for i in range(0, quantity):
        if data.iloc[i, 0] != None and data.iloc[i, 1] != None:
            if username == data.iloc[i, 0]:
                exist = 0
                cSite = i
                if password == data.iloc[i, 1]:
                    exist = 1
                else:
                    exist = 0
    for i in range(0, quantity):
        if data.iloc[i, 3] != None:
            if email == data.iloc[i, 3]:
                exist = 2
    return exist, cSite # cSite: index of account in sheet

def sendConfirmEmail(email):
    confirm_code = random.randint(100000, 1000000)
    message = EmailMessage()
    subject = "Confirm your account"
    body = "Your code confirmation is: " + str(confirm_code)
    sender_email = "nhom11.test@gmail.com"
    receiver_email = email
    sender_email_password = "kptb tagm qjle pjyw"
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.set_content(body)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context = context) as server:
        server.login(sender_email, sender_email_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
    return str(confirm_code)

def confirmAccountScreen(username, password, email):
    global language, music
    inputCode = ""
    running = True
    clicked = False
    typingCode = False
    pushConfirmButton = False
    pushSendcodeButton = False
    register = False
    status = None
    sendcode = None
    startSound.play()
    startSound.set_volume(music)
    while running:
        confirmscreen = pygame.image.load(r'img\loginscreen\confirmscreen\{}.png'.format(language))
        DISPLAYSURFACE.blit(confirmscreen, (0, 0))
        codeArea = pygame.Rect(415, 376, 247, 38)
        confirmButton = pygame.Rect(561, 425, 83, 38)
        sendcodeButton = pygame.Rect(427, 425, 113, 38)
        exitButton = pygame.Rect(922, 71, 88, 87)

        dx, dy = pygame.mouse.get_pos()

        if codeArea.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), codeArea, 3, 30)
            if clicked:
                typingCode = True
                pushConfirmButton = False
                pushSendcodeButton = False
                status = None
        if confirmButton.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), confirmButton, 3, 30)
            if clicked:
                typingCode = False
                pushConfirmButton = True
                pushSendcodeButton = False
                status = None
        if sendcodeButton.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), sendcodeButton, 3, 30)
            if clicked:
                typingCode = False
                pushConfirmButton = False
                pushSendcodeButton = True
                status = None
        if exitButton.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), exitButton, 3, 15)
            if clicked:
                running = False

        clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouseClick.play()
                    mouseClick.set_volume(music)
                    clicked = True
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    if inputCode == "":
                        pushConfirmButton = False
                    else:
                        pushConfirmButton = True
                else:
                    if typingCode:
                        if event.key == K_BACKSPACE:
                            inputCode = inputCode[0: -1]
                        else:
                            if event.key in numberKey:
                                if len(inputCode) <= 15:
                                    inputCode += event.unicode
        if pushSendcodeButton:
            sendcode = sendConfirmEmail(email)
            pushSendcodeButton = False

        if pushConfirmButton:
            if inputCode == "":
                pushConfirmButton = False
            elif inputCode == sendcode:
                startSound.stop()
                running = False
                register = True
            else:
                status = 0
                pushConfirmButton = False
                register = False
        draw_text(inputCode, mediumFont, (0, 0, 0), DISPLAYSURFACE, 513, 386)
        if status == 0:
            if language == 0:
                draw_text('Wrong code', bigFont, (0, 0, 0), DISPLAYSURFACE, 488, 480)
            else:
                draw_text('Mã xác nhận không đúng', bigFont, (0, 0, 0), DISPLAYSURFACE, 430, 480)
        fpsClock.tick(FPS)
        pygame.display.update()
    if register:
        return signUpAndLoad(username, password, email)
    else:
        signupScreen()

def signUpAndLoad(username, password, email):
    global quantity, language
    money = 300
    numItem = 0
    countItem = 0
    numRace = 0
    Path = os.path.join('User', str(username))
    data.iloc[quantity, 0] = username
    data.iloc[quantity, 1] = password
    data.iloc[quantity, 2] = int(money)
    data.iloc[quantity, 3] = email
    data.iloc[quantity, 5] = int(numItem)
    data.iloc[quantity, 6] = int(countItem)
    data.iloc[quantity, 7] = int(numRace)
    data.iloc[quantity, 8] = Path
    lSite = quantity
    quantity += 1
    data.iloc[0, 4] = quantity
    data.to_csv(database, index = False)
    Path = os.path.join(os.getcwd(), 'History', str(username))
    os.mkdir(Path)
    return lSite, username, password, money, numItem, countItem, numRace

def loadGame():
    global site
    username = data.iloc[site, 0]
    password = data.iloc[site, 1]
    money = int(data.iloc[site, 2])
    numItem = int(data.iloc[site, 5])
    countItem = int(data.iloc[site, 6])
    numRace = int(data.iloc[site, 7])
    lSite = site
    return lSite, username, password, money, numItem, countItem, numRace

def signupScreen():
    global site, language, music
    running = True
    clicked = False
    inputUserName = ""
    inputPassword = ""
    inputEmail = ""
    censoredPassword = ""
    inputRePassword = ""
    censoredRePassword = ""
    typingUserName = False
    typingPassword = False
    retypingPassword = True
    typingEmail = False
    pushSignupButton = False
    startSound.play()
    startSound.set_volume(music)
    status = None
    while running:
        signupscreen = pygame.image.load(r'img\loginscreen\signupscreen\{}.png'.format(language))
        DISPLAYSURFACE.blit(signupscreen, (0, 0))
        userNameArea = pygame.Rect(286, 303, 509, 45)
        passwordArea = pygame.Rect(286, 360, 509, 45)
        retypePasswordArea = pygame.Rect(286, 417, 509, 45)
        mailArea = pygame.Rect(286, 474, 509, 45)
        signupButton = pygame.Rect(490, 531, 100, 46)
        exitButton = pygame.Rect(922, 71, 88, 87)

        dx, dy = pygame.mouse.get_pos()

        checkExist, site = checkExistAccount(inputUserName, inputPassword, inputEmail)

        if userNameArea.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), userNameArea, 3, 30)
            if clicked:
                typingUserName = True
                typingPassword = False
                typingEmail = False
                pushSignupButton = False
                status = None
        if passwordArea.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), passwordArea, 3, 30)
            if clicked:
                typingPassword = True
                typingUserName = False
                typingEmail = False
                pushSignupButton = False
                status = None
        if retypePasswordArea.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), retypePasswordArea, 3, 30)
            if clicked:
                typingPassword = False
                retypingPassword = True
                typingEmail = False
                typingUserName = False
                pushSignupButton = False
                status = None
        if mailArea.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), mailArea, 3, 30)
            if clicked:
                typingEmail = True
                typingPassword = False
                typingUserName = False
                retypingPassword = False
                pushSignupButton = False
                status = None
        if exitButton.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), exitButton, 3, 15)
            if clicked:
                running = False
                startSound.stop()
        if signupButton.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), signupButton, 3, 30)
            if clicked:
                typingUserName = False
                typingPassword = False
                pushSignupButton = True
                typingEmail = False
                status = None

        clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouseClick.play()
                    mouseClick.set_volume(music)
                    clicked = True
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    if inputUserName == "" or inputPassword == "":
                        pushSignupButton = False
                    else:
                        pushSignupButton = True
                else:
                    if typingUserName and not typingPassword and not typingEmail:
                        if event.key == K_BACKSPACE:
                            inputUserName = inputUserName[0: -1]
                        else:
                            if (event.key in characterKey) or (event.key in numberKey):
                                if len(inputUserName) < 25:
                                    inputUserName += event.unicode
                    elif typingPassword and not typingUserName and not typingEmail:
                        if event.key == K_BACKSPACE:
                            inputPassword = inputPassword[0: -1]
                            censoredPassword = censoredPassword[0: -1]
                        else:
                            if event.key in characterKey or event.key in numberKey:
                                if len(inputPassword) < 25:
                                    inputPassword += event.unicode
                                    censoredPassword += '*'
                    elif retypingPassword and not typingPassword and not typingUserName and not typingEmail:
                        if event.key == K_BACKSPACE:
                            inputRePassword = inputRePassword[0: -1]
                            censoredRePassword = censoredRePassword[0: -1]
                        else:
                            if event.key in characterKey or event.key in numberKey:
                                if len(inputRePassword) < 25:
                                    inputRePassword += event.unicode
                                    censoredRePassword += '*'
                    elif typingEmail and not typingUserName and not typingPassword:
                        if event.key == K_BACKSPACE:
                            inputEmail = inputEmail[0: -1]
                        else:
                            if len(inputEmail) < 35:
                                inputEmail += event.unicode
            if pushSignupButton:
                if inputUserName == "" or inputPassword == "" or inputEmail == "" or inputRePassword == "":
                    pushSignupButton = False
                elif inputEmail[len(inputEmail) - 10:len(inputEmail)] != "@gmail.com" or inputEmail[0] == "@":
                    status = 4
                else:
                    if checkExist == 2:
                        status = 3
                    else:
                        if checkExist == 0 or checkExist == 1:
                            status = 0
                        else:
                            if inputPassword != inputRePassword:
                                status = 2
                            else:
                                status = 1
        if status == 4:
            if language == 0:
                draw_text('Invalid email!', bigFont, (0, 0, 0), DISPLAYSURFACE, 450, 583)
            else:
                draw_text('Email không hợp lệ!', bigFont, (0, 0, 0), DISPLAYSURFACE, 440, 583)
        elif status == 3:
            if language == 0:
                draw_text('Email was used to create another account!', bigFont, (0, 0, 0), DISPLAYSURFACE, 335, 583)
            else:
                draw_text('Email đã được sử dụng cho một tài khoản khác!', bigFont, (0, 0, 0), DISPLAYSURFACE, 335, 583)
        elif status == 0:
            if language == 0:
                draw_text("Username was existed, please enter another username!", bigFont, (0, 0, 0), DISPLAYSURFACE, 315, 583)
            else:
                draw_text('Tên đăng nhập đã tồn tại, vui lòng nhập lại!', bigFont, (0, 0, 0), DISPLAYSURFACE, 345, 583)
        elif status == 2:
            if language == 0:
                draw_text('Confirmation password is incorrect!', bigFont, (0, 0, 0), DISPLAYSURFACE, 370, 583)
            else:
                draw_text('Mật khẩu xác nhận không đúng!', bigFont, (0, 0, 0), DISPLAYSURFACE, 395, 583)
        elif status == 1:
            running = False
            startSound.stop()
            confirmAccountScreen(inputUserName, inputPassword, inputEmail)
        draw_text(inputUserName, mediumFont, (0, 0, 0), DISPLAYSURFACE, 477, 316)
        draw_text(censoredPassword, passwordFont, (0, 0, 0), DISPLAYSURFACE, 477, 375)
        draw_text(censoredRePassword, passwordFont, (0, 0, 0), DISPLAYSURFACE, 477, 431)
        draw_text(inputEmail, mediumFont, (0, 0, 0), DISPLAYSURFACE, 477, 487)
        fpsClock.tick(FPS)
        pygame.display.update()

def loginScreen():
    global site, language, music
    running = True
    clicked = False
    inputUserName = ""
    inputPassword = ""
    censoredPassword = ""
    typingUserName = False
    typingPassword = False
    pushLoginButton = False
    pushSignupButton = False
    pushForgotButton = False
    pushFaceIDButton = False
    pushSettingButton = False
    status = None
    startSound.play()
    startSound.set_volume(music)
    while running:
        loginscreen = pygame.image.load(r'img\loginscreen\loginscreen\{}.png'.format(language))
        DISPLAYSURFACE.blit(loginscreen, (0, 0))
        userNameArea = pygame.Rect(355, 315, 372, 48)
        passwordArea = pygame.Rect(355, 382, 372, 48)
        loginButton = pygame.Rect(400, 460, 107, 45)
        signupButton = pygame.Rect(530, 460, 102, 45)
        forgotPasswordArea = pygame.Rect(362, 430, 150, 27)
        faceIDButton = pygame.Rect(674, 459, 50, 50)
        settingButton = pygame.Rect(932, 584, 77, 77)

        dx, dy = pygame.mouse.get_pos()

        checkExist, site = checkExistAccount1(inputUserName, inputPassword)

        if userNameArea.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), userNameArea, 3, 30)
            if clicked:
                typingUserName = True
                typingPassword = False
                pushSignupButton = False
                pushLoginButton = False
                status = None
        if passwordArea.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), passwordArea, 3, 30)
            if clicked:
                typingPassword = True
                typingUserName = False
                pushLoginButton = False
                pushSignupButton = False
                pushFaceIDButton = False
                pushSettingButton = False
                pushForgotButton = False
                status = None
        if loginButton.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), loginButton, 3, 30)
            if clicked:
                typingPassword = False
                typingUserName = False
                pushLoginButton = True
                pushSignupButton = False
                pushSettingButton = False
                pushFaceIDButton = False
                pushForgotButton = False
                status = None
        if signupButton.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), signupButton, 3, 30)
            if clicked:
                typingUserName = False
                typingPassword = False
                pushSignupButton = True
                pushLoginButton = False
                pushFaceIDButton = False
                pushSettingButton = False
                pushForgotButton = False
                status = None
        if forgotPasswordArea.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), forgotPasswordArea, 3, 10)
            if clicked:
                pushForgotButton = True
                typingUserName = False
                typingPassword = False
                pushSignupButton = False
                pushLoginButton = False
                pushFaceIDButton = False
                pushSettingButton = False
                status = None
        if faceIDButton.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), faceIDButton, 3, 10)
            if clicked:
                pushFaceIDButton = True
                pushLoginButton = False
                pushSignupButton = False
                pushForgotButton = False
                pushSettingButton = False
                status = None
        if settingButton.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), settingButton, 3, 25)
            if clicked:
                pushFaceIDButton = False
                pushLoginButton = False
                pushSettingButton = True
                status = None

        clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouseClick.play()
                    mouseClick.set_volume(music)
                    clicked = True
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    if inputUserName == "" or inputPassword == "":
                        pushLoginButton = False
                    else:
                        pushLoginButton = True
                else:
                    if typingUserName and not typingPassword:
                        if event.key == K_BACKSPACE:
                            inputUserName = inputUserName[0: -1]
                        else:
                            if event.key in characterKey or event.key in numberKey:
                                if len(inputUserName) < 25:
                                    inputUserName += event.unicode
                    elif typingPassword and not typingUserName:
                        if event.key == K_BACKSPACE:
                            inputPassword = inputPassword[0: -1]
                            censoredPassword = censoredPassword[0: -1]
                        else:
                            if event.key in characterKey or event.key in numberKey:
                                if len(inputPassword) < 25:
                                    inputPassword += event.unicode
                                    censoredPassword += '*'
        if pushLoginButton:
            if inputUserName == "" or inputPassword == "":
                pushLoginButton = False
            else:
                if checkExist == 1:
                    status = 1
                elif checkExist == 0:
                    status = 0
                elif checkExist == -1:
                    status = -1
        if pushFaceIDButton:
            if inputUserName == "":
                pushFaceIDButton = False
            else:
                startSound.stop()
                check = False
                path = 'faceid/' + inputUserName
                images = []
                classNames = []
                myList = os.listdir(path)
                name = ""
                for cl in myList:
                    curImg = cv2.imread(f"{path}/{cl}")
                    images.append(curImg)
                    classNames.append(os.path.splitext(cl)[0])

                def encode(images):
                    encodeList = []
                    for img in images:
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        encode = face_recognition.face_encodings(img)[0]
                        encodeList.append(encode)
                    return encodeList

                encodeListKnow = encode(images)
                cap = cv2.VideoCapture(0)
                while True:
                    ret, frame = cap.read()
                    framS = cv2.resize(frame, (0, 0), None, fx=0.5, fy=0.5)
                    framS = cv2.cvtColor(framS, cv2.COLOR_BGR2RGB)

                    faceCurFrame = face_recognition.face_locations(framS)
                    encodeCurFrame = face_recognition.face_encodings(framS)

                    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
                        matches = face_recognition.compare_faces(encodeListKnow, encodeFace)
                        faceDis = face_recognition.face_distance(encodeListKnow, encodeFace)
                        matchIndex = np.argmin(faceDis)

                        if faceDis[matchIndex] < 0.50:
                            check = True
                        else:
                            name = "INVALID"

                        y1, x2, y2, x1 = faceLoc
                        y1, x2, y2, x1 = y1 * 2, x2 * 2, y2 * 2, x1 * 2
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(frame, name, (x2, y2), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
                    cv2.imshow('Face ID', frame)
                    if cv2.waitKey(1) == ord("q"):
                        break
                    if check:
                        cap.release()
                        cv2.destroyAllWindows()
                        return loadGame()

                cap.release()
                cv2.destroyAllWindows()
                startSound.play()
                startSound.set_volume(music)
                pushFaceIDButton = False
        if pushForgotButton:
            startSound.stop()
            forgotScreen()
            startSound.play()
            startSound.set_volume(music)
            pushForgotButton = False
        if pushSignupButton:
            startSound.stop()
            signupScreen()
            startSound.play()
            startSound.set_volume(music)
            pushSignupButton = False
        if pushSettingButton:
            startSound.stop()
            settingScreen()
            startSound.play()
            startSound.set_volume(music)
            pushSettingButton = False
        draw_text(inputUserName, mediumFont, (0, 0, 0), DISPLAYSURFACE, 467, 329)
        draw_text(censoredPassword, passwordFont, (0, 0, 0), DISPLAYSURFACE, 467, 396)
        if status == 0:
            if language == 0:
                draw_text('Wrong password', bigFont, (0, 0, 0), DISPLAYSURFACE, 460, 518)
            else:
                draw_text('Sai mật khẩu', bigFont, (0, 0, 0), DISPLAYSURFACE, 460, 518)
        elif status == -1:
            if language == 0:
                draw_text('Account is not exist', bigFont, (0, 0, 0), DISPLAYSURFACE, 438, 518)
            else:
                draw_text('Tài khoản không tồn tại', bigFont, (0, 0, 0), DISPLAYSURFACE, 438, 518)
        elif status == 1:
            running = False
            startSound.stop()
            return loadGame()

        pygame.display.update()
        fpsClock.tick(FPS)

def settingScreen():
    global music, language
    running = True
    clicked = False
    status = None
    pushFaceIDButton = False
    startSound.play()
    startSound.set_volume(music)
    while running:
        settingscreen = pygame.image.load(r'img\menu\settingscreen\{}.png'.format(language))
        DISPLAYSURFACE.blit(settingscreen, (0, 0))
        language0Button = pygame.Rect(674, 356, 61, 40)
        language1Button = pygame.Rect(557, 357, 60, 40)
        onButton = pygame.Rect(545, 243, 80, 80)
        offButton = pygame.Rect(660, 243, 80, 80)
        FaceIDButton = pygame.Rect(295, 432, 480, 68)
        exitButton = pygame.Rect(921, 70, 90, 90)

        dx, dy = pygame.mouse.get_pos()

        if language0Button.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), language0Button, 3)
            if clicked:
                language = 0
                status = None
                pushFaceIDButton = False
        if language1Button.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), language1Button, 3)
            if clicked:
                language = 1
                status = None
                pushFaceIDButton = False
        if exitButton.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), exitButton, 3, 25)
            if clicked:
                running = False
                startSound.stop()
                pushFaceIDButton = False
        if onButton.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), onButton, 3, 360)
            if clicked:
                music = 1
                pushFaceIDButton = False
                startSound.play()
                status = None
        if offButton.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), offButton, 3, 360)
            if clicked:
                music = 0
                pushFaceIDButton = False
                startSound.stop()
                status = None
        if FaceIDButton.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), FaceIDButton, 3, 30)
            if clicked:
                pushFaceIDButton = True
                status = None

        clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouseClick.play()
                    mouseClick.set_volume(music)
                    clicked = True
        if pushFaceIDButton:
            status = 0
        if status == 0:
            if language == 0:
                draw_text('LOG IN TO SETUP FACE ID', bigFont, (0, 0, 0), DISPLAYSURFACE, 427, 520)
            else:
                draw_text('ĐĂNG NHẬP ĐỂ THIẾT LẬP FACE ID', bigFont, (0, 0, 0), DISPLAYSURFACE, 387, 520)
        pygame.display.update()
        fpsClock.tick(FPS)

def forgotScreen():
    global site, language, music
    running = True; clicked = False
    inputUserName = ""
    inputEmail = ""
    inputCode = ""
    typingUserName = False
    typingEmail = False
    typingCode = False
    pushConfirmButton = False
    sendcode = None
    status = None
    pushSendcodeButton = False
    startSound.play()
    startSound.set_volume(music)
    while running:
        forgotscreen = pygame.image.load(r'img\loginscreen\forgotscreen\{}.png'.format(language))
        DISPLAYSURFACE.blit(forgotscreen, (0, 0))
        userNameArea = pygame.Rect(252, 343, 578, 45)
        emailArea = pygame.Rect(252, 400, 451, 45)
        codeArea = pygame.Rect(252, 457, 576, 48)
        confirmButton = pygame.Rect(490, 516, 102, 49)
        sendcodeButton = pygame.Rect(712, 398, 116, 48)
        exitButton = pygame.Rect(922, 71, 88, 87)

        dx, dy = pygame.mouse.get_pos()
        checkExist, site = checkExistAccount(inputUserName, "", inputEmail)

        if userNameArea.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), userNameArea, 3, 30)
            if clicked:
                typingUserName = True
                typingEmail = False
                typingCode = False
                pushConfirmButton = False
                status = None
        if emailArea.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), emailArea, 3, 30)
            if clicked:
                typingUserName = False
                typingEmail = True
                typingCode = False
                pushConfirmButton = False
                status = None
        if codeArea.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), codeArea, 3, 30)
            if clicked:
                typingCode = True
                typingEmail = False
                typingUserName = False
                pushConfirmButton = False
                status = None
        if sendcodeButton.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), sendcodeButton, 3, 30)
            if clicked:
                pushSendcodeButton = True
                pushConfirmButton = False
        if exitButton.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), exitButton, 3, 15)
            if clicked:
                running = False
        if confirmButton.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), confirmButton, 3, 30)
            if clicked:
                typingUserName = False
                typingEmail = False
                typingCode = False
                pushConfirmButton = True
                status = None

        clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouseClick.play()
                    mouseClick.set_volume(music)
                    clicked = True
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    if inputUserName == "" or inputCode == "" or inputEmail == "":
                        pushConfirmButton = False
                    else:
                        pushConfirmButton = True
                else:
                    if typingUserName and not typingCode and not typingEmail:
                        if event.key == K_BACKSPACE:
                            inputUserName = inputUserName[0: -1]
                        else:
                            if (event.key in characterKey) or (event.key in numberKey):
                                if len(inputUserName) < 25:
                                    inputUserName += event.unicode
                    elif typingCode and not typingUserName and not typingEmail:
                        if event.key == K_BACKSPACE:
                            inputCode = inputCode[0: -1]
                        else:
                            if event.key in numberKey:
                                if len(inputCode) < 10:
                                    inputCode += event.unicode
                    elif typingEmail and not typingUserName and not typingCode:
                        if event.key == K_BACKSPACE:
                            inputEmail = inputEmail[0: -1]
                        else:
                            if len(inputEmail) < 35:
                                inputEmail += event.unicode
        if pushSendcodeButton:
            sendcode = sendConfirmEmail(inputEmail)
            pushSendcodeButton = False
        if pushConfirmButton:
            if inputUserName == "" or inputEmail == "" or inputCode == "":
                pushConfirmButton = False
            else:
                if checkExist == -1:
                    status = 0
                else:
                    if str(inputCode) != sendcode:
                        status = 1
                    else:
                        status = 2
                pushConfirmButton = False
        if status == 0:
            if language == 0:
                draw_text('Account is not exist!', bigFont, (0, 0, 0), DISPLAYSURFACE, 455, 570)
            else:
                draw_text('Tài khoản không tồn tại!', bigFont, (0, 0, 0), DISPLAYSURFACE, 435, 570)
        elif status == 1:
            if language == 0:
                draw_text("Wrong code!", bigFont, (0, 0, 0), DISPLAYSURFACE, 487, 570)
            else:
                draw_text('Mã không đúng!', bigFont, (0, 0, 0), DISPLAYSURFACE, 473, 570)
        elif status == 2:
            startSound.stop()
            changePasswordScreen(site)
            status = None
            running = False

        draw_text(inputUserName, mediumFont, (0, 0, 0), DISPLAYSURFACE, 380, 355)
        draw_text(inputEmail, mediumFont, (0, 0, 0), DISPLAYSURFACE, 380, 413)
        draw_text(inputCode, mediumFont, (0, 0, 0), DISPLAYSURFACE, 380, 471)
        fpsClock.tick(FPS)
        pygame.display.update()

def changePasswordScreen(site):
    global language, music
    running = True; clicked = False
    inputPassword = ""
    censoredPassword = ""
    inputRePassword = ""
    censoredRePassword = ""
    typingPassword = False
    retypingPassword = True
    pushChangeButton = False
    status = None
    startSound.play()
    startSound.set_volume(music)
    while running:
        changenewpw = pygame.image.load(r'img\loginscreen\changenewpw\{}.png'.format(language))
        DISPLAYSURFACE.blit(changenewpw, (0, 0))
        newPWArea = pygame.Rect(294, 362, 489, 47)
        confirmPWArea = pygame.Rect(294, 416, 489, 47)
        changeButton = pygame.Rect(452, 482, 176, 70)
        exitButton = pygame.Rect(922, 71, 88, 87)

        dx, dy = pygame.mouse.get_pos()

        if newPWArea.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), newPWArea, 3, 30)
            if clicked:
                typingPassword = True
                retypingPassword = False
                pushChangeButton = False
                status = None
        if confirmPWArea.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), confirmPWArea, 3, 30)
            if clicked:
                typingPassword = False
                retypingPassword = True
                pushChangeButton = False
                status = None
        if exitButton.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), exitButton, 3, 15)
            if clicked:
                running = False
        if changeButton.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), changeButton, 3, 45)
            if clicked:
                typingPassword = False
                retypingPassword = False
                pushChangeButton = True
                status = None

        clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouseClick.play()
                    mouseClick.set_volume(music)
                    clicked = True
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    if inputRePassword == "" or inputPassword == "":
                        pushChangeButton = False
                    else:
                        pushChangeButton = True
                else:
                    if typingPassword and not retypingPassword:
                        if event.key == K_BACKSPACE:
                            inputPassword = inputPassword[0: -1]
                            censoredPassword = censoredPassword[0: -1]
                        else:
                            if event.key in characterKey or event.key in numberKey:
                                if len(inputPassword) < 25:
                                    inputPassword += event.unicode
                                    censoredPassword += '*'
                    elif retypingPassword and not typingPassword:
                        if event.key == K_BACKSPACE:
                            inputRePassword = inputRePassword[0: -1]
                            censoredRePassword = censoredRePassword[0: -1]
                        else:
                            if event.key in characterKey or event.key in numberKey:
                                if len(inputRePassword) < 25:
                                    inputRePassword += event.unicode
                                    censoredRePassword += '*'
            if pushChangeButton:
                if inputPassword == "" or inputRePassword == "":
                    pushChangeButton = False
                else:
                    if inputPassword != inputRePassword:
                        status = 0
                    else:
                        status = 1
        if status == 0:
            if language == 0:
                draw_text('Confirmation password is incorrect!', bigFont, (0, 0, 0), DISPLAYSURFACE, 380, 553)
            else:
                draw_text('Mật khẩu xác nhận không đúng!', bigFont, (0, 0, 0), DISPLAYSURFACE, 397, 553)
        elif status == 1:
            running = False
            startSound.stop()
            changePW(site, inputPassword)
        draw_text(censoredPassword, passwordFont, (0, 0, 0), DISPLAYSURFACE, 485, 377)
        draw_text(censoredRePassword, passwordFont, (0, 0, 0), DISPLAYSURFACE, 485, 431)
        fpsClock.tick(FPS)
        pygame.display.update()

def changePW(site, password):
    data.iloc[site, 1] = password
    data.to_csv(database, index = False)

def mainMenu():
    pygame.display.set_mode(WINDOWSIZE)
    pygame.display.set_icon(icon)
    pygame.display.set_caption('Lucky Race')
    global language, Player, music
    running = True; clicked = False
    ingameSound.play()
    ingameSound.set_volume(music)
    while running:
        mainmenuscreen = pygame.image.load(r'img\menu\mainmenu.png')
        mainmenuscreen = pygame.transform.scale(mainmenuscreen, WINDOWSIZE)
        DISPLAYSURFACE.blit(mainmenuscreen, (0, 0))
        historyButton = pygame.Rect(185, 586, 82, 82)
        playButton = pygame.Rect(655, 281, 320, 159)
        miniGameButton = pygame.Rect(482, 596, 137, 61)
        shopButton = pygame.Rect(71, 587, 82, 82)
        exitButton = pygame.Rect(941, 34, 97, 77)
        guideButton = pygame.Rect(74, 38, 78, 78)
        settingButton = pygame.Rect(932, 584, 77, 77)
        draw_text(str(Player.username), userNameFont, (0, 0, 0), DISPLAYSURFACE, 425, 52)
        draw_text(str(Player.money), bigFont, coinColor, DISPLAYSURFACE, 619, 58)

        dx, dy = pygame.mouse.get_pos()

        if settingButton.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), settingButton, 3, 25)
            if clicked:
                ingameSound.stop()
                settingScreenMenu(Player.username)
                ingameSound.play()
                ingameSound.set_volume(music)
        if exitButton.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), exitButton, 3, 15)
            if clicked:
                saveGame(Player.lSite, Player.money)
                ingameSound.stop()
                confirmExitScreen()
                ingameSound.play()
                ingameSound.set_volume(music)
        if guideButton.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), guideButton, 3, 100)
            if clicked:
                ingameSound.stop()
                helpScreen(1)
                ingameSound.play()
                ingameSound.set_volume(music)
        if miniGameButton.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), miniGameButton, 3, 30)
            if clicked:
                ingameSound.stop()
                Player.money = miniGameScreen(Player.money)
                saveGame(Player.lSite, Player.money)
                ingameSound.play()
                ingameSound.set_volume(music)
        if shopButton.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), shopButton, 3, 30)
            if clicked:
                ingameSound.stop()
                Player.money = shopScreen(Player.lSite)
                ingameSound.play()
                ingameSound.set_volume(music)
        if historyButton.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), historyButton, 3, 30)
            if clicked:
                ingameSound.stop()
                history(Player.lSite)
                ingameSound.play()
                ingameSound.set_volume(music)
        if playButton.collidepoint(dx, dy):
            if clicked:
                ChooseSet()

        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                saveGame(Player.lSite, Player.money)
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouseClick.play()
                    mouseClick.set_volume(music)
                    clicked = True
        fpsClock.tick(FPS)
        pygame.display.update()

def ChooseSet():
    global language, Player, music
    running = True; clicked = False
    Set = 0
    status = None
    while running:
        selectsetscreen = pygame.image.load(r'img\menu\selectsetscreen\{}.png'.format(language))
        DISPLAYSURFACE.blit(selectsetscreen, (0, 0))
        set1 = pygame.Rect(170, 421, 103, 108)
        set2 = pygame.Rect(591, 352, 94, 100)
        set3 = pygame.Rect(895, 205, 72, 76)
        set4 = pygame.Rect(480, 122, 59, 55)
        set5 = pygame.Rect(753, 74, 43, 43)
        exitButton = pygame.Rect(946, 27, 91, 89)

        dx, dy = pygame.mouse.get_pos()
        if set1.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), set1, 3, 100)
            if clicked:
                Set = 1
                status = None
                print(Set)
        if set2.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), set2, 3, 100)
            if clicked:
                Set = 2
                status = None
                print(Set)
        if set3.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), set3, 3, 100)
            if clicked:
                Set = 3
                status = None
                print(Set)
        if set4.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), set4, 3, 100)
            if clicked:
                Set = 4
                status = None
                print(Set)
        if set5.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), set5, 3, 100)
            if clicked:
                Set = 5
                status = None
                print(Set)
        if exitButton.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), exitButton, 3, 25)
            if clicked:
                running = False
        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouseClick.play()
                    mouseClick.set_volume(music)
                    clicked = True
        if Set > 0 and Set < 5:
            NormalSet(Set)
            Set = 0
        elif Set == 5:
            if Player.numRace < 6:
                status = 0
            else:
                FinalSet(Set)
            Set = 0
        if status == 0:
            if language == 0:
                draw_text("Locked", bigFont, (0, 0, 0), DISPLAYSURFACE, 600, 45)
            else:
                draw_text("Chưa mở khóa", bigFont, (0, 0, 0), DISPLAYSURFACE, 583, 45)
        fpsClock.tick(FPS)
        pygame.display.update()

def NormalSet(Set):
    global Player, music, language
    clicked = False; running = True
    chooseCar = 0
    while running:
        set = pygame.image.load(r'img\menu\selectfigure\set{}\{}.png'.format(Set, language))
        DISPLAYSURFACE.blit(set, (0, 0))
        exitButton = pygame.Rect(921, 70, 90, 90)
        car1 = pygame.Rect(145, 563, 215, 85)
        car2 = pygame.Rect(201, 434, 118, 50)
        car3 = pygame.Rect(500, 396, 86, 47)
        car4 = pygame.Rect(844, 412, 100, 45)
        car5 = pygame.Rect(721, 575, 170, 84)

        dx, dy = pygame.mouse.get_pos()

        if exitButton.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), exitButton, 3, 25)
            if clicked:
                running = False
        if car1.collidepoint(dx, dy):
            if clicked:
                chooseCar = 1
        if car2.collidepoint(dx, dy):
            if clicked:
                chooseCar = 2
        if car3.collidepoint(dx, dy):
            if clicked:
                chooseCar = 3
        if car4.collidepoint(dx, dy):
            if clicked:
                chooseCar = 4
        if car5.collidepoint(dx, dy):
            if clicked:
                chooseCar = 5
        if chooseCar != 0:
            enterBetScreen(chooseCar, Set)
            chooseCar = 0
        clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouseClick.play()
                    mouseClick.set_volume(music)
                    clicked = True
        fpsClock.tick(FPS)
        pygame.display.update()

def FinalSet(Set):
    global music, language
    clicked = False; running = True
    chooseCar = 0
    while running:
        set = pygame.image.load(r'img\menu\selectfigure\set{}\{}.png'.format(Set, language))
        DISPLAYSURFACE.blit(set, (0, 0))
        exitButton = pygame.Rect(921, 70, 90, 90)
        car1 = pygame.Rect(190, 335, 140, 110)
        car2 = pygame.Rect(483, 335, 140, 110)
        car3 = pygame.Rect(798, 335, 140, 110)
        car4 = pygame.Rect(190, 511, 140, 110)
        car5 = pygame.Rect(483, 511, 140, 110)
        car6 = pygame.Rect(483, 511, 140, 110)

        dx, dy = pygame.mouse.get_pos()

        if exitButton.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), exitButton, 3, 25)
            if clicked:
                running = False
        if car1.collidepoint(dx, dy):
            if clicked:
                chooseCar = 1
        if car2.collidepoint(dx, dy):
            if clicked:
                chooseCar = 2
        if car3.collidepoint(dx, dy):
            if clicked:
                chooseCar = 3
        if car4.collidepoint(dx, dy):
            if clicked:
                chooseCar = 4
        if car5.collidepoint(dx, dy):
            if clicked:
                chooseCar = 5
        if car6.collidepoint(dx, dy):
            if clicked:
                chooseCar = 6
        if chooseCar != 0:
            enterBetScreen(chooseCar, Set)
            chooseCar = 0
        clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouseClick.play()
                    mouseClick.set_volume(music)
                    clicked = True
        fpsClock.tick(FPS)
        pygame.display.update()

def enterBetScreen(chooseCar, set):
    global language, Player, music
    running = True; clicked = False
    betInput = ""
    typingBet = False
    status = None
    while running:
        betscreen = pygame.image.load(r'img\menu\betscreen\{}.png'.format(language))
        DISPLAYSURFACE.blit(betscreen, (0, 0))
        betArea = pygame.Rect(476, 334, 130, 51)
        exitButton = pygame.Rect(921, 70, 90, 90)
        draw_text(str(Player.money), bigFont, coinColor, DISPLAYSURFACE, 505, 103)

        dx, dy = pygame.mouse.get_pos()

        if betArea.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), betArea, 3, 25)
            if clicked:
                typingBet = True
                status = None
        if exitButton.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), exitButton, 3, 25)
            if clicked:
                running = False

        clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouseClick.play()
                    mouseClick.set_volume(music)
                    clicked = True
            if event.type == KEYDOWN:
                if event.key == K_RETURN and betInput != "":
                    if int(betInput) <= Player.money and int(betInput) >= 200:
                        Player.bet = int(betInput)
                        chooseRacetrack(set, chooseCar)
                    elif int(betInput) < 200:
                        status = 1
                    elif int(betInput) > Player.money:
                        status = 0
                if typingBet:
                    if event.key == K_BACKSPACE:
                        betInput = betInput[0: -1]
                    else:
                        if event.key in numberKey:
                            if len(betInput) <= 5:
                                betInput += event.unicode
        if status == 0:
            if language == 0:
                draw_text("Not enough money!!!", bigFont, (0, 0, 0), DISPLAYSURFACE, 450, 410)
            else:
                draw_text("Không đủ tiền!!!", bigFont, (0, 0, 0), DISPLAYSURFACE, 475, 410)
        elif status == 1:
            if language == 0:
                draw_text("More than 200!!!", bigFont, (0, 0, 0), DISPLAYSURFACE, 450, 410)
            else:
                draw_text("Lớn hơn 200!!!", bigFont, (0, 0, 0), DISPLAYSURFACE, 475, 410)
        draw_text(betInput, bigFont, coinColor, DISPLAYSURFACE, 500, 349)
        fpsClock.tick(FPS)
        pygame.display.update()

def confirmExitScreen():
    global language, music
    running = True; clicked = False
    while running:
        confirmexitscreen = pygame.image.load(r'img\menu\confirmexitscreen\{}.png'.format(language))
        DISPLAYSURFACE.blit(confirmexitscreen, (0, 0))
        yesButton = pygame.Rect(346, 376, 151, 70)
        noButton = pygame.Rect(580, 376, 151, 70)

        dx, dy = pygame.mouse.get_pos()
        if yesButton.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), yesButton, 3, 35)
            if clicked:
                pygame.quit()
                sys.exit()
        elif noButton.collidepoint(dx,dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), noButton, 3, 35)
            if clicked:
                running = False

        clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouseClick.play()
                    mouseClick.set_volume(music)
                    clicked = True
        fpsClock.tick(FPS)
        pygame.display.update()
    return running

def chooseRacetrack(set, chooseCar):
    global language, Player, music
    clicked = False; running = True
    raceSize = 0
    while running:
        selectracesize = pygame.image.load(r'img\menu\selectracesize\{}.png'.format(language))
        DISPLAYSURFACE.blit(selectracesize, (0, 0))
        shortRace = pygame.Rect(236, 368, 180, 67)
        mediumRace = pygame.Rect(671, 368, 180, 67)
        longRace = pygame.Rect(451, 608, 180, 67)
        exitButton = pygame.Rect(953, 26, 90, 90)
        dx, dy = pygame.mouse.get_pos()
        if shortRace.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), shortRace, 3, 35)
            if clicked:
                raceSize = 3
                running = False
        if mediumRace.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), mediumRace, 3, 35)
            if clicked:
                raceSize = 4
                running = False
        if longRace.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), longRace, 3, 35)
            if clicked:
                raceSize = 5
                running = False
        if exitButton.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), exitButton, 3, 25)
            if clicked:
                running = False

        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouseClick.play()
                    mouseClick.set_volume(music)
                    clicked = True
        if raceSize != 0:
            if set == 5:
                ingameSound.stop()
                playFinal(set, raceSize, chooseCar)
            else:
                ingameSound.stop()
                playGame(set, raceSize, chooseCar)
        fpsClock.tick(FPS)
        pygame.display.update()

class CCar:
	def __init__ (object, picture, x, y, width, rankIns, Rank):
		object.img = picture
		object.area = (x, y, 75, 50)
		object.x = x
		object.y = y
		object.width = width
		object.RankIns = rankIns
		object.Rank = Rank
		object.Ax = x + width
		object.flip = False
		object.speedup = False
		object.slow = False
		object.stop = False
		object.timer = False
		object.flash = False
		object.finish = False
		object.cheer = False
	def Area(object):
		return pygame.Rect(object.x, object.y, object.width, 50)

class Draw():
    def DrawBG2(BackGround1, BackGround2, xBg):
        screen.blit(BackGround1, (xBg, 0))
        screen.blit(BackGround2, (xBg + 1080, 0))

    def DrawBG3(BackGround1, BackGround2, BackGround3, xBg):
        screen.blit(BackGround1, (xBg, 0))
        screen.blit(BackGround2, (xBg + 1080, 0))
        screen.blit(BackGround3, (xBg + 1080 + 1080, 0))

    def DrawCar(Car, SpeedUpCheck, Speed):
        if SpeedUpCheck == 1:
            if Car.Rank == 0:
                Speed = random.randint(1, 5) % 10 + 0.01
                Car.x += Speed
        elif SpeedUpCheck == 2:
            if Car.Rank == 0:
                Car.x += Speed
        if Car.flip:
            flipImg = pygame.transform.flip(Car.img, True, False)
            screen.blit(flipImg, (Car.x, Car.y))
        else:
            screen.blit(Car.img, (Car.x, Car.y))

    def DrawRock(Car, RankCount, rand, CheckCollide, CheckScreen):
        Rock = image.load(r'img\menu\ChooseSet\Rock.png')
        dy = [190, 260, 335, 410, 480]
        for i in range(5):
            if CheckCollide[i] == 0:
                if CheckScreen == 1:
                    screen.blit(Rock, (rand[i], dy[i]))
                rand[i] -= 10
            Area = CCar.Area(Car[i])
            if Area.collidepoint(rand[i], dy[i] + 25):
                CheckCollide[i] += 1
                if CheckCollide[i] == 1:
                    RankCount = Draw.DrawCollide(Car[i], RankCount)
        return RankCount

    def Update(Car):
        if Car.flip:
            Car.timer -= 1
        if Car.timer <= 0 & Car.flip:     #Back
            Car.flip = False
        if Car.speedup:
            Car.x += 3
            Car.timer -= 1
        if Car.timer <= 0 & Car.speedup:  #Speed Up
            Car.speedup = False
        if Car.slow:
            Car.x -= 3
            Car.timer -= 1
        if Car.timer <= 0 & Car.slow:     #Slow
            Car.slow = False
        if Car.stop:
            Car.x -= 6
            Car.timer -= 1
        if Car.timer <= 0 & Car.stop:     #Stop
            Car.stop = False
        if Car.cheer:
            Car.timer -= 1
        if Car.timer <= 0 & Car.cheer:
            Car.cheer = False

    def DrawCollide(Car, RankCount):
        Back = pygame.image.load(r'img\menu\ChooseSet\Effect\Back.png')
        Slow = pygame.image.load(r'img\menu\ChooseSet\Effect\Slow.png')
        SpeedUp = pygame.image.load(r'img\menu\ChooseSet\Effect\SpeedUp.png')
        Finish = pygame.image.load(r'img\menu\ChooseSet\Effect\Finish.png')
        Stop = pygame.image.load(r'img\menu\ChooseSet\Effect\Stop.png')
        Effect = random.randrange(10, 65, 5) // 10
        if Effect == 1:	#Speedup
            screen.blit(SpeedUp, (Car.x, Car.y))
            Car.speedup = 1
            Car.timer = 30
        if Effect == 2:	#Slow
            screen.blit(Slow, (Car.x, Car.y))
            Car.slow = 1
            Car.timer = 30
        if Effect == 3:	#Stop
            screen.blit(Stop, (Car.x, Car.y))
            Car.stop = 1
            Car.timer = 30
        if Effect == 4:	#Back
            screen.blit(Back, (Car.x, Car.y))
            Car.flip = 1
            Car.timer = 30
        if Effect == 5: #Teleport
            screen.blit(SpeedUp, (Car.x, Car.y))
            Car.x += 50
        if Effect == 6:	#Finish
            screen.blit(Finish, (Car.x, Car.y))
            Car.x = 950
            Car.RankIns = RankCount
            Car.Rank = RankCount
            RankCount +=1
        return RankCount

    def DrawWeak(Set, Car, ChooseCar):
        if Set < 5:
            for i in range(5):
                if i != ChooseCar:
                    Car[i].timer = 20
                    Car[i].slow = True
        else:
            for i in range(6):
                if i != ChooseCar:
                    Car[i].timer = 20
                    Car[i].slow = True

    def DrawCheer(Car, ChooseCar):
        image_sprite = [pygame.image.load("img\Results\Firework_1.png"), pygame.image.load("img\Results\Firework_2.png"), pygame.image.load("img\Results\Firework_3.png"), pygame.image.load("img\Results\Firework_4.png")]
        dx = None
        dy = None
        for i in range(5):
            if Car[i].Rank == 1:
                dx = Car[i].x
                dy = Car[i].y
        if dx != None and dy != None:
            for i in range(4):
                image_sprite[i] = pygame.transform.scale(image_sprite[i], (50, 50))
                screen.blit(image_sprite[i], (dx - 50, dy))
                pygame.display.update()

def DeleteFiles(directory_path):
	files = os.listdir(directory_path)
	for file in files:
		file_path = os.path.join(directory_path, file)
		if os.path.isfile(file_path):
			os.remove(file_path)

def RankTable(Car, ChooseCar, StageCount, Race, CheckScreen):
    global Player
    Rankx = [1, 2, 3, 4, 5]
    for i in range(5):
        Rankx[i] = Car[i].x
    Rankx = sorted(Rankx)
    xrank = 280
    RTable = image.load(r'img\menu\ChooseSet\RankTable.png')
    RCar=[Car[0].img, Car[1].img, Car[2].img, Car[3].img, Car[4].img]
    for x in range(5):
        RCar[x] = pygame.transform.scale(RCar[x], (40, 25))
    screen.blit(RTable, (1, 1))
    if Car[ChooseCar - 1].Rank == 0 and StageCount <= Race + 1:
        if CheckScreen==1:
            draw_text(Player.username, font, (255, 255, 255), screen, Car[ChooseCar - 1].x + 50, Car[ChooseCar - 1].y + 20)
    for x in range(5):
        for y in range(5):
            if Rankx[x] == Car[y].x:
                Car[y].RankIns = x
                screen.blit(RCar[y], (xrank, 120))
                xrank -= 65

def FinalRankTable(Car, ChooseCar, StageCount, Race, CheckScreen):
    global Player
    Rankx=[1, 2, 3, 4, 5, 6]
    for i in range(6):
        Rankx[i]=Car[i].x
    Rankx = sorted(Rankx)
    xrank = 303
    RTable = image.load(r'img\menu\ChooseSet\FinalRankTable.png')
    RCar = [Car[0].img, Car[1].img, Car[2].img, Car[3].img, Car[4].img, Car[5].img]
    for x in range(6):
        RCar[x] = pygame.transform.scale(RCar[x], (40, 25))
    screen.blit(RTable, (1, 1))
    if Car[ChooseCar - 1].Rank == 0 and StageCount <= Race + 1:
        if CheckScreen == 1:
            draw_text(Player.username, font, (255, 255, 255), screen, Car[ChooseCar - 1].x + 30, Car[ChooseCar - 1].y + 20)
    for x in range(6):
        for y in range(6):
            if Rankx[x] == Car[y].x:
                Car[y].RankIns = x
                screen.blit(RCar[y], (xrank, 120))
                xrank -= 55

def playFinal(Set, Race, ChooseCar):
    global Player, music
    inraceSound.play()
    inraceSound.set_volume(music)
    #Delete existed folder named 'Ready'
    Path = os.path.join(os.getcwd(), 'img', 'menu', 'ChooseSet', 'Ready')
    if os.path.exists(Path):
        DeleteFiles(Path)
    if os.path.exists(Path):
        os.rmdir(Path)
    #Create Folder 'Ready'
    #ReadyPath=os.path.join(os.getcwd(),'img','menu','ChooseSet','Ready')
    #if os.path.exists(ReadyPath)==False:
    #	os.mkdir(ReadyPath)
    OldPath = os.path.join(os.getcwd(), 'img', 'menu',  'ChooseSet', 'set5')
    NewPath = os.path.join(os.getcwd(), 'img', 'menu', 'ChooseSet', 'Ready')
    files = os.listdir(OldPath)
    shutil.copytree(OldPath, NewPath)
    Carwidth = 60
    #Create variable
    xBg = 0
    yC = [190, 260, 333, 404, 480, 547]
    Car = [CCar, CCar, CCar, CCar, CCar, CCar]
    clicked = False
    StageCount = 0
    ItemTable = image.load(r'img\menu\ChooseSet\ItemList.png')
    ItemTable = pygame.transform.scale(ItemTable, (445, 95))
    rand = [1, 2, 3, 4, 5, 6]		#random position of Rock
    CheckCollide = [0, 0, 0, 0, 0, 0]		#Collide with Rock?
    CheckScreen=1
    RankCount = 1
    Checkbetmoney = False #check for change of money when win/lose
    #Create
    BackGroundStart = image.load(r'img\menu\ChooseSet\Ready\Begin.png')
    BackGroundP = image.load(r'img\menu\ChooseSet\Ready\Default.png')
    BackGroundStage = image.load(r'img\menu\ChooseSet\Ready\Stage.png')
    BackGroundEnd = image.load(r'img\menu\ChooseSet\Ready\End.png')
    for x in range(6):
        Path = os.path.join(os.getcwd(), 'img', 'menu', 'ChooseSet', 'Ready', str(x + 1) + '.png')
        pic = image.load(Path)
        Car[x] = CCar(pic, 10, yC[x], Carwidth, 0, 0)

    def FirstScreen():
        if StageCount < Race:
            Draw.DrawBG3(BackGroundP, BackGroundStage, BackGroundP, xBg)

    def SecondScreen():
        screen.blit(BackGroundEnd,(0,0))
        for i in range(6):
            if Car[i].Rank != 0:
                Draw.DrawCar(Car[i],0,0)
    #For Effect
    Tick = pygame.image.load(r'img\menu\ChooseSet\Effect\Tick.png')
    Tick = pygame.transform.scale(Tick, (20, 20))
    ASpeedUp = pygame.Rect(31, 590, 46, 46)
    AErase = pygame.Rect(113, 640, 46, 46)
    AWeak = pygame.Rect(195, 640, 46, 46)
    AFlash = pygame.Rect(277, 640, 46, 46)
    ARestart = pygame.Rect(357, 640, 46, 46)
    if Player.numItem == 1:
        ATick = (67, 675)
    if Player.numItem == 2:
        ATick = (147, 675)
    if Player.numItem == 3:
        ATick = (229, 675)
    if Player.numItem == 4:
        ATick = (312, 675)
    if Player.numItem == 5:
        ATick = (393, 675)
    #GameLoop
    while True:
        if RankCount == 6:
            StageCount = Race + 1
        if StageCount == 0:
            Draw.DrawBG2(BackGroundStart, BackGroundP, xBg)
            for i in range(6):
                Draw.DrawCar(Car[i], 1, 0)
        if StageCount == Race:
            Draw.DrawBG3(BackGroundP, BackGroundP, BackGroundEnd, xBg)
        if CheckScreen==1:
            FirstScreen()
        if CheckScreen==2:
            SecondScreen()
        if StageCount == Race + 1:
            screen.blit(BackGroundEnd, (0, 0))
            for i in range(6):
                Draw.DrawCar(Car[i], 1, 0)
            for x in range(6):
                if Car[x].x + Car[x].width > 755 and Car[x].x + Car[x].width < 950:
                    Car[x].x = 950
                    Car[x].Rank = RankCount
                    RankCount += 1
                    if RankCount == 7:
                        betmoney = ""
                        if Car[ChooseCar - 1].Rank == 1 and Checkbetmoney == False:
                            Player.money += Player.bet
                            betmoney = "+" + str(Player.bet)
                            Player.bet = 0
                            WinCheck = True
                            Checkbetmoney = True
                        elif Checkbetmoney == False:
                            Player.money -= Player.bet
                            betmoney = "-" + str(Player.bet)
                            Player.bet = 0
                            WinCheck = False
                            Checkbetmoney = True
                        Player.numRace += 1
                        Save()
                        saveBet(betmoney)
                        inraceSound.stop()
                        ShowFinalResult(Car, WinCheck)
        #DrawRock and check collide
        RankCount = Draw.DrawRock(Car, RankCount, rand, CheckCollide, CheckScreen)
        for i in range(6):
            Draw.Update(Car[i])
        for i in range(6):
            if Car[i].Rank == 0:
                Draw.DrawCar(Car[i], 0, 0)
        for i in range(6):
            if Car[i].Rank == 1:
                yCheer = Car[i].y
        #Draw item table & rank table
        screen.blit(ItemTable, (1, 625))
        if Player.numItem != 0:
             screen.blit(Tick, ATick)
        FinalRankTable(Car, ChooseCar, StageCount, Race,CheckScreen)
        xBg -= 10
        #Count Stages
        if StageCount == 0:
            if xBg <- 1080:
                xBg = 0
                StageCount += 1
        elif StageCount < Race + 1:
            if xBg <- 1080 * 2:
                xBg = 0
                StageCount += 1
                for i in range(6):
                    rand[i] = random.randint(600, 900)
                    CheckCollide[i] = 0
        dx, dy = pygame.mouse.get_pos()
        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouseClick.play()
                    mouseClick.set_volume(music)
                    clicked = True
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_LEFT:
                    CheckScreen = 1
                if event.key==pygame.K_RIGHT:
                    CheckScreen = 2
        if ASpeedUp.collidepoint(dx, dy):
            pygame.draw.rect(screen, (0, 255, 0), ASpeedUp, 3)
            if clicked:
                if Player.numItem == 1 and Player.countItem == 1:
                    item1.play()
                    item1.set_volume(music)
                    Car[ChooseCar-1].speedup = True
                    Player.numItem = 0
                    Player.countItem -= 1
        if AErase.collidepoint(dx, dy):
            pygame.draw.rect(screen, (0, 255, 0), AErase, 3)
            if clicked:
                if Player.numItem == 2 and Player.countItem == 1:
                    item2.play()
                    item2.set_volume(music)
                    CheckCollide[ChooseCar - 1] += 2
                    Player.numItem = 0
                    Player.countItem -= 1
        if AWeak.collidepoint(dx, dy):
            pygame.draw.rect(screen, (0, 255, 0), AWeak, 3)
            if clicked:
                if Player.numItem == 3 and Player.countItem == 1:
                    item3.play()
                    item3.set_volume(music)
                    Draw.DrawWeak(5, Car, ChooseCar - 1)
                    Player.numItem = 0
                    Player.countItem -= 1
        if AFlash.collidepoint(dx, dy):
            pygame.draw.rect(screen, (0, 255, 0), AFlash, 3)
            if clicked:
                if Player.numItem == 4 and Player.countItem == 1:
                    item4.play()
                    item4.set_volume(music)
                    Player.numItem = 0
                    Car[ChooseCar - 1].x += 50
                    Player.countItem -= 1
        if ARestart.collidepoint(dx, dy):
            pygame.draw.rect(screen, (0, 255, 0), ARestart, 3)
            if clicked:
                if Player.numItem == 5 and Player.countItem == 1:
                    item5.play()
                    item5.set_volume(music)
                    Player.numItem = 0
                    Player.countItem -= 1
                    playFinal(Set, Race, ChooseCar)
        if StageCount == Race + 1:
            Draw.DrawCheer(Car, ChooseCar - 1)
        pygame.display.update()

def playGame(Set, Race, ChooseCar):
    global Player, music
    inraceSound.play()
    inraceSound.set_volume(music)
    #Delete existed folder named 'Ready'
    Path = os.path.join(os.getcwd(), 'img', 'menu', 'ChooseSet', 'Ready')
    if os.path.exists(Path):
        DeleteFiles(Path)
    if os.path.exists(Path):
        os.rmdir(Path)
    #Create Folder 'Ready'
    #ReadyPath=os.path.join(os.getcwd(),'img','menu','ChooseSet','Ready')
    #if os.path.exists(ReadyPath)==False:
    #	os.mkdir(ReadyPath)
    if Set == 1:
        OldPath = os.path.join(os.getcwd(), 'img', 'menu', 'ChooseSet', 'set1')
        NewPath = os.path.join(os.getcwd(), 'img', 'menu', 'ChooseSet', 'Ready')
        files = os.listdir(OldPath)
        shutil.copytree(OldPath, NewPath)
        Carwidth = 132
    if Set == 2:
        OldPath = os.path.join(os.getcwd(), 'img', 'menu', 'ChooseSet', 'set2')
        NewPath = os.path.join(os.getcwd(), 'img', 'menu', 'ChooseSet', 'Ready')
        files = os.listdir(OldPath)
        shutil.copytree(OldPath, NewPath)
        Carwidth = 132
    if Set == 3:
        OldPath = os.path.join(os.getcwd(), 'img', 'menu', 'ChooseSet', 'set3')
        NewPath = os.path.join(os.getcwd(), 'img', 'menu', 'ChooseSet', 'Ready')
        files = os.listdir(OldPath)
        shutil.copytree(OldPath, NewPath)
        Carwidth = 132
    if Set == 4:
        OldPath = os.path.join(os.getcwd(), 'img', 'menu', 'ChooseSet', 'set4')
        NewPath = os.path.join(os.getcwd(), 'img', 'menu', 'ChooseSet', 'Ready')
        files = os.listdir(OldPath)
        shutil.copytree(OldPath, NewPath)
        Carwidth = 10
    #Create variable
    xBg = 0
    yC = [170, 260, 333, 410, 475]
    Car = [CCar, CCar, CCar, CCar, CCar]
    clicked = False
    StageCount = 0
    ItemTable = image.load(r'img\menu\ChooseSet\ItemList.png')
    rand = [1, 2, 3, 4, 5]				#random position of Rock
    CheckCollide = [0, 0, 0, 0, 0]		#Collide with Rock?
    CheckScreen = 1                     #Screen 1 or 2
    RankCount = 1
    Checkbetmoney = False  #check for change of money when win/lose
    #Create
    BackGroundStart = image.load(r'img\menu\ChooseSet\Ready\Begin.png')
    BackGroundP = image.load(r'img\menu\ChooseSet\Ready\Default.png')
    BackGroundStage = image.load(r'img\menu\ChooseSet\Ready\Stage.png')
    BackGroundEnd = image.load(r'img\menu\ChooseSet\Ready\End.png')
    for x in range(5):
        Path = os.path.join(os.getcwd(), 'img', 'menu', 'ChooseSet', 'Ready', str(x + 1) + '.png')
        pic = image.load(Path)
        Car[x] = CCar(pic, 10, yC[x], Carwidth, 0, 0)
    def FirstScreen():
        if StageCount < Race:
            Draw.DrawBG3(BackGroundP, BackGroundStage, BackGroundP, xBg)

    def SecondScreen():
        screen.blit(BackGroundEnd,(0,0))
        for i in range(5):
            if Car[i].Rank != 0:
                Draw.DrawCar(Car[i],0,0)

    #For Effect
    Tick = pygame.image.load(r'img\menu\ChooseSet\Effect\Tick.png')
    ASpeedUp = pygame.Rect(53, 590, 75, 75)
    AErase = pygame.Rect(190, 590, 75, 75)
    AWeak = pygame.Rect(328, 590, 75, 75)
    AFlash = pygame.Rect(467, 590, 75, 75)
    ARestart = pygame.Rect(604, 590, 75, 75)
    if Player.numItem == 1:
        ATick = (113, 645)
    if Player.numItem == 2:
        ATick = (249, 645)
    if Player.numItem == 3:
        ATick = (386, 645)
    if Player.numItem == 4:
        ATick = (527, 645)
    if Player.numItem == 5:
        ATick = (663, 645)
    #GameLoop
    while True:
        if RankCount == 5:
            StageCount = Race + 1
        if StageCount == 0:
            Draw.DrawBG2(BackGroundStart, BackGroundP, xBg)
            for i in range(5):
                Draw.DrawCar(Car[i], 1, 0)
        if StageCount == Race:
            if xBg>-2100:
                CheckScreen==1
            Draw.DrawBG3(BackGroundP, BackGroundP, BackGroundEnd, xBg)
        if CheckScreen==1:
            FirstScreen()
        if CheckScreen==2:
            SecondScreen()
        if StageCount == Race + 1:
            screen.blit(BackGroundEnd, (0, 0))
            for i in range(5):
                Draw.DrawCar(Car[i], 1, 0)                                           #ShowCar
            for x in range(5):
                if Car[x].x + Car[x].width > 755 and Car[x].x + Car[x].width < 950:
                    Car[x].x = 950
                    Car[x].Rank = RankCount
                    RankCount += 1
                    if RankCount == 6:
                        betmoney = ""
                        if Car[ChooseCar - 1].Rank == 1 and Checkbetmoney == False:
                            Player.money += Player.bet
                            betmoney = "+" + str(Player.bet)
                            Player.bet = 0
                            WinCheck = True
                            Checkbetmoney = True
                        elif Checkbetmoney == False:
                            Player.money -= Player.bet
                            betmoney = "-" + str(Player.bet)
                            Player.bet = 0
                            WinCheck = False
                            Checkbetmoney = True
                        Player.numRace += 1
                        Save()
                        saveBet(betmoney)
                        inraceSound.stop()
                        ShowResult(Car, WinCheck)
        #DrawRock and check collide
        RankCount = Draw.DrawRock(Car, RankCount, rand, CheckCollide, CheckScreen)
        for i in range(5):
            Draw.Update(Car[i])
        for i in range(5):
            if Car[i].Rank == 0:
                if CheckScreen == 1:
                    Draw.DrawCar(Car[i], 0, 0)
        for i in range(5):
            if Car[i].Rank == 1:
                yCheer = Car[i].y
        #Draw item table & rank table
        screen.blit(ItemTable, (1, 560))
        if Player.numItem != 0:
             screen.blit(Tick, ATick)
        RankTable(Car, ChooseCar, StageCount, Race,CheckScreen)
        xBg -= 10
        #Count Stages
        if StageCount == 0:
            if xBg <- 1080:
                xBg = 0
                StageCount += 1
        elif StageCount < Race + 1:
            if xBg <- 1080 * 2:
                xBg = 0
                StageCount += 1
                for i in range(5):
                    rand[i] = random.randint(600, 900)
                    CheckCollide[i] = 0
        dx, dy = pygame.mouse.get_pos()
        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouseClick.play()
                    mouseClick.set_volume(music)
                    clicked = True
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_LEFT:
                    CheckScreen = 1
                if event.key==pygame.K_RIGHT:
                    CheckScreen = 2
        if ASpeedUp.collidepoint(dx, dy):
            pygame.draw.rect(screen, (0, 255, 0), ASpeedUp, 3)
            if clicked:
                if Player.numItem == 1 and Player.countItem == 1:
                    item1.play()
                    item1.set_volume(music)
                    Car[ChooseCar - 1].speedup = True
                    Player.numItem = 0
                    Player.countItem -= 1
        if AErase.collidepoint(dx, dy):
            pygame.draw.rect(screen, (0, 255, 0), AErase, 3)
            if clicked:
                if Player.numItem == 2 and Player.countItem == 1:
                    item3.play()
                    item3.set_volume(music)
                    CheckCollide[ChooseCar - 1] += 2
                    Player.numItem = 0
                    Player.countItem -= 1
        if AWeak.collidepoint(dx, dy):
            pygame.draw.rect(screen, (0, 255, 0), AWeak, 3)
            if clicked:
                if Player.numItem == 3 and Player.countItem == 1:
                    item2.play()
                    item2.set_volume(music)
                    Draw.DrawWeak(Set, Car, ChooseCar - 1)
                    Player.numItem = 0
                    Player.countItem -= 1
        if AFlash.collidepoint(dx, dy):
            pygame.draw.rect(screen, (0, 255, 0), AFlash, 3)
            if clicked:
                if Player.numItem == 4 and Player.countItem == 1:
                    item4.play()
                    item4.set_volume(music)
                    Player.numItem = 0
                    Car[ChooseCar-1].x += 50
                    Player.countItem -= 1
        if ARestart.collidepoint(dx, dy):
            pygame.draw.rect(screen, (0, 255, 0), ARestart, 3)
            if clicked:
                if Player.numItem == 5 and Player.countItem == 1:
                    item4.play()
                    item4.set_volume(music)
                    Player.numItem = 0
                    Player.countItem -= 1
                    playGame(Set, Race, ChooseCar)
        if StageCount == Race + 1:
            Draw.DrawCheer(Car, ChooseCar - 1)
        pygame.display.update()

def settingScreenMenu(username):
    global music, language
    running = True; clicked = False
    status = None
    pushFaceIDButton = False
    ingameSound.play()
    ingameSound.set_volume(music)
    while running:
        settingscreen = pygame.image.load(r'img\menu\settingscreen\{}.png'.format(language))
        DISPLAYSURFACE.blit(settingscreen, (0, 0))
        language0Button = pygame.Rect(674, 356, 61, 40)
        language1Button = pygame.Rect(557, 357, 60, 40)
        onButton = pygame.Rect(545, 243, 80, 80)
        offButton = pygame.Rect(660, 243, 80, 80)
        FaceIDButton = pygame.Rect(295, 432, 480, 68)
        exitButton = pygame.Rect(921, 70, 90, 90)

        dx, dy = pygame.mouse.get_pos()

        if language0Button.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), language0Button, 3)
            if clicked:
                language = 0
                status = None
                pushFaceIDButton = False
        if language1Button.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), language1Button, 3)
            if clicked:
                language = 1
                status = None
                pushFaceIDButton = False
        if exitButton.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), exitButton, 3, 25)
            if clicked:
                running = False
                ingameSound.stop()
                pushFaceIDButton = False
        if onButton.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), onButton, 3, 360)
            if clicked:
                music = 1
                ingameSound.play()
                pushFaceIDButton = False
                status = None
        if offButton.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), offButton, 3, 360)
            if clicked:
                music = 0
                ingameSound.stop()
                pushFaceIDButton = False
                status = None
        if FaceIDButton.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), FaceIDButton, 3, 30)
            if clicked:
                pushFaceIDButton = True
                status = None

        clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouseClick.play()
                    mouseClick.set_volume(music)
                    clicked = True
        if pushFaceIDButton:
            video = cv2.VideoCapture(0)
            faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            count = 0
            path = 'faceid/' + username
            isExist = os.path.exists(path)

            if not isExist:
                os.makedirs(path)
                while True:
                    ret, frame = video.read()
                    faces = faceDetect.detectMultiScale(frame, 1.3, 5)
                    count1 = 0
                    for x, y, w, h in faces:
                        count1 += 1
                        count += 1
                        name = './faceid/' + username + '/' + str(count) + '.jpg'
                        cv2.imwrite(name, frame[y : y + h, x : x + w])
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                    cv2.imshow('Face ID', frame)
                    cv2.waitKey(1)
                    if count1 > 1:
                        status = 1
                        break
                    if count > 39:
                        break
            else:
                status = 0
            video.release()
            cv2.destroyAllWindows()
            pushFaceIDButton = False
        if status == 0:
            if language == 0:
                draw_text('YOU HAVE SETUP FACE ID BEFORE!', bigFont, (0, 0, 0), DISPLAYSURFACE, 397, 520)
            else:
                draw_text('BẠN ĐÃ THIẾT LẬP FACE ID!', bigFont, (0, 0, 0), DISPLAYSURFACE, 405, 520)
        elif status == 1:
            if os.path.exists('faceid/' + username):
                DeleteFiles('faceid/' + username)
                os.rmdir('faceid/' + username)
            if language == 0:
                draw_text('SETUP FACE ID UNSUCCESSFUL!', bigFont, (0, 0, 0), DISPLAYSURFACE, 405, 520)
            else:
                draw_text('KHÔNG THÀNH CÔNG!', bigFont, (0, 0, 0), DISPLAYSURFACE, 428, 520)
        pygame.display.update()
        fpsClock.tick(FPS)

def helpScreen(index):
    global language, music
    running = True
    clicked = False
    ingameSound.play()
    ingameSound.set_volume(music)
    while running:
        help = pygame.image.load(r'img\menu\helpscreen\{}\{}.png'.format(language, index))
        DISPLAYSURFACE.blit(help, (0, 0))
        exitButton = pygame.Rect(920, 70, 90, 90)
        prevButton = pygame.Rect(943, 608, 42, 40)
        nextButton = pygame.Rect(987, 608, 42, 40)

        dx, dy = pygame.mouse.get_pos()
        if exitButton.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), exitButton, 3, 25)
            if clicked:
                ingameSound.stop()
                running = False
        if prevButton.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), prevButton, 3, 100)
            if clicked:
                if index > 1:
                    index -= 1
        if nextButton.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), nextButton, 3, 100)
            if clicked:
                if index < 9:
                    index += 1

        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                if event.key == K_RIGHT:
                    if index < 9:
                        index += 1
                if event.key == K_LEFT:
                    if index > 1:
                        index -= 1
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouseClick.play()
                    mouseClick.set_volume(music)
                    clicked = True
        fpsClock.tick(FPS)
        pygame.display.update()

def shopScreen(lSite):
    global music, language, Player
    clicked = False; running = True
    status = None
    ingameSound.play()
    ingameSound.set_volume(music)
    while running:
        shopscreen = pygame.image.load(r'img\menu\shopscreen.png')
        DISPLAYSURFACE.blit(shopscreen, (0, 0))
        item1 = pygame.Rect(96, 308, 115, 105)
        item2 = pygame.Rect(289, 308, 115, 105)
        item3 = pygame.Rect(484, 308, 115, 105)
        item4 = pygame.Rect(675, 308, 115, 105)
        item5 = pygame.Rect(871, 308, 116, 105)
        exitButton = pygame.Rect(922, 71, 88, 87)
        draw_text(str(Player.money), bigFont, coinColor, DISPLAYSURFACE, 833, 222)
        if language == 0:
            draw_text("You are having " + str(Player.countItem) + " item", bigFont, coinColor, DISPLAYSURFACE, 165, 221)
        else:
            draw_text("Bạn đang có " + str(Player.countItem) + " vật phẩm", bigFont, coinColor, DISPLAYSURFACE, 165, 221)
        dx, dy = pygame.mouse.get_pos()

        if item1.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), item1, 3)
            if clicked:
                status = None
                if Player.countItem < 1:
                    if Player.money < 100:
                        status = 0
                    else:
                        Player.numItem = 1
                        Player.countItem += 1
                        Player.money -= 100
                else:
                    status = -1
        if item2.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), item2, 3)
            if clicked:
                status = None
                if Player.countItem < 1:
                    if Player.money < 200:
                        status = 0
                    else:
                        Player.numItem = 3
                        Player.countItem += 1
                        Player.money -= 200
                else:
                    status = -1
        if item3.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), item3, 3)
            if clicked:
                status = None
                if Player.countItem < 1:
                    if Player.money < 300:
                        status = 0
                    else:
                        Player.numItem = 2
                        Player.countItem += 1
                        Player.money -= 300
                else:
                    status = -1
        if item4.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), item4, 3)
            if clicked:
                status = None
                if Player.countItem < 1:
                    if Player.money < 400:
                        status = 0
                    else:
                        Player.numItem = 4
                        Player.countItem += 1
                        Player.money -= 400
                else:
                    status = -1
        if item5.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), item5, 3)
            if clicked:
                status = None
                if Player.countItem < 1:
                    if Player.money < 500:
                        Player.status = 0
                    else:
                        Player.numItem = 5
                        Player.countItem += 1
                        Player.money -= 500
                else:
                    status = -1
        if exitButton.collidepoint(dx, dy):
            status = None
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), exitButton, 3, 15)
            if clicked:
                ingameSound.stop()
                running = False

        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouseClick.play()
                    mouseClick.set_volume(music)
                    clicked = True
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        if status == 0:
            if language == 0:
                draw_text("You don't have enough money", bigFont, (0, 0, 0), DISPLAYSURFACE, 400, 600)
            else:
                draw_text("Bạn không có đủ tiền", bigFont, (0, 0, 0), DISPLAYSURFACE, 440, 600)
        elif status == -1:
            if language == 0:
                draw_text("You can only buy at most one item", bigFont, (0, 0, 0), DISPLAYSURFACE, 380, 600)
            else:
                draw_text("Bạn chỉ được mua tối đa 1 vật phẩm", bigFont, (0, 0, 0), DISPLAYSURFACE, 390, 600)
        fpsClock.tick(FPS)
        pygame.display.update()
    buyItem(Player.lSite)
    return Player.money

def ShowResult(Car, WinCheck):
    global language, Player, music
    pygame.display.set_caption('Leadership')
    icon = pygame.image.load(r'img\Results\car.png')
    bg = pygame.image.load(r'img\Results\result\{}.png'.format(language))
    def save_data():
        file_name = "Rank.txt"
        with open(file_name, "w") as file:
            if language:
                file.write("BANG XEP HANG\n")
                for i in range(5):
                    for j in range(5):
                        if Car[j].Rank == i + 1:
                            file.write("Hang " + str(i + 1) + ":     Xe " + str(j + 1) + "\n")

                if WinCheck:
                    file.write("BAN THANG\n")
                    clapSound.play()
                    clapSound.set_volume(music)
                else :
                    file.write("BAN THUA\n")
            else:
                file.write("RANKING RESULT\n")
                for i in range(5):
                    for j in range(5):
                        if Car[j].Rank == i + 1:
                            file.write("Rank " + str(i + 1) + ":     Car " + str(j + 1) + "\n")
                if WinCheck:
                    file.write("YOU WIN\n")
                    clapSound.play()
                    clapSound.set_volume(music)
                else:
                    file.write("YOU LOSE\n")
            file.close()
        #print(f"da luu file {file_name} thanh cong")
    def save_file():
        shutil.copyfile('Rank.txt', 'Game_'+str(Player.numRace)+'.txt')
        shutil.copyfile('screenshot.png', 'Game_'+str(Player.numRace)+'.png')
        Player_Path = os.path.join(os.getcwd(), 'History', str(Player.username), 'Game_' + str(Player.numRace)+'.txt')
        shutil.move(os.path.join(os.getcwd(), 'Game_' + str(Player.numRace)+'.txt'), Player_Path)
        Player_Path = os.path.join(os.getcwd(), 'History', str(Player.username), 'Game_' + str(Player.numRace)+'.png')
        shutil.move(os.path.join(os.getcwd(), 'Game_' + str(Player.numRace)+'.png'), Player_Path)
    pygame.display.set_icon(icon)
    screen = pygame.display.set_mode((640, 640))
    image_sprite = [pygame.image.load("img\Results\Firework_1.png"), pygame.image.load("img\Results\Firework_2.png"),pygame.image.load("img\Results\Firework_3.png"), pygame.image.load("img\Results\Firework_4.png")]
    clock = pygame.time.Clock()
    value = 0
    running = True
    count = 0
    Win = pygame.image.load(r'img\race\celebrate\youwin.png')
    Lose = pygame.image.load(r'img\race\celebrate\youlose.png')
    while running:
        screen.blit(bg, (0, 0))
        clock.tick(8)
        if value >= len(image_sprite):
            value = 0

        image = image_sprite[value]
        x = 0
        y = -30
        screen.blit(image, (x, y)) # sửa window thành screen

        clock.tick(8)
        if value >= len(image_sprite):
            value = 0

        image = image_sprite[value]
        x = 430
        y = -30
        screen.blit(image, (x, y)) # sửa window thành screen
        pygame.display.update()
        yRTable = [160, 235, 305, 375, 440]
        for i in range(5):
            for j in range(5):
                if Car[j].Rank == i + 1:
                    screen.blit(Car[j].img, (300, yRTable[i]))
        if WinCheck:
            screen.blit(Win, (465, 540))
        else:
            screen.blit(Lose, (465, 540))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    clapSound.stop()
                    # Save()
                    save_data()
                    mainMenu()
                if event.key == K_RETURN:
                    pygame.image.save(screen, 'screenshot.png')
                    save_data()
                    save_file()
        pygame.display.update()
        value += 1
        if value == 4:
            # Lưu ảnh vào file
            pygame.image.save(screen, 'screenshot.png')
            save_data()
        pygame.display.update()
    save_file()

def ShowFinalResult(Car, WinCheck):
    global language, Player
    pygame.display.set_caption('Leadership')
    icon = pygame.image.load(r'img\Results\car.png')
    bg = pygame.image.load(r'img\Results\resultfinal\{}.png'.format(language))

    def save_data():
        file_name = "Rank.txt"
        with open(file_name,"w") as file:
            if language:
                file.write("BANG XEP HANG\n")
                for i in range(6):
                    for j in range(6):
                        if Car[j].Rank == i + 1:
                            file.write("Hang " + str(i + 1) + ":     Xe " + str(j + 1) + "\n")
                if WinCheck:
                    file.write("BAN THANG\n")
                else:
                    file.write("BAN THUA\n")
            else:
                file.write("RANKING RESULT\n")
                for i in range(6):
                    for j in range(6):
                        if Car[j].Rank == i + 1:
                            file.write("Rank " + str(i + 1) + ":     Car " + str(j + 1) + "\n")
                if WinCheck:
                    file.write("YOU WIN\n")
                else:
                    file.write("YOU LOSE\n")
            file.close()
    def save_file():
        shutil.copyfile('Rank.txt', 'Game_'+str(Player.numRace)+'.txt')
        shutil.copyfile('screenshot.png', 'Game_'+str(Player.numRace)+'.png')
        Player_Path = os.path.join(os.getcwd(), 'History', str(Player.username), 'Game_' + str(Player.numRace)+'.txt')
        shutil.move(os.path.join(os.getcwd(), 'Game_' + str(Player.numRace)+'.txt'), Player_Path)
        Player_Path = os.path.join(os.getcwd(), 'History', str(Player.username), 'Game_' + str(Player.numRace)+'.png')
        shutil.move(os.path.join(os.getcwd(), 'Game_' + str(Player.numRace)+'.png'), Player_Path)
    pygame.display.set_icon(icon)
    screen = pygame.display.set_mode((640, 716))
    image_sprite = [pygame.image.load("img\Results\Firework_1.png"), pygame.image.load("img\Results\Firework_2.png"), pygame.image.load("img\Results\Firework_3.png"), pygame.image.load("img\Results\Firework_4.png")]
    clock = pygame.time.Clock()
    value = 0
    running = True
    Win = pygame.image.load(r'img\race\celebrate\youwin.png')
    Lose = pygame.image.load(r'img\race\celebrate\youlose.png')
    while running:
        screen.blit(bg, (0, 0))
        clock.tick(8)
        if value >= len(image_sprite):
            value = 0
        image = image_sprite[value]
        x = 0
        y = -30
        screen.blit(image, (x, y))
        clock.tick(8)
        if value >= len(image_sprite):
            value = 0
        image = image_sprite[value]
        x = 430
        y = -30
        screen.blit(image, (x, y))
        pygame.display.update()
        yRTable = [149, 221, 294, 364, 435, 506]
        for i in range(6):
            for j in range(6):
                if Car[j].Rank == i + 1:
                    screen.blit(Car[j].img, (300, yRTable[i]))
        if WinCheck:
            screen.blit(Win, (465, 625))
        else:
            screen.blit(Lose, (465, 625))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    Save()
                    save_data()
                    mainMenu()
                if event.key== K_RETURN:
                    save_data()
                    save_file()
        pygame.display.update()
        value += 1
        if value == 4:
            # Lưu ảnh vào file
            pygame.image.save(screen, 'screenshot.png')
        pygame.display.update()

def miniGameScreen(money):
    global language
    screen = pygame.display.set_mode(WINDOWSIZE)

    bg = pygame.image.load(r"img/minigame/assets/background.jpg")
    tree = pygame.image.load(r"img/minigame/assets/tree.png")
    dino = pygame.image.load(r"img/minigame/assets/dinosaur.png")

    sound1 = pygame.mixer.Sound(r"img/minigame/sound/tick.wav")
    sound2 = pygame.mixer.Sound(r"img/minigame/sound/te.wav")
    game_font = pygame.font.Font('04B_19.TTF', 20)

    bg_x, bg_y = 0, 0
    tree_x, tree_y = 900, 600
    dino_x, dino_y = 15, 600
    x_def, y_def = 6, 7
    jump = False
    currentScore = 0
    highScore = 0
    score = 0
    GamePLay = False
    checkMoney=False
    CurrentMoney=0
    def obstacles():
        if dino_hcn.colliderect(tree_hcn):
            pygame.mixer.Sound.play(sound2)
            return False
        return True

    def score_view():
        if GamePLay:
            score_txt = game_font.render(f'Score: {int(score)}', True, (255, 0, 0))
            screen.blit(score_txt, (500, 50))
            highScore_txt = game_font.render(f'High score: {int(score)}', True, (255, 0, 0))
            screen.blit(highScore_txt, (500, 80))
        else:
            if status == 1:
                score_txt = game_font.render(f'score: {int(score)}', True, (255, 0, 0))
                screen.blit(score_txt, (500, 50))
                highScore_txt = game_font.render(f'High score: {int(highScore)}', True, (255, 0, 0))
                screen.blit(highScore_txt, (500, 80))
                gameover_txt = game_font.render(f'Gameover', True, (255, 0, 0))
                screen.blit(gameover_txt, (500, 130))

    running = True
    status = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_SPACE and GamePLay:
                    if dino_y == 600:
                        jump = True
                        pygame.mixer.Sound.play(sound1)
                if event.key == K_SPACE and GamePLay == False:
                    if money < 200 and CurrentMoney < 200:
                        GamePLay = True
                        checkMoney=False
                        status = 1
                    else:
                        status = 0
        if GamePLay:
            bg_hcn = screen.blit(bg, (bg_x, bg_y))
            bg2_hcn = screen.blit(bg, (bg_x + 1080, bg_y))
            bg_x -= x_def
            if bg_x == -1080: bg_x = 0

            tree_hcn = screen.blit(tree, (tree_x, tree_y))
            tree_x -= 7
            if tree_x == -10: tree_x = 900

            dino_hcn = screen.blit(dino, (dino_x, dino_y))
            if dino_y >= 430 and jump == True:
                dino_y -= y_def
            else:
                jump = False
            if dino_y < 600 and jump == False:
                dino_y += y_def
            score += 0.1
            if highScore < score:
                highScore = score
            currentScore = score
            GamePLay = obstacles()
            score_view()
        else:
            #reset game
            bg_x, bg_y = 0, 0
            tree_x, tree_y = 900, 600
            dino_x, dino_y = 15, 600
            if checkMoney == False:
                CurrentMoney += int(currentScore)
                checkMoney=True
            score = 0

            bg_hcn = screen.blit(bg, (bg_x, bg_y))
            tree_hcn = screen.blit(tree, (tree_x, tree_y))
            dino_hcn = screen.blit(dino, (dino_x, dino_y))
            score_view()
        if status == 0:
            if language == 0:
                draw_text("You can't play minigame when your money is more than 200", pygame.font.SysFont('Asap', 30, bold = True, italic = False), (0, 0, 0), screen, 150, 300)
            else:
                draw_text("Bạn không thể chơi minigame khi số tiền lớn hơn 200", pygame.font.SysFont('Asap', 30, bold = True, italic = False), (0, 0, 0), screen, 150, 300)
        fpsClock.tick(FPS)
        pygame.display.update()
    money += CurrentMoney
    return int(money)

def history(lSite):
    global language, music
    running = True; clicked = False
    numRace = int(data.iloc[lSite, 7])
    list = data.iloc[lSite, 9:(numRace + 9)]
    start = 0
    ingameSound.play()
    ingameSound.set_volume(music)
    while running:
        historyscreen = pygame.image.load(r'img\menu\historyscreen\{}.png'.format(language))
        DISPLAYSURFACE.blit(historyscreen, (0, 0))
        exitButton = pygame.Rect(921, 70, 90, 90)
        if numRace > 5:
            start = numRace - 5
        else:
            start = 0
        if numRace == 0:
            if language == 0:
                draw_text("You haven't played any matches yet!", pygame.font.SysFont('Asap', 30, bold = True, italic = False), (0, 0, 0), DISPLAYSURFACE, 320, 300)
            else:
                draw_text("Bạn chưa chơi trận nào!", pygame.font.SysFont('Asap', 30, bold = True, italic = False), (0, 0, 0), DISPLAYSURFACE, 380, 300)
        else:
            if language == 0:
                for i in range (start, numRace):
                    draw_text("Game " + str(i + 1) + ":         " + str(list[i]), pygame.font.SysFont('Asap', 35, bold = True, italic = False), (0, 0, 0), DISPLAYSURFACE, 420, (i - start) * 70 + 280)
            else:
                for i in range (start, numRace):
                    draw_text("Trận " + str(i + 1) + ":         " + str(list[i]), pygame.font.SysFont('Asap', 35, bold = True, italic = False), (0, 0, 0), DISPLAYSURFACE, 420, (i - start) * 70 + 280)

        dx, dy = pygame.mouse.get_pos()

        if exitButton.collidepoint(dx, dy):
            pygame.draw.rect(DISPLAYSURFACE, (0, 255, 0), exitButton, 3, 25)
            if clicked:
                running = False
                ingameSound.stop()

        clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouseClick.play()
                    mouseClick.set_volume(music)
                    clicked = True
        pygame.display.update()
        fpsClock.tick(FPS)

def main():
    global language, Player
    Player.lSite, Player.username, password, Player.money, Player.numItem, Player.countItem, Player.numRace = loginScreen()
    mainMenu()

if __name__ == "__main__":
    main()
