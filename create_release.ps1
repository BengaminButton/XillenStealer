$token = "YOUR_GITHUB_TOKEN_HERE"
$owner = "BengaminButton"
$repo = "XillenStealer"
$tag = "v4.0"
$releaseNotes = Get-Content "RELEASE_NOTES.md" -Raw

$headers = @{
    "Authorization" = "Bearer $token"
    "Accept" = "application/vnd.github+json"
    "Content-Type" = "application/json"
}

$bodyObject = @{
    "tag_name" = $tag
    "name" = "XillenStealer V4.0 - Portable Builder"
    "body" = $releaseNotes
    "draft" = $false
    "prerelease" = $false
}
$body = $bodyObject | ConvertTo-Json -Depth 10

Write-Host "Creating release..."
$release = Invoke-RestMethod -Uri "https://api.github.com/repos/$owner/$repo/releases" -Method Post -Headers $headers -Body $body

Write-Host "Release created: $($release.html_url)"
Write-Host "Uploading file..."

$uploadUrl = $release.upload_url -replace '\{?name\}?', ''
$fileName = "XillenStealer-V4-Builder-Windows.zip"
$filePath = Join-Path $PWD $fileName

$fileBytes = [System.IO.File]::ReadAllBytes($filePath)
$uploadHeaders = @{
    "Authorization" = "Bearer $token"
    "Content-Type" = "application/zip"
}

try {
    Invoke-RestMethod -Uri "$uploadUrl?name=$fileName" -Method Post -Headers $uploadHeaders -Body $fileBytes
    Write-Host "File uploaded successfully!"
    Write-Host "Release URL: $($release.html_url)"
} catch {
    Write-Host "Error uploading file: $_"
}
