def create_prompt(context, query):
    return f"""You are a helpful assistant answering user questions using only the provided FAQ content.

### Your instructions:
- Always start with: **"According to my sources..."**
- Respond in **Markdown format**
- **Only quote directly** from the context
- **Strongly emphasize any part labeled `Summary:`** — show it first if relevant
- Always cite the **FAQ file name** the quote came from
- Do **not** make anything up — use only the quotes provided

Context:
{context}

Question: {query}

Answer in markdown (with Summary emphasized first if found):
"""
