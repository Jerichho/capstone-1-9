# Together.ai Model Setup Guide

## Model: meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo

### Do You Need a Dedicated Endpoint?

**No!** The "Turbo" suffix indicates this is a **serverless model**, which means:
- ✅ No dedicated endpoint setup required
- ✅ Pay-per-use pricing
- ✅ Instant availability (no waiting for deployment)
- ✅ Automatically scales

### What You Need to Do

1. **Verify Model Availability**
   - Log into your Together.ai account: https://api.together.ai
   - Go to the **Models** section in your dashboard
   - Look for `meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo`
   - Confirm it shows as "Available" or "Serverless"

2. **Check Your API Key**
   - Make sure your `TOGETHER_API_KEY` is set in your `.env` file
   - Verify the API key has access to this model
   - Some models may require a paid account tier

3. **Test the Model**
   - Restart your server
   - Try generating an exam
   - Check the logs for any model availability errors

### If the Model Isn't Available

If you get an error saying the model isn't available, try:

1. **Check Exact Model Name**: 
   - The model name is case-sensitive
   - Make sure you're using: `meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo`
   - Some variants might be: `meta-llama/Llama-3.1-8B-Instruct-Turbo` (without "Meta-")

2. **List Available Models**:
   - Visit: https://api.together.ai/models
   - Or use the Together.ai API to list models programmatically
   - Look for similar Llama 3.1 models

3. **Account Tier**:
   - Some models require specific account tiers
   - Check your Together.ai account settings
   - You may need to upgrade your plan

### When You WOULD Need a Dedicated Endpoint

Only if you see:
- Models WITHOUT "Turbo" suffix (e.g., `meta-llama/Llama-3-8b-chat-hf`)
- Error messages saying "non-serverless model" or "requires dedicated endpoint"
- Very large models (70B+ parameters)

### Quick Test

To verify everything works, you can test with a simple Python script:

```python
from together import Together
import os

client = Together(api_key=os.getenv("TOGETHER_API_KEY"))
response = client.chat.completions.create(
    model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
    messages=[{"role": "user", "content": "Say hello!"}]
)
print(response.choices[0].message.content)
```

If this works, your model is available and configured correctly!
