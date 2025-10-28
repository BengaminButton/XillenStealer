#ifndef FILE_GRABBER_H
#define FILE_GRABBER_H

#include <string>

class FileGrabber {
public:
    static std::string GrabFiles(const std::string& pattern);
};

#endif
