# bAUTO Configuration

## 🔑 API Key Setup

The project uses Google Gemini API by default. You'll need an API key:

1. Get a free API key: https://makersuite.google.com/app/apikey
2. Create a `.env` file in the project root:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

## 🤖 Choosing the Right Model

### Gemini Models Available

**Note:** Always use `models/` prefix with Gemini model names.

1. **models/gemini-2.0-flash** (Recommended - Default)
   - Stable Gemini 2.0 model
   - Good rate limits
   - Fast and reliable
   - Best for most use cases

2. **models/gemini-2.5-flash** (Latest)
   - Newest flash model
   - May have quota limits on free tier
   - Use if you need latest features

3. **models/gemini-flash-latest** (Auto-latest)
   - Always points to latest flash model
   - Good for staying current
   - Rate limits may vary

4. **models/gemini-2.0-flash-exp** (Experimental)
   - Experimental features
   - May have lower limits
   - Use for testing only

### How to Change Model

#### Option 1: In quick_start.py

Edit line 58:
```python
config = Config(
    model=ModelConfig(
        provider="gemini",
        model_name="models/gemini-2.0-flash"  # Note: models/ prefix required
    )
)
```

#### Option 2: Via CLI

```bash
python -m bauto.cli run instructions.yaml --model models/gemini-2.0-flash
```

#### Option 3: In config file

Create `config.yaml`:
```yaml
model:
  provider: gemini
  model_name: models/gemini-2.0-flash  # Note: models/ prefix required
  temperature: 0.0
  max_tokens: 2048
```

## ⚠️ Rate Limits

### Free Tier Limits (per minute)

| Model | Requests/min | Best For |
|-------|--------------|----------|
| models/gemini-2.0-flash | 10 | **Recommended** - Stable, reliable |
| models/gemini-2.5-flash | 10 | Latest features |
| models/gemini-flash-latest | 10 | Auto-updated |
| models/gemini-2.0-flash-exp | 2-10 | Testing only |

**Tip:** Use `models/gemini-2.0-flash` for best stability!

**Important:** Always include the `models/` prefix when specifying Gemini model names.

## 🔧 Troubleshooting

### Error 429: Quota Exceeded

**Problem:** You've hit the rate limit.

**Solutions:**
1. Switch to `models/gemini-2.0-flash` (stable model)
2. Wait 1 minute before retrying
3. Upgrade to paid plan for higher limits
4. Reduce the number of concurrent requests

### Error 401: Invalid API Key

**Problem:** API key is not configured or invalid.

**Solution:**
1. Check your `.env` file exists
2. Verify the API key is correct
3. Make sure there are no extra spaces
4. Run: `python -m bauto.cli setup`

### Model Not Found (Error 404)

**Problem:** `404 models/xxx is not found`

**Solution:**
1. Make sure model name includes `models/` prefix
2. Check spelling: `models/gemini-2.0-flash`
3. Verify the model exists - run: `python -c "import google.generativeai as genai; import os; genai.configure(api_key=os.getenv('GOOGLE_API_KEY')); [print(m.name) for m in genai.list_models()]"`
4. Verify your API key is valid

### Slow Response Times

**Problem:** Model is taking too long.

**Solution:**
1. Use `models/gemini-2.0-flash` (fast and stable)
2. Reduce `max_tokens` in config
3. Simplify your instructions

## 💡 Best Practices

1. **Use models/gemini-2.0-flash** for stable, reliable automation
2. **Always include models/ prefix** in model names  
3. **Cache responses** when possible (enabled by default)
4. **Batch operations** to reduce API calls
5. **Monitor usage** at https://ai.dev/usage
6. **Set reasonable retry delays** to avoid hitting limits
7. **Test with experimental models** only after verifying with stable ones

## 📊 Monitoring Usage

Check your usage:
- Dashboard: https://ai.dev/usage?tab=rate-limit
- Monitor requests per minute
- Track token consumption
- View quota limits

## 🚀 Upgrading

If you need higher limits:
1. Visit: https://ai.google.dev/pricing
2. Upgrade to paid tier
3. Get higher rate limits
4. Use advanced models

---

**Default Model:** `models/gemini-2.0-flash` (stable and reliable)  
**Model Format:** Always use `models/` prefix (e.g., `models/gemini-2.0-flash`)  
**Recommended Model:** `models/gemini-2.0-flash` (10 requests/min, stable performance)

**To list all available models:**
```bash
python -c "import google.generativeai as genai; import os; from dotenv import load_dotenv; load_dotenv(); genai.configure(api_key=os.getenv('GOOGLE_API_KEY')); [print(m.name) for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]"
```

