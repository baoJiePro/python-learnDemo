import socket
import os
import json

class FtpClient(object):
    def __init__(self):
        self.client = socket.socket()

    def help(self):
        msg = '''
            ls
            pwd
            cd..
            get filename
            put filename
        '''
        print(msg)

    def connect(self, ip, port):
        self.client.connect(ip, port)

    def interactive(self):
        while True:
            cmd = input(">>").strip()
            if len(cmd) == 0: continue
            cmd_str = cmd.split()[0]
            if hasattr(self, "cmd_%s" % cmd_str):
                func = getattr(self, "cmd_%s" % cmd_str)
                func(cmd)
            else:
                self.help()

    def cmd_put(self, *args):
        cmd_split = args[0].split()
        if len(cmd_split) > 1:
            fileName = cmd_split[1]
            if os.path.isfile(fileName):
                filesize = os.stat(fileName).st_size
                msg_dic = {
                    "action": "put",
                    "filename": fileName,
                    "size": filesize,
                    "overridden": True
                }
                self.client.send(json.dumps(msg_dic).encode("utf-8"))
                # 防止粘包，等服务器确认
                server_response = self.client.recv(1024)
                f = open(fileName, "rb")
                for line in f:
                    self.client.send(line)
            else:
                print(fileName, "is not file")

    def cmd_get(self):
        pass
