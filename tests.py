import unittest
from unittest.mock import MagicMock
from main import SentimentAssistant

class TestSentimentBot(unittest.TestCase):
    
    def setUp(self):
        """
        This runs before every test. We create a 'fake' AI model 
        so we don't actually call Google servers during testing.
        """
        # 1. Create a fake model object
        self.mock_model = MagicMock()
        
        # 2. Create a fake chat session object inside the model
        self.mock_chat = MagicMock()
        self.mock_model.start_chat.return_value = self.mock_chat
        
        # 3. Initialize our bot with the fake model
        # This prevents the bot from asking for a Real API Key
        self.bot = SentimentAssistant(self.mock_model)

    def test_sentiment_parsing_positive(self):
        """
        Test if the bot correctly splits the AI's response into Mood and Reply.
        """
        # Prepare a fake response from the "AI"
        fake_response = MagicMock()
        fake_response.text = "[STATUS]: Positive\n[MSG]: I am glad to hear that!"
        
        # Tell the fake chat to return this when we send a message
        self.mock_chat.send_message.return_value = fake_response
        
        # Run the actual function
        mood, reply = self.bot.handle_user_input("I love this service")
        
        # Check if our Python logic extracted the text correctly
        self.assertEqual(mood, "Positive")
        self.assertEqual(reply, "I am glad to hear that!")

    def test_history_tracking(self):
        """
        Test if the bot saves the conversation history (Tier 1 Requirement).
        """
        # Simulate a conversation turn
        fake_response = MagicMock()
        fake_response.text = "[STATUS]: Neutral\n[MSG]: Okay."
        self.mock_chat.send_message.return_value = fake_response
        
        self.bot.handle_user_input("Hello")
        
        # Check if the session_data list is not empty
        self.assertTrue(len(self.bot.session_data) > 0)
        
        # Check if the log contains the user's message
        self.assertIn("User said: 'Hello'", self.bot.session_data[0])

if __name__ == '__main__':
    unittest.main()
