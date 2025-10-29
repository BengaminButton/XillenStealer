$token = "YOUR_GITHUB_TOKEN_HERE"
$owner = "BengaminButton"
$repo = "XillenStealer"

$releaseNotes = "# XillenStealer V4.0 Release`n`n## What's New`n`n### Portable Builder (EXE)`n- No Python/Node.js installation required`n- All dependencies included`n- Works out of the box`n`n### How to Use`n1. Download XillenStealer-V4-Builder-Windows.zip`n2. Extract it`n3. Run XillenStealer Builder.exe`n`n---`n`nFor more info, see the README: https://github.com/BengaminButton/XillenStealer#%D1%80%D0%B5%D0%BB%D0%B8%D0%B7%D1%8B-%D0%B8-%D0%B7%D0%B0%D0%B3%D1%80%D1%83%D0%B7%D0%BA%D0%B8"

$releaseId = "v4.0"

$bodyJson = @{
    body = $releaseNotes
} | ConvertTo-Json

Write-Host "Updating release..." -ForegroundColor Cyan
try {
    $response = Invoke-WebRequest -Uri "https://api.github.com/repos/$owner/$repo/releases/tags/$releaseId" `
        -Method Patch `
        -Headers @{
            "Authorization" = "Bearer $token"
            "Accept" = "application/vnd.github+json"
        } `
        -Body ([System.Text.Encoding]::UTF8.GetBytes($bodyJson)) `
        -ContentType "application/json; charset=utf-8"
    
    $release = $response.Content | ConvertFrom-Json
    Write-Host "Success! Release updated: $($release.html_url)" -ForegroundColor Green
    
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}
