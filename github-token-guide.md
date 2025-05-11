# GitHub Personal Access Token Guide

## 1. Generating a Token on GitHub

1. Go to GitHub and sign in to your account
2. Click on your profile picture in the top right corner
3. Select "Settings" from the dropdown menu
4. Scroll down to "Developer settings" in the left sidebar
5. Select "Personal access tokens" → "Tokens (classic)"
6. Click "Generate new token" → "Generate new token (classic)"
7. Give your token a descriptive name
8. Set an expiration date (recommended for security)
9. Select scopes based on your needs (for basic repo access, select "repo")
10. Click "Generate token"
11. **IMPORTANT**: Copy your token immediately! You won't be able to see it again.

## 2. Using the Token for HTTPS Authentication

When pushing to a repository for the first time, you'll be prompted for authentication:

```bash
git push origin main
```

- For username: enter your GitHub username
- For password: paste your personal access token (not your GitHub password)

## 3. Setting Up Credential Caching

### macOS

```bash
# Cache credentials for 1 hour (3600 seconds)
git config --global credential.helper 'cache --timeout=3600'

# Or store permanently in macOS Keychain
git config --global credential.helper osxkeychain
```

### Windows

```bash
# Store permanently
git config --global credential.helper store

# Or cache temporarily
git config --global credential.helper 'cache --timeout=3600'
```

### Linux

```bash
# Store permanently (less secure)
git config --global credential.helper store

# Or cache temporarily (3600 seconds = 1 hour)
git config --global credential.helper 'cache --timeout=3600'
```

## Security Notes

- Treat your token like a password
- Use the shortest expiration time that's practical for your needs
- Give tokens the minimum permissions necessary
- Regenerate tokens if you suspect they've been compromised
- For shared environments, prefer temporary caching over permanent storage