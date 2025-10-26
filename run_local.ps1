cd C:\gracealoneaba

# Start backend (Django REST)
Start-Job -Name "backend" -ScriptBlock {
    cd C:\gracealoneaba\backend
    python manage.py runserver 0.0.0.0:8000
}

# Start frontend (React)
Start-Job -Name "frontend" -ScriptBlock {
    cd C:\gracealoneaba\frontend
    npm run dev
}

# Wait for exit signal
Write-Host "
Grace Alone ABA Local Mode running... Press Enter to stop and push to GitHub."
Read-Host

# Stop all jobs
Get-Job | Stop-Job | Remove-Job

# Auto Git commit & push
cd C:\gracealoneaba
git add .
git commit -m "Local session update 2025-10-26 16:50:31"
git push origin main

Write-Host "
 Local servers stopped and changes pushed to GitHub."
