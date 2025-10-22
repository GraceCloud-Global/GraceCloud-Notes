# Ensure you're authenticated first
gh auth login

# Create teams
$teams = @{
    "GraceOps"      = "Executive oversight / project management"
    "DevCore"       = "Backend and API development"
    "FrontlineUX"   = "Frontend and UI development"
    "DevInfra"      = "CI/CD and Infrastructure"
    "QA-Testers"    = "Quality Assurance team"
    "Contributors"  = "External collaborators"
    "Observers"     = "Read-only access group"
}

foreach ($t in $teams.Keys) {
    gh team create $t --description "$($teams[$t])" --org GraceCloud-Global --privacy closed
}

# Assign repositories and permission levels
gh team add-repo GraceCloud-Global/GraceOps GraceCloud-Global/GraceAloneABA-Backend --permission admin
gh team add-repo GraceCloud-Global/DevCore GraceCloud-Global/GraceAloneABA-Backend --permission write
gh team add-repo GraceCloud-Global/DevInfra GraceCloud-Global/GraceAloneABA-Backend --permission maintain
gh team add-repo GraceCloud-Global/QA-Testers GraceCloud-Global/GraceAloneABA-Backend --permission triage
gh team add-repo GraceCloud-Global/Contributors GraceCloud-Global/GraceAloneABA-Backend --permission write

gh team add-repo GraceCloud-Global/GraceOps GraceCloud-Global/GraceAloneABA-Frontend --permission admin
gh team add-repo GraceCloud-Global/FrontlineUX GraceCloud-Global/GraceAloneABA-Frontend --permission write
gh team add-repo GraceCloud-Global/QA-Testers GraceCloud-Global/GraceAloneABA-Frontend --permission triage
gh team add-repo GraceCloud-Global/Contributors GraceCloud-Global/GraceAloneABA-Frontend --permission write

# (Optional) Add yourself to all key teams
$myUser = "Damion16729"
foreach ($team in $teams.Keys) {
    gh team add-member GraceCloud-Global/$team $myUser
}
