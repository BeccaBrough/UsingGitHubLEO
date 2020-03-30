## Installation

## Sync Between Google Drive and Git

#### 1. Set up Project Reposity in GitHub  
#### 2. Clone repository from GitHub to local computer
- Open the git bash you installed. 
- Use the following code to clone your respository in a LEO folder. 
```
cd /path/to/leo/folder/you/want/connected/to/github/
git clone https://github.com/BeccaBrough/UsingGitHubLEO.git
```

#### 3. Make changes to files 
- Make edits, changes, etc. 
- Save files using the same name (no V1, V2) 

#### 4. Identify Files that Need to be synced back to GitHub
- Open Git Bash
- Display all files that you've made changes to
```
cd /path/to/leo/folder/you/made/changes/to/ (should be same folder as in step 2.2)
git status 
```
#### 4. Commit Changes Back to GitHub
- Syncing Files 
```
# To Sync Entire Folder
git add . 
# To Sync Certain Files:
git add "FolderName" 
```
- Commit files 
```
git commit -m "Make a Note of what You Did"
```
#### Commit Changes Back to GitHub
