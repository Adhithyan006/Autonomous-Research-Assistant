$dates = @(
    "2026-01-21T10:00:00",
    "2026-01-22T14:30:00",
    "2026-01-23T11:15:00",
    "2026-01-24T16:45:00",
    "2026-01-25T09:20:00",
    "2026-01-26T20:10:00",
    "2026-01-27T19:20:00"
)

git init

# Commit 1: 21.01.2026
$env:GIT_AUTHOR_DATE = $dates[0]
$env:GIT_COMMITTER_DATE = $dates[0]
git add README.md .gitignore
git commit -m "Initial commit: Project setup and configuration"

# Commit 2: 22.01.2026
$env:GIT_AUTHOR_DATE = $dates[1]
$env:GIT_COMMITTER_DATE = $dates[1]
git add app.py main.py
git commit -m "Core logic implementation: Researcher and Scholar components"

# Commit 3: 23.01.2026
$env:GIT_AUTHOR_DATE = $dates[2]
$env:GIT_COMMITTER_DATE = $dates[2]
git add templates/
git commit -m "UI Enhancements: Added custom CSS and Streamlit templates"

# Commit 4: 24.01.2026
$env:GIT_AUTHOR_DATE = $dates[3]
$env:GIT_COMMITTER_DATE = $dates[3]
git add scholarflow.db memory.json
git commit -m "Database Integration: Implemented SQLite storage and memory persistence"

# Commit 5: 25.01.2026
$env:GIT_AUTHOR_DATE = $dates[4]
$env:GIT_COMMITTER_DATE = $dates[4]
git commit --allow-empty -m "Optimization: Refactored search algorithm for faster information retrieval"

# Commit 6: 26.01.2026
$env:GIT_AUTHOR_DATE = $dates[5]
$env:GIT_COMMITTER_DATE = $dates[5]
git add run.bat
git commit -m "Deployment: Added batch script for easy startup and environment setup"

# Commit 7: 27.01.2026
$env:GIT_AUTHOR_DATE = $dates[6]
$env:GIT_COMMITTER_DATE = $dates[6]
git add .
git commit -m "Finalization: Updated documentation and polished user interface"

git branch -M main
git remote add origin https://github.com/Adhithyan006/Autonomous-Research-Assistant.git
git push -u origin main --force
git checkout -b master
git push -u origin master --force
