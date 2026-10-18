import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser

# 1. Page Configuration
st.set_page_config(page_title="Chef Buhari's Kitchen", page_icon="👨‍🍳", layout="wide")

# 2. Load API Key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("Missing `OPENAI_API_KEY`. Please configure your `.env` file.")
    st.stop()

# 3. Sidebar: Preferences & Controls
with st.sidebar:
    st.title("👨‍🍳 Kitchen Setup")
    
    diet_pref = st.selectbox(
        "Dietary Preference",
        ["None (Standard)", "High-Protein", "Keto / Low-Carb", "Vegan", "Vegetarian", "Gluten-Free"]
    )
    
    calorie_target = st.select_slider(
        "Target Calories per Serving",
        options=["Light (< 350 kcal)", "Moderate (350 - 600 kcal)", "Hearty (> 600 kcal)", "Any"],
        value="Moderate (350 - 600 kcal)"
    )

    servings = st.number_input("Default Servings", min_value=1, max_value=10, value=2, step=1)

    st.markdown("---")
    if st.button("Clear Conversation 🧹", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# 4. Model and Pipeline Definition
@st.cache_resource
def get_chain():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

    system_prompt = (
        "You are Chef Buhari, an elite culinary chef and certified nutritional consultant. "
        "Whenever recommending dishes, you must provide BOTH culinary excellence AND reliable nutritional calculations.\n\n"
        "Active constraints:\n"
        "- Dietary Preference: {diet_preference}\n"
        "- Target Calorie Band: {calorie_band}\n"
        "- Servings: {serving_count}\n\n"
        "Format every recipe strictly using this layout:\n"
        "### 🍽️ [Dish Name]\n"
        "⏱️ **Prep Time:** [X mins] | 🍳 **Cook Time:** [Y mins] | 👥 **Servings:** [Z]\n\n"
        "📊 **Nutrition (Per Serving Estimate):**\n"
        "- **Calories:** ~[X] kcal\n"
        "- **Protein:** [P]g | **Carbs:** [C]g | **Fats:** [F]g\n\n"
        "🛒 **Key Ingredients:**\n"
        "- [Ingredient with exact quantity]\n\n"
        "👨‍🍳 **Preparation Highlights:**\n"
        "1. [Clear, numbered instruction]\n\n"
        "💡 **Chef's Secret Tip:** [Specific chef technique or substitution]"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        # Few-Shot Example
        ("human", "Give me a quick egg breakfast"),
        (
            "ai",
            "### 🍽️ Mediterranean Scramble with Spinach & Feta\n"
            "⏱️ **Prep Time:** 5 mins | 🍳 **Cook Time:** 6 mins | 👥 **Servings:** 2\n\n"
            "📊 **Nutrition (Per Serving Estimate):**\n"
            "- **Calories:** ~290 kcal\n"
            "- **Protein:** 18g | **Carbs:** 4g | **Fats:** 22g\n\n"
            "🛒 **Key Ingredients:**\n"
            "- 4 large pasture-raised eggs\n"
            "- 1 cup baby spinach, chopped\n"
            "- 30g crumbled feta cheese\n"
            "- 1 tbsp extra virgin olive oil\n"
            "- Pinch of sea salt and red pepper flakes\n\n"
            "👨‍🍳 **Preparation Highlights:**\n"
            "1. Sauté spinach in olive oil over medium-low heat until just wilted (1 minute).\n"
            "2. Pour in lightly beaten eggs; stir gently in folds from outer edges inward.\n"
            "3. Fold in feta right before the eggs finish setting so it warms through without melting away.\n\n"
            "💡 **Chef's Secret Tip:** Remove the pan from heat while eggs are still slightly glossy; residual heat finishes the cook without making them rubbery."
        ),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{user_question}")
    ])

    return prompt | llm | StrOutputParser()

chain = get_chain()

# 5. Chat History State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Header
st.title("👨‍🍳 Buhari's Kitchen")
st.caption(f"Active Mode: **{diet_pref}** | Target: **{calorie_target}** | Servings: **{servings}**")

# 6. Display Historical Messages
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.markdown(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant", avatar="👨‍🍳"):
            st.markdown(msg.content)

# 7. Real-Time Chat Input & Streaming
if user_input := st.chat_input("Ask for recipes, dietary tweaks, or nutritional breakdowns..."):
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append(HumanMessage(content=user_input))

    with st.chat_message("assistant", avatar="👨‍🍳"):
        response_stream = chain.stream({
            "diet_preference": diet_pref,
            "calorie_band": calorie_target,
            "serving_count": servings,
            "history": st.session_state.messages[:-1],
            "user_question": user_input
        })
        full_response = st.write_stream(response_stream)

    st.session_state.messages.append(AIMessage(content=full_response))