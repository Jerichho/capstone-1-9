# Model Setup Guide

## Issue: Model Not Available

If you're getting errors like "model_not_available" or "Unable to access model", the model name in the config doesn't match what's available in your Together.ai account.

## Quick Fix

1. **Check Available Models**: Visit https://api.together.ai/models to see which models are available with your API key.

2. **Update Model in `.env` file**: Create or edit `.env` in the project root:

```env
LLM_MODEL=your-model-name-here
```

3. **Common Serverless Models** (check availability):
   - `meta-llama/Llama-3.2-3B-Instruct-Turbo`
   - `meta-llama/Llama-3.1-8B-Instruct-Turbo` 
   - `Qwen/Qwen2.5-7B-Instruct`
   - `mistralai/Mixtral-8x7B-Instruct-v0.1`
   - `arize-ai/qwen-2-1.5b-instruct` (small but worked before)

## Finding Your Available Models

You can also check via Together.ai dashboard:
1. Log in to https://api.together.ai
2. Go to Models section
3. Look for models marked as "Serverless" or "Available"
4. Copy the exact model name and add it to `.env`

## Testing a Model

After updating `.env`, restart your server and try generating an exam. The error messages will tell you if the model is still not available.

## Fallback

If none of the larger models work, you can temporarily use:
```env
LLM_MODEL=arize-ai/qwen-2-1.5b-instruct
```

This model worked before, but it's smaller and may generate less unique questions.
