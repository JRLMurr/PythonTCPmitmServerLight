import socket,warnings, datetime, random, time
import multiprocessing, ThreadWithResponse
warnings.filterwarnings("ignore")
class Player:
    def __init__(self, GameIp, GamePort, PcPort, debug = False ):
        self.ThreadWithReturnValue = ThreadWithResponse.ThreadWithReturnValue
        self.PcPort = PcPort
        self.targetGame = GameIp
        self.targetPort = GamePort
        self.GameServerConnection = None
        self.recvData = 65500

    def ConnectionDataSend(self):
        try:
            while True:
                data = self.PcPort.recv(self.recvData)
                try:
                    self.GameServerConnection.send(data)
                except:
                    print("Thread dead for gameServerSending")
        except:
            print("Thread dead for listening to the PcPort")

    def WaitForData(self):
        try:
            while True:
                data = self.GameServerConnection.recv(self.recvData)

                try:
                    self.PcPort.send(data)
                except:
                    print("Thread dead for sending to PcPort")
        except:
            print("Thread dead for listening to GameServerConnection")

    def CreateNewConnection(self):
        Trying = True
        failed = False
        counter = 0
        while Trying:
            try:
                gameserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                gameserver.connect((self.targetGame, self.targetPort))
                Trying = False
                print("Successfully connected to targetGame: ", self.targetGame)
            except:
                counter = counter + 1
        if(counter == 10):
            failed = True
            Trying = False
        if(not failed):
            self.GameServerConnection = gameserver
            if(self.State == False):
                self.State = True
                self.SetState()
        else:
            print("Closing Connection, Failed connecting to target server!")

    def SetState(self):
        (multiprocessing.Process(target=self.WaitForData)).start()
        (self.ThreadWithReturnValue(target=self.ConnectionDataSend, args=()).start())

    def SuperClient(self):
        if(self.SecondaryConnection == None):            
            gameserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            gameserver.connect((self.targetGame, self.targetPort))
            self.SecondaryConnection = gameserver
        else:
            self.SecondaryConnection.send(self.RequestsBytesNew)

    def CreateConnection(self, ConnectionToGame):
        self.GameServerConnection = ConnectionToGame

    def CloseConnections(self):
        self.GameServerConnection.close()