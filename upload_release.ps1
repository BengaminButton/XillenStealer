$ErrorActionPreference = "Stop"

$token = "YOUR_GITHUB_TOKEN_HERE"
$owner = "BengaminButton"
$repo = "XillenStealer"

$releaseNotes = @"
# XillenStealer V4.0 Release

## Что нового

### Портативный Builder (EXE)
- Не требует установки Python/Node.js
- Все зависимости включены
- Работает из коробки

### Как использовать
1. Скачай XillenStealer-V4-Builder-Windows.zip
2. Распакуй
3. Запусти XillenStealer Builder.exe

См. https://github.com/BengaminButton/XillenStealer#-%D1%80%D0%B5%D0%BB%D0%B8%D0%B7%D1%8B-%D0%B8-%D0%B7%D0%B0%D0%B3%D1%80%D1%83%D0%B7%D0%BA%D0%B8
"@

$bodyJson = @{
    tag_name = "v4.0"
    name = "XillenStealer V4.0 - Portable Builder"
    body = $releaseNotes
    draft = $false
    prerelease = $false
} | ConvertTo-Json

Write-Host "Step 1: Creating release..." -ForegroundColor Cyan
try {
    $response = Invoke-WebRequest -Uri "https://api.github.com/repos/$owner/$repo/releases" `
        -Method Post `
        -Headers @{
            "Authorization" = "Bearer $token"
            "Accept" = "application/vnd.github+json"
        } `
        -Body ([System.Text.Encoding]::UTF8.GetBytes($bodyJson)) `
        -ContentType "application/json; charset=utf-8"
    
    $release = $response.Content | ConvertFrom-Json
    Write-Host "Release created: $($release.html_url)" -ForegroundColor Green
    
    $uploadUrl = $release.upload_url -replace '\{.*$', ''
    $filePath = "XillenStealer-V4-Builder-Windows.zip"
    
    if (Test-Path $filePath) {
        Write-Host "Step 2: Uploading file..." -ForegroundColor Cyan
        $fileName = Split-Path $filePath -Leaf
        
        $fileBytes = [System.IO.File]::ReadAllBytes($filePath)
        
        $uploadResponse = Invoke-WebRequest -Uri "$uploadUrl?name=$fileName" `
            -Method Post `
            -Headers @{
                "Authorization" = "Bearer $token"
                "Content-Type" = "application/zip"
            } `
            -Body $fileBytes
        
        Write-Host "Success! Release URL: $($release.html_url)" -ForegroundColor Green
    } else {
        Write-Host "Error: File not found: $filePath" -ForegroundColor Red
    }
    
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
    Write-Host $_.Exception.Response.StatusCode.value__
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $responseBody = $reader.ReadToEnd()
        Write-Host $responseBody
    }
}
