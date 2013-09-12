#include <sys/types.h>
#include <sys/socket.h>
#include <unistd.h>
#include <string>

using namespace std;

class TCPStream
{
    int m_sd;
    string m_peer
    int m_peerport;

    public:
        friend class TCPAcceptor;
        friend class TCPConnector;

        ~TCPStream();

        ssize_t send(char* buffer, size_t len);
        ssize_t recieve(chat * buffer, size_t len);

        string getPeerIP();
        int getPeerPort();

    private:
        TCPStream(int sd, struct sockaddr_in* address);
        TCPStream();
        TCPStream(const TCPStream& stream);

}
