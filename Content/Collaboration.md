# Collaboration
**Summary:** Here, we describe the ways you can use GitHub to collaborate with project partners. The key to collaboration is to use different branches for parts of the project. By creating a branch, you create a copy of the project at a given time. For example, you could create a separate branch for each member of the project, or a branch for each section of the analysis. This allows you to work on each branch separately, without creating any changes to the master file. You are then able to work on all the files in your branch and save them to your branch. Eventually, you will be able to merge changes in your 

#### 1. Creating Branches 
Create a new branch using the following code. This will make a copy of the directory of your current branch. 
```
git branch new_branch
```

#### 2. Switch to the new branch. 
At this point, you've only created a new branch. You are still in the branch you originally started in. Switch branches by running the following. Confirm you've sucessfully switched branches by checking the status. 
```
git checkout new_branch
git status
```

#### 3. Edit your new branch, and commit your new branch to the online repo
This will save your edits to a different branch on GitHub. You will have this local branch saved on your computer.
```
git commit -m "message"
git push origin new_branch 
```
