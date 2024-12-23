# -*- coding: utf-8 -*-
import SocketServer

flag = "D0g3xGC{a19f009e-d9be-560e-a1f1-6bboa47d4e21}"
ascii_art = '''
                                ,,        ,,         ,...,,                                                               
`7MM"""Mq.                      db      `7MM       .d' ""db                         .g8""8q.    ,gM""bg           db      
  MM   `MM.                               MM       dM`                            .dP'    `YM.  8MI  ,8          ;MM:     
  MM   ,M9   ,6"Yb. `7MMpdMAo.`7MM   ,M""bMM      mMMmm`7MM  `7Mb,od8 .gP"Ya      dM'      `MM   WMp,"          ,V^MM.    
  MMmmdM9   8)   MM   MM   `Wb  MM ,AP    MM       MM    MM    MM' "',M'   Yb     MM        MM  ,gPMN.  jM"'   ,M  `MM    
  MM  YM.    ,pm9MM   MM    M8  MM 8MI    MM mmmmm MM    MM    MM    8M""""""     MM.      ,MP ,M.  YMp.M'     AbmmmqMA   
  MM   `Mb. 8M   MM   MM   ,AP  MM `Mb    MM       MM    MM    MM    YM.    ,     `Mb.    ,dP' 8Mp   ,MMp     A'     VML  
.JMML. .JMM.`Moo9^Yo. MMbmmd' .JMML.`Wbmd"MML.   .JMML..JMML..JMML.   `Mbmmd'       `"bmmd"'   `YMbmm'``MMm..AMA.   .AMMA.
                      MM                                                                MMb                               
                    .JMML.                                                               `bood'                      
'''

def check_whitelist(data):
    whitelist = "~()<{}[]>./?"
    for char in data:
        if char not in whitelist:
            raise ValueError("Invalid character detected, not in whitelist!")

def evaluate_and_compare(expression):
    try:
        result = eval(expression)
        if result == 2000:
            return "Congratulations! Your answer is correct，here is your flag: " + flag
        else:
            return "Wrong answer, try again."
    except Exception as e:
        return "Error evaluating expression: " + str(e)

class Task(SocketServer.BaseRequestHandler):
    def handle(self):
        try:
            self.request.sendall(ascii_art + "\n")
            self.request.sendall("Welcome to Rapid-fire Q&A! Answer the question, and you'll get the flag.\n")
            self.request.sendall("What year was Python 2 released?\n")
            while True:
                self.request.sendall("Enter your answer: ")
                user_input = self.request.recv(1024).strip()
                try:
                    check_whitelist(user_input)
                    response = evaluate_and_compare(user_input)
                    self.request.sendall(response + "\n")
                    if "Congratulations!" in response:
                        break
                except ValueError as e:
                    self.request.sendall(str(e) + "\n")
        except Exception as e:
            self.request.sendall("An unexpected error occurred: " + str(e) + "\n")

class ForkedServer(SocketServer.ForkingMixIn, SocketServer.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 12133
    print("Server listening on {}:{}".format(HOST, PORT))
    server = ForkedServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    server.serve_forever()

