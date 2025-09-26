# AI Web Assistant

When Ollama dropped their web search API, I knew I had to build something with it immediately. This is a clean, practical implementation that shows how powerful local AI becomes when you give it access to real-time web data.

If you're curious about AI, want to see what's possible with modern tools, or need a starting point for your own projects - this is for you.

## What you get

The core idea was simple: what if your AI could actually look things up instead of just guessing? Here's what I built:

- **Live web search** - Ask about current events, latest tech news, or anything recent and watch it search the web in real-time
- **Better answers** - No more "my knowledge cutoff" responses. The AI can fact-check itself and give you current information
- **See the thinking** - Toggle on the reasoning process to understand how the AI approaches problems
- **Conversation memory** - Your chat history persists, so you can build on previous discussions
- **Simple interface** - Clean Streamlit UI that just works, no complicated setup

## Getting started

I tried to make this as straightforward as possible. Here's what you need:

**1. Install the basics**
```bash
pip install streamlit ollama python-dotenv
```

**2. Get your Ollama API key**
Head to [ollama.com](https://ollama.com) and sign up - they have a generous free tier for the web search API.

**3. Add your API key**
Create a `.env` file and drop in your key:
```
OLLAMA_API_KEY=your_ollama_api_key_here
```

**4. Make sure Ollama is running**
You'll need Ollama installed locally with the qwen3:4b model. If you haven't done this before, check out Ollama's documentation - it's pretty painless.

## Running it

```bash
streamlit run main.py
```

Open your browser to the local URL and you're good to go. The interface is pretty intuitive:

- Toggle web search on/off depending on whether you want current info
- Enable "Show AI Thinking" if you want to see how it reasons through problems  
- Clear chat when you want to start fresh
- Just start typing and watch it work

## Why I built this

I've been fascinated by the problem of AI hallucinations - you know, when AI confidently tells you something completely wrong. Ollama's web search API felt like a breakthrough moment.

Being able to give a local AI model access to current information changes everything. Instead of "I don't know about events after my training cutoff," you get real answers about what's happening right now. 

It's not just useful for current events - try asking it to fact-check claims, research recent developments in your field, or help with decisions that need up-to-date information. The difference is night and day.

## Technical notes

A few things I focused on while building this:

- **Context awareness**: Automatically includes current date/time so the AI knows when "now" is
- **Tool integration**: Clean handling of web search and fetch operations
- **Error handling**: Graceful fallbacks when things go wrong
- **Session persistence**: Your conversation survives page refreshes
- **Mobile friendly**: Works well on phones and tablets

## What's under the hood

- **[Streamlit](https://streamlit.io/)** for the web interface - fast to build, easy to deploy
- **[Ollama](https://ollama.ai/)** for AI model integration and their new web search API
- **[python-dotenv](https://pypi.org/project/python-dotenv/)** for clean environment management

## What's next

This is a starting point. Fork it, modify it, build something better. I'd love to see what you create with Ollama's web search capabilities.

---

*Built by [lesteroliver](https://www.linkedin.com/in/lesteroliver/) - always curious about what's possible with AI*
