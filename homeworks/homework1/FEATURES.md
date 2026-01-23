# Features Documentation

## Core Features

### 1. Receipt Recognition
- Upload receipt images (supports JPG, PNG formats)
- Automatically extract the following information:
  - Merchant name
  - Amount paid
  - Date
  - Expense category
  - Item list
  - Tax
  - Discount amount
  - Original amount (before discount)
  - Payment method
  - Merchant address

### 2. Conversational Queries
The agent can answer various questions about uploaded receipts:

#### Supported Query Types

**Total Spending Queries**
- "Total spending?"
- "How much money did I spend in total for these bills?"
- "How much did I spend in total?"
- "What is the total amount across all receipts?"

**Discount-Related Queries**
- "Amount before discount?"
- "How much would I have had to pay without the discount?"
- "How much did I save in total?"
- "What is the total discount amount?"

**Other Queries**
- "Which receipt has the highest spending?"
- "Which store did I spend the most money at?"
- "Group spending by category"
- "What was my spending on a specific date?"

### 3. Smart Query Filtering
The agent automatically determines if a query is related to receipts:

**Relevant Queries** ✅
- Questions about receipts, bills, invoices
- Questions about spending, expenses, costs
- Questions about purchases and payment information
- Financial-related queries

**Irrelevant Queries** ❌
- General questions like weather, news
- Knowledge questions unrelated to receipts
- Other completely unrelated topics

When encountering irrelevant queries, the agent politely declines and explains why.

## Technical Implementation

### 1. Multimodal Recognition
- Uses Google Gemini Vision API to recognize receipt images
- Extracts and stores structured data

### 2. Natural Language Understanding
- Uses Gemini model to understand user query intent
- Determines query relevance
- Generates natural language responses

### 3. Data Management
- Supports storing multiple receipts
- Unified data format
- Easy to query and analyze

## Usage Examples

### Example 1: Basic Query Flow

```
User: [Upload receipt image1]
Agent: ✅ Receipt recognized successfully!
       **Merchant**: Starbucks
       **Amount**: ¥45.50
       **Date**: 2024-01-15
       **Category**: Food & Beverage
       
       Uploaded 1 receipt. You can ask questions about it...

User: What is the total spending?
Agent: Based on the 1 receipt uploaded, your total spending is ¥45.50.
```

### Example 2: Multiple Receipts Query

```
User: [Upload receipt image1]
User: [Upload receipt image2]
User: [Upload receipt image3]

User: How much money did I spend in total for these bills?
Agent: Based on the 3 receipts you've uploaded, your total spending is ¥156.80.
```

### Example 3: Discount Query

```
User: [Upload receipt with discount]

User: How much would I have had to pay without the discount?
Agent: Without the discount, you would have had to pay ¥120.00. 
       With the discount of ¥20.00, you actually paid ¥100.00.
```

### Example 4: Irrelevant Query

```
User: What's the weather like today?
Agent: ⚠️ Sorry, this question is not related to receipts or expenses. I can only answer questions about uploaded receipts.

User: What is artificial intelligence?
Agent: ⚠️ Sorry, this question is not related to receipts or expenses. I can only answer questions about uploaded receipts.
```

## Notes

1. **API Key**: GEMINI_API_KEY must be set to use full functionality
2. **Image Quality**: Clear receipt images yield better recognition results
3. **Query Language**: Supports both Chinese and English queries
4. **Data Persistence**: Current version stores data in memory, clearing on page refresh
