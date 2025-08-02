# Design

# TG Agent Bot
## 1. System Components
### Interface (Aiogram)
1. The bot reacts to all incoming messages (text, forwarded messages, mentions) without explicit commands.
2. Inline buttons are used only for:
   - adding the api key for the llm usage;
   - confirmation of the use of tools;
   - managing explicit memory (e.g., cleaning the current context, deleting or editing a saved record);
   - other bot settings.

### LLM Layer
- **API**: OpenAI and custom API. Possible models: gpt-4.1, gpt-4.1-mini, o4-mini, o3-mini, deepseek-v3, deepseek-r1.
- **Interaction**: `/set_api_key` command for adding the api key for the llm usage, `/model_settings` command for changing the model settings.

### RAG Layer
#### Retrieval Configuration
- **Vector Store**: Chroma for Retrieval.
- **Embeddings**: heavy (ai-sage/Giga-Embeddings-instruct, Qwen3 Embedding-8B, sentence-transformers/paraphrase-multilingual-mpnet-base-v2) or light (minishlab/potion-multilingual-128M, all-MiniLM-L6-v2, intfloat/multilingual-e5-small) for all texts: queries, correspondence, automatic memory, search results.
- **Selection**: top-K fragments, cosine similarity threshold = 0.75
- **Memory optimization**: hierarchical memory: short-term (last N messages) + long-term (RAG), automatic compression of dialogs → summarization of old messages (via LLM).
- **Interaction**: `/clean_context` command for cleaning the current context.
- **Prompt Template**:

#### Fragment Processing
- **Re-Ranking**: sort by score
- **Chunk Fusion**: merge adjacent fragments into ≤2 KB blocks  
- **Deduplication**: drop >80% overlap

#### Prompt Assembly
```
[SYSTEM]
You are an expert agent. Based on the user's query and the provided context from your tools (memory, web search), generate a helpful response.

[CONTEXT]
{context from tools: auto-memory, user-memory, web search results, etc.}

[USER]
{current query}
```

### Tools
### Hybrid Memory
- **Automatic Memory**:
  - For each message, the bot generates an embedding and saves it in the vector store (`source:dialogue`).
  - When generating a response, the top-K most relevant fragments are selected.
- **Explicit Memory**:
  - A separate table in SQLite: `id`, `text`, `category`, `created_at`, `updated_at`.
  - Management commands: `/remember`, `/list_memories`, `/edit_memory`, `/delete_memory`.
  - Filtering by category or tags during retrieval.

### Web Search Module
- **Service**: Google Programmable Search Engine (PSE) or DuckDuckGo API.
- **Caching**: Snippets and titles are cached in the vector store for subsequent retrieval.
- **Filters**: temporary filters.
- **Web Search Schema**:
```
User: "News about quantum computing"
         ↓
[LLM] → Identify the intent of the user and use the web search tool
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
```

### Task and Reminder Manager
- **Storage**: SQLite.
- **Scheduler**: APScheduler for sending reminders to Telegram.
- **Interaction**: Inline buttons for confirmation and deletion.

## 2. Data Flow on Request
### Incoming Request
1. **Receive & Normalize**  
   - Parse text, attachments, metadata  
   - Sanitize inputs (remove unsupported characters)

2. **Context Retrieval (RAG)**  
   - Query vector store (auto-memory, user-memory) → Top-K fragments  
   - (Optional) Web search for external data

3. **Function Registration**  
   - Prepare full list of tools with names, descriptions, JSON schemas   
   - e.g. `web_search`, `memory_read`, `memory_write`, `set_reminder`, `get_stats`

4. **LLM Invocation with Function Calling**  
   - Send user message + retrieved context + `functions` array  
   - Let GPT choose which tool to call based on semantic match  
   - Or return a direct answer if no function is appropriate

5. **Tool Execution**  
   - Parse GPT’s function call JSON  
   - Execute corresponding module (e.g. call `web_search(query)`)  
   - Capture results

6. **Final Response Assembly**  
   - If tool was used: send tool output back to LLM for formatting, then to user  
   - If direct answer: send GPT’s content as-is

7. **Logging & Persistence**  
   - Log request, chosen function (if any), execution time  
   - Store new embeddings or explicit memory entries as needed

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

## 6. Future Enhancements

### 6.1. Dynamic Context Selection
Instead of always fetching a fixed top-K number of fragments, an adaptive selection method can be used. This involves calculating an "entropy score" for chunks to retrieve a more diverse and relevant set of contexts, which can improve response quality, especially for complex queries.

### 6.2. Cross-Encoder Re-Ranking
To improve the precision of retrieved fragments, a re-ranking step can be added after the initial retrieval from the vector store. Cross-encoder models take the user query and each retrieved document as a pair and output a more accurate relevance score. This helps to filter out irrelevant results that might have high cosine similarity but are not semantically aligned with the query's intent.

### 6.3. Iterative Agent Behavior
The data flow described in section 2 is linear. For more complex tasks, a more advanced, iterative (or "multi-step") agent approach can be implemented. This is a common pattern in frameworks like LangChain or LlamaIndex (e.g., ReAct agent).

**How it works:**
1.  **LLM makes a plan**: Instead of just calling one tool, the LLM can create a sequence of steps.
2.  **Execute step-by-step**: The agent executes the first step (e.g., calls a tool).
3.  **Observe and reflect**: The agent gets the result from the tool and adds it to its "scratchpad" or memory. It then analyzes the result.
4.  **Repeat**: Based on the observation, the LLM decides on the next step. This could be calling another tool, refining the query for the same tool, or deciding that it has enough information to answer the user.
5.  **Final Answer**: Once the goal is achieved, the LLM generates the final response.

This allows the agent to solve problems that require multiple tool uses or to self-correct if the initial tool call did not yield the expected results.
