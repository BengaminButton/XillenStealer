$token = "8474305805:AAHZ98s7nr9IAFQehnqh0x3iGV1OmVhTq9I"
$chatId = "7368280792"
$message = "XILLENSTEALER V5 TEST - BUILD SUCCESSFUL"

Write-Host "[*] Sending test message to Telegram..."

$url = "https://api.telegram.org/bot$token/sendMessage?chat_id=$chatId&text=$message"

try {
    $response = Invoke-RestMethod -Uri $url -Method Get
    Write-Host "[+] SUCCESS! Message sent to Telegram!"
    Write-Host "[+] Message ID: $($response.result.message_id)"
    Write-Host "[+] Chat: $($response.result.chat.first_name)"
} catch {
    Write-Host "[!] ERROR: $($_.Exception.Message)"
}

Write-Host ""
Write-Host "Press Enter to continue..."
Read-Host
