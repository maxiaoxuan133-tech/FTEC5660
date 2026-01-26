# Features Documentation

## Core Features

### 1. Receipt Recognition
- Upload receipt images (supports JPG, PNG formats)
- Automatically extract ALL information from receipts (supports both English and Chinese text):
  - **Merchant name** (商家名称)
  - **Amount paid** / Final total (实付金额)
  - **Date** of purchase (消费日期)
  - **Expense category** (消费类别) - e.g., Food, Shopping, Transportation
  - **Item list** (商品列表) - what was purchased
  - **Tax amount** (税费)
  - **Discount amounts** (折扣金额) - shown with minus signs like -$20.00, -¥50
  - **Original amount** BEFORE discounts (原价)
  - **Payment method** (支付方式) - cash, card, mobile pay, etc.
  - **Merchant address** (商家地址)

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
- "What are the individual discounts on each receipt?"

**Individual Receipt Queries**
- "What did I buy on each receipt?"
- "Show me all the items purchased"
- "What are the merchant names?"
- "When did I make these purchases?"
- "What payment methods were used?"

**Analysis Queries**
- "Which receipt has the highest spending?"
- "Which store did I spend the most money at?"
- "Group spending by merchant"
- "How many receipts are there?"

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
- Supports **multilingual text** (English and Chinese)
- Extracts and stores structured data

### 2. Natural Language Understanding
- Uses Gemini model to understand user query intent
- Determines query relevance
- Generates natural language responses in English

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
       **Amount**: $45.50
       **Date**: 2024-01-15
       **Category**: Food & Beverage
       **Items**: 2x Coffee, 1x Sandwich

       Uploaded 1 receipt. You can ask questions about it...

User: What is the total spending?
Agent: Based on the 1 receipt uploaded, your total spending is $45.50.
```

### Example 2: Multiple Receipts Query

```
User: [Upload receipt image1]
User: [Upload receipt image2]
User: [Upload receipt image3]

User: How much money did I spend in total for these bills?
Agent: Based on the 3 receipts you've uploaded, your total spending is $156.80.
```

### Example 3: Discount Query (with Chinese Receipt)

```
User: [Upload receipt with discount]

User: How much would I have had to pay without the discount?
Agent: Based on the receipt:
       - Original Amount: $120.00
       - Discounts: -$20.00
       - Final Total: $100.00

       Without the discount, you would have had to pay $120.00.
```

### Example 4: Detailed Item Query

```
User: What items did I purchase on each receipt?
Agent: Here's what you purchased:

Receipt 1 (Starbucks):
- 2x Coffee ($8.00 each)
- 1x Sandwich ($12.50)

Receipt 2 (Walmart):
- 1x Shirt ($35.00)
- 2x Pants ($45.00 each)
```

### Example 5: Irrelevant Query

```
User: What's the weather like today?
Agent: ⚠️ Sorry, this question is not related to receipts or expenses. I can only answer questions about uploaded receipts.

User: What is artificial intelligence?
Agent: ⚠️ Sorry, this question is not related to receipts or expenses. I can only answer questions about uploaded receipts.
```

## Notes

1. **API Key**: VERTEX_API_KEY must be set to use full functionality
2. **Image Quality**: Clear receipt images yield better recognition results
3. **Multilingual Support**: Receipts can contain both English and Chinese text - the agent reads both
4. **Query Language**: Interface is in English; receipts can be in any language
5. **Data Persistence**: Current version stores data in memory, clearing on page refresh
6. **Currency**: Supports USD ($), RMB (¥), and other currencies
7. **Discount Format**: Discounts are shown with minus signs (e.g., -$20.00, -¥50)
