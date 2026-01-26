# Receipt Recognition Agent

An intelligent receipt recognition system that automatically extracts expense information from receipt images.

## Features

-  **Receipt Recognition**: Upload receipt images (JPG, PNG) and automatically extract ALL expense information
-  **Multilingual Support**: Reads both English and Chinese text on receipts
-  **Conversational Queries**: Ask questions about receipts, such as:
  - "Total spending?" / "How much money did I spend in total for these bills?"
  - "Amount before discount?" / "How much would I have had to pay without the discount?"
  - "What did I buy?" / "Show me all items purchased"
-  **Smart Filtering**: Automatically rejects irrelevant queries
-  **Multiple Receipts**: Upload multiple receipts for unified query and management
-  Uses Google Gemini Vision API for multimodal recognition and natural language understanding
-  Automatically extracts:
  - Merchant name, amount, date
  - Expense category
  - Item list
  - Tax amount
  - Discount information (with minus signs)
  - Original amount (before discounts)
  - Payment method
  - Merchant address
-  User-friendly Gradio web interface with conversational interaction
-  **English Interface**: All text and queries are in English; receipts can be in any language

## Installation

### 1. Clone or Download the Project

```bash
cd homework1
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Vertex API Key

**Create .env File**

1. Create a `.env` file in the project root
2. Add the following:
   ```
   VERTEX_API_KEY=your_vertex_api_key
   ```
   Or (if using a different environment variable name):
   ```
   GEMINI_API_KEY=your_vertex_api_key
   ```


**Note:** This project uses Vertex AI and requires `vertexai=True` parameter

### 4. Run the Program

```bash
python receipt_agent.py
```

After starting, open the displayed address in your browser (usually `http://localhost:7860`)

## Usage

### 1. Upload Multiple Receipts
- Click the upload button, you can select multiple receipt images at once (hold Ctrl/Cmd to multi-select)
- The system supports batch upload
- Receipts can contain English and/or Chinese text

### 2. Enter Query
Enter your question in the text box, for example:
- **Total spending query**: "How much money did I spend in total for these bills?"
- **Discount query**: "How much would I have had to pay without the discount?"
- **Item query**: "What items did I purchase on each receipt?"
- **Merchant query**: "What are the merchant names?"
- **Date query**: "When did I make these purchases?"

### 3. Submit Query
- Click "Submit" button
- The system processes all uploaded images and answers the question
- If the question is not related to receipts, the system politely declines

### 4. Clear Conversation
- Click "Clear" button to clear conversation history

## Project Structure

```
homework1/
├── receipt_agent.py          # Main program file
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── FEATURES.md               # Detailed features documentation
├── images/                   # Sample images directory
│   └── *.jpg                 # Sample receipt images
└── HW1 report.pdf            # Report for the homework1
```

## Tech Stack

- **Python 3.8+**
- **Gradio**: Web interface framework
- **LangChain Google GenAI**: Vertex AI integration
- **Vertex AI Gemini**: Multimodal AI model (via Vertex API)
- **Pillow**: Image processing
- **Pydantic**: Data validation


## Notes

- **Based on notebook implementation**: Uses helper functions and image input from notebook
- **Vertex AI**: Uses Vertex API instead of regular Gemini API
- **Multi-image support**: Can upload multiple receipt images and ask questions
- Ensure receipt images are clear with visible text
- **Multilingual**: Interface is English; reads both English and Chinese on receipts
- **Currency**: Supports USD ($), RMB (¥), and other currencies
- If VERTEX_API_KEY is not set, the program runs in mock mode (for interface testing only)
- Use clear receipt photos for best recognition results
- Discount amounts are shown with minus signs (e.g., -$20.00, -¥50)

## Troubleshooting

### Issue: "VERTEX_API_KEY not set" warning

**Solution:**
1. Check if `.env` file exists
2. Verify `VERTEX_API_KEY` or `GEMINI_API_KEY` is correctly set in `.env`
3. Ensure API key is valid
4. Confirm `langchain-google-genai` and `langchain-core` are installed

### Issue: Recognition results are inaccurate

**Solution:**
1. Use clearer images
2. Ensure receipt text is fully visible
3. Try adjusting image angle and lighting
4. Make sure both English and Chinese text is legible

### Issue: Program cannot start

**Solution:**
1. Check Python version (3.8+ required)
2. Confirm all dependencies are installed: `pip install -r requirements.txt`
3. Check if port 7860 is occupied

## References

- [Google Gemini API Documentation](https://ai.google.dev/docs)
- [Gradio Documentation](https://www.gradio.app/docs/)
- [Google Finance Tracker Project](https://ai.google.dev/competition/projects/finance-tracker?hl=en)

## License

This project is for learning and assignment purposes only.
