# Security Policy

## Supported Versions

We release patches for security vulnerabilities. Which versions are eligible for receiving such patches depends on the CVSS v3.0 Rating:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

Please report (suspected) security vulnerabilities to **[INSERT EMAIL ADDRESS]**. You will receive a response from us within 48 hours. If the issue is confirmed, we will release a patch as soon as possible depending on complexity but historically within a few days.

### What to Include

When reporting a vulnerability, please include:

1. Description of the vulnerability
2. Steps to reproduce
3. Potential impact
4. Suggested fix (if any)
5. Your contact information for follow-up

### What NOT to Do

- Do not open a public issue
- Do not disclose the vulnerability publicly until it has been addressed
- Do not test the vulnerability on live production systems without permission

## Security Best Practices for Users

### API Keys

- Never commit API keys to version control
- Use environment variables or `.env` files (gitignored)
- Rotate API keys regularly
- Use separate API keys for development and production

### Browser Automation

- Be cautious when automating sensitive operations
- Use headless mode when possible to avoid accidental exposure
- Clear browser profiles regularly if handling sensitive data
- Review generated code before execution in sensitive environments

### Code Execution

- bAUTO uses `exec()` to run generated code
- Only use bAUTO with trusted AI providers
- Review instruction files from untrusted sources
- Consider sandboxing in production environments

### Dependencies

- Keep dependencies up to date: `pip install --upgrade -r requirements.txt`
- Use virtual environments to isolate dependencies
- Regularly check for security advisories

## Known Security Considerations

### AI-Generated Code

bAUTO generates and executes code using AI. While we implement safety measures:

- Generated code is executed in a controlled scope
- Dangerous operations are limited
- Error handling prevents most unsafe operations

However, users should:
- Review critical automations manually
- Test in safe environments first
- Implement additional safeguards for production use

### Browser Data

bAUTO creates browser profiles that may contain:
- Cookies
- Session data
- Cached credentials

**Recommendation**: Use separate profiles for different purposes and clear profiles regularly.

## Security Updates

Security updates will be released as soon as possible after a vulnerability is confirmed. Users will be notified through:

- GitHub Security Advisories
- Release notes
- Project discussions

## Acknowledgments

We appreciate the security research community's efforts in responsibly disclosing vulnerabilities. Contributors who report valid security issues will be acknowledged (with permission) in release notes.

## Contact

For security concerns, please contact: **[INSERT SECURITY EMAIL]**

For general issues, use the [GitHub issue tracker](https://github.com/SwintexD/bAUTO/issues).

