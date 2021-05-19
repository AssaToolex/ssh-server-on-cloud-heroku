from modules.sshd.sshd_server import SshdServer

if __name__ == '__main__':
    server = SshdServer()
    address = '127.0.0.22'
    port = 22022
    print("Client use: $ ssh admin@{address} -p {port}".format(address=address, port=port))
    server.start(address=address, port=port)
