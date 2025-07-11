import os
import time

# Change this to the filename you want to modify
filename = "commit_log.txt"

# Create or append to the file
with open(filename, "a") as f:
    for i in range(1, 51):
        f.write(f"Auto commit line {i} at {time.ctime()}\n")
        os.system("git add .")
        os.system(f'git commit -m "Auto Commit {i}: {time.ctime()}"')
        time.sleep(1)  # Optional delay between commits

# Push to GitHub
os.system("git push origin main")  # Change 'main' to your branch name if needed
