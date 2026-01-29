#!/usr/bin/env python3
import subprocess
import json
import sys
import shutil

def run_command(command, check=True, capture_output=True, text=True):
    """Result wrapper for subprocess.run."""
    try:
        result = subprocess.run(
            command,
            check=check,
            capture_output=capture_output,
            text=text,
            shell=True
        )
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        raise e

def check_dependencies():
    """Check if gh and git are installed."""
    if not shutil.which("gh"):
        print("Error: GitHub CLI (gh) is not installed. Please install it (e.g., 'brew install gh') and login ('gh auth login').")
        sys.exit(1)
    if not shutil.which("git"):
        print("Error: git is not installed.")
        sys.exit(1)

def get_current_branch():
    """Get the name of the current git branch."""
    res = run_command("git branch --show-current")
    return res.stdout.strip()

def get_open_prs():
    """Fetch open PRs using gh CLI."""
    print("Fetching open PRs...")
    # Fields: number, title, headRefName, headRepositoryOwner, url
    cmd = "gh pr list --state open --json number,title,headRefName,headRepositoryOwner,url"
    try:
        res = run_command(cmd)
        return json.loads(res.stdout)
    except Exception:
        print("Failed to list PRs. specific 'gh' error might be above.")
        return []

def run_tests():
    """Run pytest."""
    try:
        print("Running tests...")
        # Use sys.executable to ensure we use the same python environment
        # and -m pytest to add CWD to sys.path
        import os
        env = os.environ.copy()
        env["PYTHONPATH"] = os.getcwd()
        
        cmd = "pytest"
        subprocess.run(cmd, shell=True, check=True, capture_output=False, env=env)
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    check_dependencies()
    
    current_branch = get_current_branch()
    print(f"Current branch: {current_branch}")
    
    # Warn user
    print("WARNING: This script will attempt to merge PRs into your *current* branch.")
    print("Ensure you have a clean working directory.")
    
    # Check for uncommitted changes (ignoring untracked files)
    status = run_command("git status --porcelain --untracked-files=no")
    if status.stdout.strip():
        print("Error: You have uncommitted changes (modified/staged files). Please stash or commit them first.")
        sys.exit(1)

    prs = get_open_prs()
    if not prs:
        print("No open PRs found.")
        sys.exit(0)
    
    print(f"Found {len(prs)} open PRs.")
    
    processed_count = 0
    merged_count = 0
    failed_count = 0
    skipped_count = 0
    
    for pr in prs:
        pr_number = pr['number']
        title = pr['title']
        user = pr['headRepositoryOwner']['login']
        # We construct a local branch name for the PR
        pr_branch_name = f"pr-{pr_number}-integration"
        
        print(f"\nProcessing PR #{pr_number}: {title} (by {user})")
        
        try:
            # 1. Fetch the PR into a temporary local branch
            # Syntax: git fetch origin pull/ID/head:BRANCHNAME
            print(f"  Fetching PR #{pr_number}...")
            run_command(f"git fetch origin pull/{pr_number}/head:{pr_branch_name}")
            
            # 2. Merge attempts
            print(f"  Attempting merge into {current_branch}...")
            # --no-commit: Allows us to run tests before finalizing
            # --no-ff: Preserves merge commit structure if we were committing, but here we just want to test content.
            # Actually, we want to integration test.
            try:
                run_command(f"git merge --no-commit --no-ff {pr_branch_name}", check=True)
            except subprocess.CalledProcessError:
                print(f"  [X] Merge conflict or failure for PR #{pr_number}. Aborting merge.")
                run_command("git merge --abort", check=False)
                # Cleanup branch
                run_command(f"git branch -D {pr_branch_name}", check=False)
                skipped_count += 1
                continue
            
            # 3. Run Tests
            print("  Merge successful (staged). Running tests...")
            if run_tests():
                # Tests Passed
                print(f"  [+] Tests PASSED for PR #{pr_number}.")
                # 4. Commit results
                # We commit the merge
                commit_msg = f"Merge PR #{pr_number}: {title}"
                run_command(f"git commit -m '{commit_msg}'")
                print("  [+] Changes committed.")
                merged_count += 1
            else:
                # Tests Failed
                print(f"  [-] Tests FAILED for PR #{pr_number}. Rolling back...")
                run_command("git merge --abort")
                failed_count += 1
                
            # Cleanup local PR branch
            run_command(f"git branch -D {pr_branch_name}", check=False)
            
        except Exception as e:
            print(f"  [!] Unexpected error processing PR #{pr_number}: {e}")
            # Try to ensure we aren't left in a bad state
            run_command("git merge --abort", check=False)
            run_command(f"git branch -D {pr_branch_name}", check=False)
            failed_count += 1

    print("\n" + "="*30)
    print("SUMMARY")
    print(f"Total PRs processed: {len(prs)}")
    print(f"Merged: {merged_count}")
    print(f"Failed (Tests): {failed_count}")
    print(f"Skipped (Conflicts): {skipped_count}")
    print("="*30)

if __name__ == "__main__":
    main()
