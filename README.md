# 👨‍🍳 Chef Buhari's Kitchen – AI Culinary & Nutritional Consultant

An interactive culinary and nutrition assistant built with **Streamlit**, **LangChain**, and **OpenAI GPT-4o-mini**. The application generates personalized, nutritionally balanced recipes according to specific dietary constraints, target calorie brackets, and serving sizes, preserving conversation context and streaming responses in real time.

---

## 🚀 Key Features

- **Personalized Dietary Filtering:** Supports High-Protein, Keto/Low-Carb, Vegan, Vegetarian, and Gluten-Free preferences.
- **Calorie & Serving Controls:** Dynamically adjusts recipe yields and tracks calorie targets per serving.
- **Structured Recipe Output:** Every suggestion includes prep/cook timing, macro breakdowns (calories, protein, carbs, fats), exact measurements, and chef techniques.
- **Few-Shot Prompt Engineering:** Anchors the LLM output to a consistent format using few-shot prompt examples.
- **Streaming & Context Retention:** Utilizes LangChain's `MessagesPlaceholder` to retain ongoing multi-turn chat history with real-time response streaming.

---

## 🛠️ Tech Stack

- **Frontend / UI:** Streamlit
- **LLM Orchestration:** LangChain Core (`ChatPromptTemplate`, `MessagesPlaceholder`, `StrOutputParser`)
- **LLM Provider:** `langchain-openai` (`gpt-4o-mini`)
- **Environment Management:** `python-dotenv`

---