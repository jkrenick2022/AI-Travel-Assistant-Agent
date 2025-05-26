# 🧠 AI Travel Assistant Agent

This project is an interactive AI Agent built with **LangGraph**, designed to help users search the internet for travel-related information. It takes user queries, rewrites them into effective search prompts, performs a live DuckDuckGo search, and formats the results into a structured, helpful travel guide — all powered by OpenAI and LangChain tools.

---

## 🚀 Features

- 🔍 Rewrites user input into optimized search queries  
- 🌐 Performs live internet searches using DuckDuckGo  
- 📝 Formats raw search results into human-friendly travel summaries  
- 🧠 Modular LangGraph design for clear logic and routing  
- 🤖 LLM-powered by OpenAI with real-time CLI interaction

---

## 📁 Project Structure

```plaintext
.
├── main.py                  # Entry point: builds and runs the LangGraph agent
├── pyproject.toml           # Project dependencies (used with uv or poetry)
├── uv.lock                  # Lock file for uv-based environment
├── .gitignore               # Specifies files/folders to exclude from Git
├── .python-version          # Optional: specifies Python version
├── README.md                # This file
```


> ⚠️ `.env` is used to store your OpenAI API key and must **not** be committed to GitHub.

---

## 🔧 Setup Instructions

```bash 
# 1. Clone the repo
git clone https://github.com/your-username/your-repo.git
cd your-repo

# 2. Install dependencies with `uv`
uv pip install -r pyproject.toml

# 3. Create a `.env` file
echo "OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" > .env

# 4. Run the agent
python main.py
```

---

## 🧪 How It Works

1. **User enters a search query**  
   Example: `"Things to do in Tokyo in summer"`

2. **Agent rewrites the input**  
   The LLM reformulates the query into a concise search-friendly version.

3. **Performs a DuckDuckGo search**  
   The cleaned-up query is passed to the `DuckDuckGoSearchResults` tool to retrieve real-time web data.

4. **Formats the results**  
   The LLM converts raw search output into a structured travel guide with:
   - ✅ Overview of the location
   - 📍 Places to visit
   - 🎯 Things to do
   - 💡 Fun facts (if any)
   - 🔗 List of sources

5. **Returns the final response**  
   The user sees a well-organized summary in the terminal or console.

---


## 📜 License

This project is for educational/demo purposes. Use responsibly when working with LLMs and sensitive data.

---

## 🤝 Acknowledgements

- [LangGraph](https://github.com/langchain-ai/langgraph)  
- [LangChain](https://github.com/langchain-ai/langchain)  
- [OpenAI](https://openai.com)
