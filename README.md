# Docling-OCR-Unstructured.io
Demo for these tech-stacks




The remote main has commits you don't have locally (likely a README created on GitHub). Fix it with:

bash
# Pull remote main and merge with your local master
git pull origin main --allow-unrelated-histories

# Push your local master to remote main
git push origin master:main
Or if you want to rename your local branch to main as well:

bash
git pull origin main --allow-unrelated-histories
git branch -m master main
git push -u origin main
What's happening:

GitHub created a README.md commit on main when you created the repo
Your local master has no knowledge of that commit
--allow-unrelated-histories merges two branches that have no common ancestor
venv) abhishek@abhishek-ThinkPad-L14-Gen-3:~/Desktop/BAGIC$ git pull origin main --allow-unrelated-histories
From https://github.com/abhishek7112001/Docling-OCR-Unstructured.io
 * branch            main       -> FETCH_HEAD
hint: You have divergent branches and need to specify how to reconcile them.
hint: You can do so by running one of the following commands sometime before
hint: your next pull:
hint: 
hint:   git config pull.rebase false  # merge (the default strategy)
hint:   git config pull.rebase true   # rebase
hint:   git config pull.ff only       # fast-forward only
hint: 
hint: You can replace "git config" with "git config --global" to set a default
hint: preference for all repositories. You can also pass --rebase, --no-rebase,
hint: or --ff-only on the command line to override the configured default per
hint: invocation.
fatal: Need to specify how to reconcile divergent branches.
(venv) abhishek@abhishek-ThinkPad-L14-Gen-3:~/Desktop/BAGIC$ git push origin master:main
To https://github.com/abhishek7112001/Docling-OCR-Unstructured.io.git
 ! [rejected]        master -> main (non-fast-forward)
error: failed to push some refs to 'https://github.com/abhishek7112001/Docling-OCR-Unstructured.io.git'
hint: Updates were rejected because a pushed branch tip is behind its remote
hint: counterpart. Check out this branch and integrate the remote changes
hint: (e.g. 'git pull ...') before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.

Show more
16:07
Run these commands one by one:

bash
git pull origin main --allow-unrelated-histories --no-rebase
It may open a merge commit editor — just save and close it (press Ctrl+X if nano, or :wq if vim).

Then push:

bash
git push origin master:main
If you still face issues and just want to force push (safe since this is a fresh repo with only a README on GitHub):

bash
git push origin master:main --force
This will overwrite the remote main with your local master. Your code will be up on GitHub.

