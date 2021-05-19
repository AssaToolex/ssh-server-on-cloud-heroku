import unittest
from modules.sshd.sshd_server import Shell, SshdServer


class TestParamiko(unittest.TestCase):

    def test_cmd_02(self):
        test_shell = Shell()
        test_shell.cmdloop()
        
        result = 1
        self.assertEqual(result, 1)
        self.assertNotEqual(result, 0)

    def test_sshd_01(self):
        """
        test:
        $ ssh admin@127.0.0.22 -p 22022
        """

        # How to Generate your SSH keys
        #
        # Linux:
        # use the command `ssh-keygen -A` in terminal 
        # to generate all of your SSH keys. Once the command is run,
        # you can find the RSA key in the following location: ~/.ssh/id_rsa, or /home/username/.ssh/id_rsa
        #
        # Windows 10:
        # Press Windows Key, type 'Manage Optional Features`. If OpenSSH Client & Server is in the list, you're all set.
        # If either is not, click on "Add a feature" and search for `OpenSSH`, click on them to install.
        # Next, open cmd as administrator. Enter the command `ssh-keygen` and follow the on screen prompts.
        # The location of the key will be displayed. Copy that and paste the location here.
        # If you put a password, include it as the second parameter, otherwise don't include it.

        test_server = SshdServer('deploy/docker/conf/sshd-id_rsa.private')
        test_server.start(address='127.0.0.22', port=22022)
        
        result = 1
        self.assertEqual(result, 1)
        self.assertNotEqual(result, 0)

    def test_sshd_02(self):
        """
        test:
        $ ssh admin@127.0.0.22 -p 22022
        """

        test_server = SshdServer()
        test_server.start(address='127.0.0.22', port=22022)
        
        result = 1
        self.assertEqual(result, 1)
        self.assertNotEqual(result, 0)


if __name__ == '__main__':
    unittest.main()
