## Sync Versions Between Google Drive and Git

#### 1. Connect respository to local computer
##### Option 1:  Set up Project Reposity in GitHub  and Clone to Local computer 
- Create a repo from GitHub's website interface
- Open the git bash you installed. 
- Use the following code to clone your respository in a LEO folder. 
```
cd /path/to/leo/folder/you/want/connected/to/github/
git clone https://github.com/BeccaBrough/UsingGitHubLEO.git
```
##### Option 2:  Initiate a local folder on computer as a GitHub repository 
- If you have folders in Google drive you want to sync to GitHub, then you must initiate them as git folders

```
cd /path/to/leo/folder/you/want/connected/to/github/
git init
```

#### 2. Make changes to files 
- Make edits, changes, etc. 
- Save files using the same name (no V1, V2) 

#### 3. Identify Files that Need to be synced back to GitHub
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
#### 5. Commit Changes Back to GitHub
```
git push origin your-branch
```

You may need to set your origin as the correct online repo

```
git remote add origin url-to-repo
```
#### 6. Update Local Drive with Most Recent GitHub
- Do this when the repo on GitHub is more uptodate than your working version on your local computer
- For example, if you work on your file directly in GitHub or if someone else updates GitHub
```
git pull remote-name (e.g. origin) branch-name (e.g. master)
```
- Git Pull is a combination of two other Git commands, git fetch and git merge 
- Git fetch: updates remote tracking branches
- Git merge: updates the current branch (e.g. master) with the corresponding remote tracking branch  (e.g. origin)
