# ==========================================
# 1. SETUP & LIBRARIES
# ==========================================
# We need to install the Google AI library first
!pip install -q -U google-generativeai

import google.generativeai as google_ai
import getpass
import os

# ==========================================
# 2. CONFIGURATION
# ==========================================
print("🔒 SECURE LOGIN")
print("Please paste your Google API Key (starts with AIza):")
# Using getpass hides the key when you paste it for security
my_key = getpass.getpass("Input Key > ")

# Connect to Google's servers
google_ai.configure(api_key=my_key)

# We are using the 'gemini-2.0-flash' model because it is fast and efficient
# Note: Ensure your API key has access to this specific model version
ai_model = google_ai.GenerativeModel('gemini-2.0-flash')

# ==========================================
# 3. THE BOT LOGIC (TIER 1 & 2)
# ==========================================
class SentimentAssistant:
    def __init__(self):
        # This list tracks the conversation for the Tier 1 summary later
        self.session_data = []
        
        # Initialize the chat session
        self.conversation = ai_model.start_chat(history=[])
        
        # SYSTEM PROMPT: This defines the bot's "Personality" and "Rules"
        # I am telling it strictly how to format answers so I can parse them easily
        self.conversation.send_message("""
        INSTRUCTIONS:
        You are a helpful "Feedback Assistant" for a tech company.
        
        For every message I type, you must:
        1. Detect the emotion (Positive, Negative, or Neutral).
        2. Write a polite, professional reply.
        
        STRICT FORMAT REQUIRED:
        [STATUS]: <Sentiment Label>
        [MSG]: <Your Reply>
        
        Do not write anything else.
        """)

    def handle_user_input(self, text_in):
        """
        Tier 2 Implementation: 
        Takes user input, sends to AI, and extracts real-time sentiment.
        """
        try:
            # Send text to Google Gemini
            response = self.conversation.send_message(text_in)
            raw_text = response.text
            
            # Default fallback values
            detected_mood = "Neutral"
            bot_reply = raw_text
            
            # PARSING LOGIC:
            # We split the AI's response by lines to find our tags
            clean_lines = raw_text.split('\n')
            for line in clean_lines:
                if "[STATUS]:" in line:
                    # Remove the tag and clean up spaces/symbols
                    detected_mood = line.replace("[STATUS]:", "").replace("*", "").strip()
                elif "[MSG]:" in line:
                    bot_reply = line.replace("[MSG]:", "").strip()
            
            # Save this turn to our session history (Tier 1 requirement)
            self.session_data.append(f"User said: '{text_in}' -> Mood: {detected_mood}")
            
            return detected_mood, bot_reply
            
        except Exception as error:
            return "Error", f"System Issue: {error}"

    def create_session_report(self):
        """
        Tier 1 Implementation:
        Sends the full chat history back to the AI to get a final summary.
        """
        if not self.session_data:
            return "No data to analyze."
            
        # Join all history into one big string
        full_log = "\n".join(self.session_data)
        
        # Ask the AI to summarize the trend
        prompt = f"""
        Analyze this chat log:
        {full_log}
        
        Task: Give me a 1-sentence summary of how the user's mood changed from start to finish.
        """
        
        try:
            summary_resp = ai_model.generate_content(prompt)
            return summary_resp.text
        except:
            return "Unable to generate report."

# ==========================================
# 4. MAIN EXECUTION LOOP
# ==========================================
def start_program():
    bot = SentimentAssistant()
    
    print("\n" + "▒"*40)
    print("   SENTIMENT ANALYSIS BOT (AI POWERED)")
    print("   Type 'exit' to close the session.")
    print("▒"*40 + "\n")

    while True:
        # Get input
        u_input = input("You > ")
        
        # Exit condition
        if u_input.lower() in ['exit', 'quit', 'bye']:
            break
            
        if not u_input.strip():
            continue

        # --- TIER 2: REAL-TIME OUTPUT ---
        mood, reply = bot.handle_user_input(u_input)
        
        # Print with custom formatting
        print(f"   >>> Sentiment Detected: [{mood}]")
        print(f"   >>> Bot: {reply}")
        print("-" * 30)

    # --- TIER 1: FINAL REPORT ---
    print("\n" + "="*40)
    print("📝 SESSION SUMMARY (Tier 1)")
    print("="*40)
    print("Generating report...")
    final_report = bot.create_session_report()
    print(f"Result: {final_report.strip()}")
    print("="*40)

if __name__ == "__main__":
    start_program()
