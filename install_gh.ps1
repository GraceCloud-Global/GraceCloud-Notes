winget install --id GitHub.cli -e --source winget
[Environment]::SetEnvironmentVariable("PATH", $env:PATH + ";$env:LOCALAPPDATA\Programs\GitHub CLI\", [EnvironmentVariableTarget]::Machine)
$env:PATH += ";$env:LOCALAPPDATA\Programs\GitHub CLI\"
gh --version
