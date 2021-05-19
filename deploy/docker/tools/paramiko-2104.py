from .modules.sshd.sshd_server import SshServer

if __name__ == '__main__':
    server = SshServer()
    server.start(address='127.0.0.22', port=22022)
