# Documentation

# TG Agent Bot
## 1. System Components

### Interface (Aiogram)
- The bot reacts to all incoming messages (text, forwarded messages, mentions) without explicit commands.
- Bot is agent and understand what it has to do (information search, adding to memory, reminder, analyzing forwarded text).
- Inline buttons are used only for confirming or deleting reminders and managing explicit memory (e.g., deleting or editing a saved record).

### Agent Core (Decision-Making)
- **Intent Classifier**: A simple LLM-based function that analyzes the user's message to determine the primary intent. Intents include: `chat`, `web_search`, `remember_data`, `manage_memory`, `create_reminder`.
- **Tool Router**: Based on the identified intent, the agent selects the appropriate tool or sequence of tools. For example, `web_search` intent triggers the `Web Search Module`.
- **Orchestrator**: The central logic (`agent/agent.py`) that executes the selected tools, gathers context (from memory and tools), and passes it to the LLM for final response generation.

### RAG Layer
- **Vector Store**: Chroma for Retrieval.
- **Embeddings**: NV-Embed (NVIDIA), BAAI/bge-small-en-v1.5 or ntfloat/e5-small-v2 for all texts: queries, correspondence, automatic memory, search results.
- **Prompt Template**:
  ```
  [SYSTEM]
  You are an expert agent. Based on the user's query and the provided context from your tools (memory, web search), generate a helpful response.

  [CONTEXT]
  {context from tools: auto-memory, user-memory, web search results, etc.}

  [USER]
  {current query}
  ```

### Task and Reminder Manager
- **Storage**: SQLite.
- **Scheduler**: APScheduler for sending reminders to Telegram.
- **Interaction**: Inline buttons for confirmation and deletion.

### Web Search Module
- **Service**: Google Programmable Search Engine (PSE) + Custom Search JSON API or DuckDuckGo API.
- **Caching**: Snippets and titles are cached in the vector store for subsequent retrieval.

### Web Search Schema 
User: "News about quantum computing"
         ↓
[Intent Analysis] → Is this a search? → Yes
         ↓
[Cache/Memory check] → No recent data available
         ↓
[Web search: Google PSE / DDG] → 10 results
         ↓
[Cleaning + extracting snippets]
         ↓
[Extension: parsing 2 pages] → +200 words of context
         ↓
[Saving in Chroma] → source:web_search
         ↓
[RAG: Retrieval from web + auto + user memory]
         ↓
[LLM] → Response Generation
         ↓
[Reply to user + links]
         ↓
[Saving the dialog to auto-memory]
### Tools
### Hybrid Memory
- **Automatic Memory**:
  - For each message, the bot generates an embedding and saves it in the vector store (`source:dialogue`).
  - When generating a response, the top-K most relevant fragments are selected.
- **Explicit Memory**:
  - A separate table in SQLite: `id`, `text`, `category`, `created_at`, `updated_at`.
  - Management commands: `/remember`, `/list_memories`, `/edit_memory`, `/delete_memory`.
  - Filtering by category or tags during retrieval.

## 2. Data Flow on Request
1.  Input from the user (text, forwarded content, or command).
2. 
3. 

## 3. Step-by-step Implementation (MVP Iterations)


## 4. Key Prompting Tips

- **Chain-of-Thought**: Ask the agent to explain its thought process.
- **Role Instructions**: "You are a friendly expert assistant, ..."
- **Length Control**: `max_tokens` + "If it's too long, provide a brief summary."
- **Debug Output**: For development, include retrieved snippets and similarity scores.

## 5. File Architecture

```
rag_agent_bot/
├── bot.py                  # Entry point: Aiogram initialization, bot startup
├── config.py               # Settings (API keys, RAG parameters, DB)
├── handlers/               # Telegram event handlers
│   ├── __init__.py
│   ├── message_handlers.py # Handling text and forwarded messages
│   └── callback_handlers.py# Managing reminders and memory via inline buttons
├── middlewares/            # Custom middlewares for Aiogram
│   ├── __init__.py
│   ├── throttling.py       # Spam protection (rate limiting)
│   └── context.py          # Saving user context for hybrid memory
├── memory/
│   ├── auto_memory.py      # Working with the vector store (Chroma)
│   └── user_memory.py      # CRUD for explicit memory
├── tasks/
│   └── reminders.py        # APScheduler logic
├── search/
│   └── web_search.py       # SerpAPI wrapper / parsers
├── rag_pipeline/
│   └── rag.py              # Combining Retrieval and Generation
├── db/
│   └── models.py           # SQLAlchemy models or Redis client
├── utils/
│   ├── nlp_utils.py        # Intent classifier, embeddings
│   └── prompt_templates.py # RAG prompt templates
├── tests/
│   ├── test_memory.py
│   ├── test_rag.py
│   └── test_bot.py
├── requirements.txt
└── README.md
```
