import socket, warnings, random
import ThreadWithResponse
import PlayerTCP
warnings.filterwarnings("ignore")

class TcpMitm:
    def __init__(self, ServerIp, ServerPort, ActualGameIp, Debug = False):
        self.Debug = Debug
        self.ThreadWithReturnValue = ThreadWithResponse.ThreadWithReturnValue
        self.Players = []
        self.ServerIp = ''
        self.ServerPort = ServerPort
        self.ActualGameServer = ActualGameIp
        self.RECV = 65500
        self.main()

    def main(self):
        try:
            sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            sock.bind((self.ServerIp,self.ServerPort))
            sock.listen(100)
            print("Listening on ", self.ServerIp, " : ", self.ServerPort)
            while True:
                conn, addr = sock.accept()
                print('Adding new player: ' + addr[1])
                Deciding = True
                while(Deciding):
                    ip = input("Enter the final digit for the ip: ")
                    if(ip.isdigit()):
                        port = input("Enter the final digit for the ip: ")
                        if (port.isdigit()):
                            NewPlayer = PlayerTCP.Player(GameIp=self.ActualGameServer + ip, GamePort=port, PcPort=conn ,debug=self.Debug)
                            NewPlayer.CreateNewConnection()
                            self.Players.append(NewPlayer)
        except Exception as e:
            print(e)
TCP_PORT = 8889
Target_IP = "198.20.200."

TcpMitm('',TCP_PORT,Target_IP,0,True)
