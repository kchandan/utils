import paramiko
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText

SERVER = '192.168.2.66'
USER = 'chandank'
PASSWORD = 'chandan'

class MYSSHClient():

    def __init__(self, server=SERVER, username=USER, password=PASSWORD):
        self.server = server
        self.username = username
        self.password = password
        self.connection = None
        self.result =  ''
        self.is_error = False


    def do_connect(self):
        self.connection = paramiko.SSHClient()
        self.connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.connection.connect(self.server, username=self.username, password=self.password)

    def execute_command(self, command):
        if command:
            print command            
            stdin,stdout,stderr = self.connection.exec_command(command)
            stdin.close()
            error = str(stderr.read())
            if error:
                self.is_error = True
                self.result = error
                print 'error'
            else:
                self.is_error = False
                self.result = str(stdout.read())
                print 'no error'

            print self.result


        else:
            print "no command was entered"

    def do_close(self):
        self.connection.close()

class Myemail():

    def __init__(self,server=MAILSERVER,mailto=MAILTO,mailfrom=MAILFROM,texfile=TEXTFILE):
        self.server=server
        self.mailto=mailto
        self.mailfrom=mailfrom
        self.texfile=textfile

    def send_mail(self):
        
        fp = open(self.textfile, 'rb')
        msg = MIMEText(fp.read())
        fp.close()
        msg['Subject'] ='The contents of %s' % self.textfile
        msg['From'] = self.mailfrom
        msg['To'] = self.mailto
        s = smtplib.SMTP('127.0.0.1')
        s.sendmail(me, [you], msg.as_string())
        s.quit()
    
        


if __name__ == '__main__':
    client = MYSSHClient()
    client.do_connect()
    command = 'df -h'
    client.execute_command(command)
    client.do_close()
