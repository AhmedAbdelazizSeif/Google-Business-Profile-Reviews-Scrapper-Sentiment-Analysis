# Getting Started with GitHub

This guide helps you push your project to GitHub.

## Step 1: Create GitHub Repository

1. Go to [GitHub](https://github.com)
2. Click "New Repository" or visit https://github.com/new
3. Fill in details:
   - **Repository name**: `google-reviews-sentiment-analysis`
   - **Description**: Automated Google Business reviews sentiment analysis with bilingual support
   - **Visibility**: Choose Public or Private
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
4. Click "Create repository"

## Step 2: Initialize Local Git Repository

Open PowerShell in the `github-repo` directory and run:

```powershell
# Navigate to the github-repo directory
cd c:\Users\aseif\Jupyter\scraps\google_reviews\github-repo

# Initialize git repository
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: Complete sentiment analysis system v2.0.0"
```

## Step 3: Connect to GitHub

Replace `YOUR_USERNAME` with your GitHub username:

```powershell
# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/google-reviews-sentiment-analysis.git

# Verify remote
git remote -v
```

## Step 4: Push to GitHub

```powershell
# Push to GitHub (main branch)
git branch -M main
git push -u origin main
```

If prompted, enter your GitHub credentials:
- **Username**: Your GitHub username
- **Password**: Use a [Personal Access Token](https://github.com/settings/tokens) instead of password

### Creating a Personal Access Token

1. Go to GitHub Settings > Developer settings > Personal access tokens
2. Click "Generate new token (classic)"
3. Select scopes: `repo` (full control of private repositories)
4. Generate and copy the token
5. Use this token as your password when pushing

## Step 5: Verify on GitHub

1. Go to your repository: `https://github.com/YOUR_USERNAME/google-reviews-sentiment-analysis`
2. Verify all files are present
3. Check that README.md displays correctly

## Step 6: Add Repository Topics (Optional)

On your repository page:
1. Click the gear icon next to "About"
2. Add topics:
   - `sentiment-analysis`
   - `google-reviews`
   - `selenium`
   - `python`
   - `nlp`
   - `vader`
   - `excel-automation`
   - `data-analysis`

## Common Git Commands

```powershell
# Check status
git status

# Add specific file
git add path/to/file

# Commit changes
git commit -m "Your commit message"

# Push changes
git push

# Pull latest changes
git pull

# Create new branch
git checkout -b feature-name

# Switch branches
git checkout branch-name

# View commit history
git log --oneline
```

## Branching Strategy

For future development:

- `main` - Production-ready code
- `develop` - Development branch
- `feature/*` - New features
- `bugfix/*` - Bug fixes
- `hotfix/*` - Urgent fixes

## .gitignore Already Configured

Your `.gitignore` file excludes:
- Virtual environments (`venv/`)
- Python cache (`__pycache__/`, `*.pyc`)
- Jupyter checkpoints
- Output files (`output/`)
- Sensitive data (`*.env`, credentials)
- OS files (`.DS_Store`, `Thumbs.db`)

## Protecting Sensitive Data

Before committing, ensure:
1. No passwords in code
2. Database credentials in `.env` (not committed)
3. API keys in environment variables
4. Review `.gitignore` is working: `git status`

## Next Steps After Pushing

1. **Add README badges**: Update README.md with your repository URL
2. **Create releases**: Tag versions (v2.0.0)
3. **Add GitHub Actions**: CI/CD pipeline
4. **Enable GitHub Pages**: Project documentation
5. **Add collaborators**: Invite team members
6. **Create issues**: Track bugs and features
7. **Set up projects**: Kanban boards

## Troubleshooting

**Problem**: Permission denied (publickey)
**Solution**: Set up SSH key or use HTTPS with personal access token

**Problem**: Large files rejected
**Solution**: Check `.gitignore` is excluding output files

**Problem**: Merge conflicts
**Solution**: `git pull` before pushing, resolve conflicts manually

## Need Help?

- [GitHub Documentation](https://docs.github.com)
- [Git Reference](https://git-scm.com/docs)
- [GitHub Desktop](https://desktop.github.com) - GUI alternative

---

**Ready to push?** Run the commands in Step 2-4 and your project will be on GitHub! 🚀
