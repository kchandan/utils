import paramiko
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText

const_ssh_servers = 'sshhost'
USER = 'username'
PASSWORD = 'password'
TEXTFILE='statusfile'
MAILSERVER='127.0.0.1'
MAILTO='targetmail'
MAILFROM='youremail'
DISK_USAGE_LIMIT=10

class MYSSHClient():

    def __init__(self, server=const_ssh_servers, username=USER, password=PASSWORD):
        self.server = server
        self.username = username
        self.password = password
        self.connection = None
        self.result =  ''
        self.is_error = False
        self.textfile=TEXTFILE


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
                return self.result
            
        else:
            print "no command was entered"

    def do_close(self):
        self.connection.close()

class Myemail():

    def __init__(self,server=MAILSERVER,mailto=MAILTO,mailfrom=MAILFROM,textfile=TEXTFILE):
        self.server=server
        self.mailto=mailto
        self.mailfrom=mailfrom
        self.textfile=textfile

    def send_mail(self):
        
        fp = open(self.textfile, 'rb')
        msg = MIMEText(fp.read())
        fp.close()
        msg['Subject'] ='Disk usage report'
        msg['From'] = self.mailfrom
        msg['To'] = self.mailto
        s = smtplib.SMTP('127.0.0.1')
        s.sendmail(self.mailfrom, [mail.mailto], msg.as_string())
        s.quit()
    
class FormatOutput():
    
    def __init__(self,result):
        self.result=result;
        self.disk_usage=DISK_USAGE_LIMIT
        self.textfile=TEXTFILE

    def format_df_h(self):
        fp = open(self.textfile, 'w')

        for line in self.result.split('\n'):
            if not line:
                continue
            usage=line.split()[4][:-1]
            disk=line.split()[0]
            if (disk != 'Filesystem') and (usage > self.disk_usage):
                fp.write(line.split()[0] + '\thas usage ' + usage + '%\n')
                #print line.split()[0] + '\thas usage ' + usage + '%\n'

        fp.close()
            
                
              



if __name__ == '__main__':
    client = MYSSHClient()
    client.do_connect()
    command = 'df -h'
    result=client.execute_command(command)
    client.do_close()
    output = FormatOutput(result)
    output.format_df_h()
    mail = Myemail()
    mail.send_mail()
