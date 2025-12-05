# AI-Powered Sentiment Chatbot

A production-minded Python chatbot that conducts a conversation with a user, performs real-time sentiment analysis using Google's Gemini LLM (Tier 2), and generates a conversational summary of the user's mood (Tier 1).

## 🚀 How to Run (Important)

**Recommended Platform: Google Colab**
The source code (`main.py`) includes specific setup commands (`!pip install`) optimized for cloud environments. Please follow these steps to run it without errors:

1. Open [Google Colab](https://colab.research.google.com/).
2. Create a **New Notebook**.
3. Copy the **entire content** of `main.py` from this repository.
4. Paste it into the Colab code cell.
5. Click the **Play (▶️)** button.
6. When prompted, paste your **Google Gemini API Key** securely into the input box.

*(Note: If running locally on a standard Python terminal, please remove the first line `!pip install...` to avoid syntax errors).*

## 🛠 Chosen Technologies

- **Language:** Python 3
- **Core Engine:** **Google Gemini 2.0 Flash** (via `google-generativeai` library).
- **Security:** `getpass` module for secure, non-visible API key input.

**Why Gemini (LLM) over VADER?**
Standard lexicon libraries (like NLTK/VADER) often fail to detect sarcasm or complex emotional context. By using a Large Language Model, this chatbot understands nuance, slang, and context, providing significantly higher accuracy for the assignment's sentiment requirements.

## 🧠 Explanation of Sentiment Logic

The chatbot uses a **Generative AI** approach with structured prompting:

1. **System Prompting:** The AI is initialized with a specific persona ("Feedback Assistant") and a strict output rule:
   > `[STATUS]: <Sentiment Label>`
   > `[MSG]: <Reply>`
2. **Tier 2 (Statement-Level Analysis):**
   - Every user message is sent to the LLM immediately.
   - The Python script uses string parsing to extract the text after `[STATUS]:`.
   - This allows the bot to display the sentiment (`Positive`, `Negative`, `Neutral`) in real-time alongside the response.
3. **Tier 1 (Conversation-Level Analysis):**
   - The script maintains a local list (`session_data`) of the entire conversation.
   - Upon exit, this full history is sent back to the LLM with a prompt to "summarize the mood trend," generating a sophisticated final report.

## ✅ Status of Tier 2 Implementation

**Status: COMPLETED**
- The chatbot performs sentiment evaluation for **every user message individually**.
- The sentiment (Positive/Negative/Neutral) is displayed in the console immediately after the user types, meeting the real-time requirement.

## 🧪 Tests

A `tests.py` file is included in the repository. It contains unit tests using `unittest.mock` to verify the string parsing logic and history tracking without needing to make actual API calls to Google.

## ✨ Highlights of Innovations (Bonus)

- **LLM Integration:** Replaced standard "bag-of-words" logic with a state-of-the-art Large Language Model for human-like understanding.
- **Robust Parsing:** Implemented a custom parsing system to separate the AI's "internal thought" (Sentiment) from its "external speech" (Reply).
- **Secure Key Handling:** Utilized `getpass` to prevent API keys from being visible in the console or hardcoded in the source file.
        
        
    
