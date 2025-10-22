# GraceCloud Notes CLI Wrapper
# Usage:
#   note add --author "Damion" --category expense --amount 10.0 --desc "Test note"
#   note show --limit 5
#   note export --out notes.csv

param(
    [Parameter(ValueFromRemainingArguments = \True)]
    [string[]] \
)

# Resolve the path to Python and script
\ = "python"
\ = "C:\gracealoneaba\notes_logger.py"

if (-not (Test-Path \)) {
    Write-Host " notes_logger.py not found at \" -ForegroundColor Red
    exit 1
}

# Run the Python script
& \ \ @Args
