# RS-Website Deployment Notes

## Important: This site uses GitHub Actions for deployment (NOT standard GitHub Pages)

### Deployment Process
1. **Push to main branch** triggers the GitHub Actions workflow
2. **Workflow steps**:
   - Cleans files
   - Sets up pages
   - Uploads artifacts
   - Deploys to GitHub Pages
3. **Deployment time**: 2-5 minutes typically

### How to Check Deployment Status
1. Go to: https://github.com/jonwashburn/rs-website
2. Click the **Actions** tab
3. Look for "Deploy to GitHub Pages" workflow
4. Click to see progress
5. Green checkmark (✅) = deployment complete

### Common Issues
- If changes aren't appearing after push, check Actions tab for failures
- Workflow can get stuck - check GitHub Actions status
- Always verify deployment completed before assuming changes are live

### Git Push Issues
When getting "rejected" errors:
```bash
git pull --rebase origin main
git push origin main
```

Use `| cat` to prevent interactive prompts in scripts.

---
Last updated: Aug 12, 2025
