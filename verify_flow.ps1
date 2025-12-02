$headers = @{
    "Content-Type" = "application/json"
}

$body = @{
    email = "test@example.com"
    movieId = "573a1390f29313caabcd4135"
    rating = 5
    comment = "Excellent movie!"
} | ConvertTo-Json

Write-Host "Sending rating to Calificacion service..."
try {
    $response = Invoke-RestMethod -Uri "http://localhost:5001/ratings" -Method Post -Headers $headers -Body $body
    Write-Host "Response from Calificacion:"
    Write-Host ($response | ConvertTo-Json -Depth 5)
} catch {
    Write-Error "Failed to send rating. Ensure services are running."
    exit 1
}

Write-Host "`nWaiting for processing..."
Start-Sleep -Seconds 5

Write-Host "`nChecking Opiniones service logs (you should see 'Received rating' and 'Rating saved')..."
docker logs opiniones
