#ifndef SSH_COLLECTOR_H
#define SSH_COLLECTOR_H

#include <string>

class SSHCollector {
public:
    static std::string CollectSSHKeys();
    static std::string CollectFTPSessions();
};

#endif
