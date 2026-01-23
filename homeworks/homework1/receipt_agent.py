"""
Receipt Recognition Agent - Notebook-based implementation
Using Vertex AI Gemini API, supports multiple image uploads and queries
"""

import os
import json
import base64
import mimetypes
from typing import Optional, Dict, Any, List
from datetime import datetime
from PIL import Image
import gradio as gr
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# LangChain imports for Vertex AI
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.messages import HumanMessage
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    print("Warning: langchain_google_genai is not installed. Please run: pip install langchain-google-genai langchain-core")

# Load environment variables
load_dotenv()

# Vertex API configuration
VERTEX_API_KEY = os.getenv("VERTEX_API_KEY", os.getenv("GEMINI_API_KEY", ""))


# ============================================================================
# Helper Functions (from notebook)
# ============================================================================

def image_to_base64(img_path: str) -> str:
    """
    Helper function to read and encode image to base64
    From notebook Cell 9
    """
    with open(img_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')


def get_image_data_url(image_path: str) -> str:
    """
    Helper function to encode local file to Base64 Data URL
    From notebook Cell 9
    """
    # Guess the mime type (e.g., image/png, image/jpeg) based on file extension
    mime_type, _ = mimetypes.guess_type(image_path)
    if mime_type is None:
        mime_type = "image/png"  # Default fallback
    
    encoded_string = image_to_base64(image_path)
    
    # Construct the Data URL
    return f"data:{mime_type};base64,{encoded_string}"


def pil_image_to_data_url(pil_image: Image.Image) -> str:
    """
    Convert PIL Image to data URL
    """
    import io
    # Determine format
    format_map = {
        'JPEG': 'image/jpeg',
        'PNG': 'image/png',
        'GIF': 'image/gif',
        'WEBP': 'image/webp'
    }
    img_format = pil_image.format or 'PNG'
    mime_type = format_map.get(img_format, 'image/png')
    
    # Convert to bytes
    buffer = io.BytesIO()
    pil_image.save(buffer, format=img_format)
    img_bytes = buffer.getvalue()
    
    # Encode to base64
    encoded_string = base64.b64encode(img_bytes).decode('utf-8')
    
    return f"data:{mime_type};base64,{encoded_string}"


# ============================================================================
# Data Models
# ============================================================================

class ExpenseInfo(BaseModel):
    """Expense information data model"""
    merchant: str = Field(description="Merchant name")
    amount: float = Field(description="Amount")
    date: str = Field(description="Date (YYYY-MM-DD format)")
    category: str = Field(description="Expense category (e.g., Food, Shopping, Transportation)")
    items: Optional[str] = Field(default=None, description="List of purchased items")
    tax: Optional[float] = Field(default=None, description="Tax amount")
    total: Optional[float] = Field(default=None, description="Total amount")
    discount: Optional[float] = Field(default=None, description="Discount amount")
    original_amount: Optional[float] = Field(default=None, description="Amount before discount")
    payment_method: Optional[str] = Field(default=None, description="Payment method")
    address: Optional[str] = Field(default=None, description="Merchant address")


# ============================================================================
# Receipt Agent
# ============================================================================

class ReceiptAgent:
    """Receipt Recognition Agent - Notebook-based implementation with Vertex AI and multi-image query support"""
    
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        """Initialize Agent"""
        self.model_name = model_name
        self.llm = None
        
        if not LANGCHAIN_AVAILABLE:
            print("Warning: langchain_google_genai is not installed, cannot use Vertex API")
            return
        
        if VERTEX_API_KEY:
            try:
                # Use Vertex AI (from notebook Cell 10)
                self.llm = ChatGoogleGenerativeAI(
                    model=model_name,
                    api_key=VERTEX_API_KEY,
                    temperature=0,
                    vertexai=True  # Key: Enable Vertex AI
                )
                print(f"Initialized Vertex AI model: {model_name}")
            except Exception as e:
                print(f"Failed to initialize Vertex AI: {e}")
                self.llm = None
        else:
            print("Warning: VERTEX_API_KEY not set, will use mock mode")
    
    def process_multiple_receipts_with_query(
        self, 
        image_paths: List[str], 
        query: str
    ) -> Dict[str, Any]:
        """
        Process multiple receipt images and a query simultaneously
        Based on notebook Cell 14 implementation
        
        Args:
            image_paths: List of image paths
            query: User query
            
        Returns:
            Dictionary containing answer and relevance
        """
        if not self.llm:
            return self._mock_query_response(query, len(image_paths))
        
        if not image_paths:
            return {
                "success": False,
                "answer": "Please upload at least one receipt image",
                "is_relevant": True
            }
        
        if not query or not query.strip():
            return {
                "success": False,
                "answer": "Please enter your question",
                "is_relevant": True
            }
        
        try:
            # Check query relevance
            relevance_check = self._check_query_relevance(query)
            if not relevance_check["is_relevant"]:
                return {
                    "success": False,
                    "answer": relevance_check["reason"],
                    "is_relevant": False
                }
            
            # Prepare image data URLs
            image_data_urls = []
            for img_path in image_paths:
                if isinstance(img_path, str) and os.path.exists(img_path):
                    data_url = get_image_data_url(img_path)
                elif isinstance(img_path, Image.Image):
                    data_url = pil_image_to_data_url(img_path)
                else:
                    continue
                image_data_urls.append(data_url)
            
            if not image_data_urls:
                return {
                    "success": False,
                    "answer": "Cannot process uploaded images. Please ensure they are valid image files.",
                    "is_relevant": True
                }
            
            # Build prompt (based on notebook Cell 14)
            # Dynamically build prompt containing multiple images
            human_message_parts = [
                {"type": "text", "text": query}
            ]
            
            # Add all images
            for i, data_url in enumerate(image_data_urls, 1):
                human_message_parts.append({
                    "type": "image_url",
                    "image_url": {"url": data_url}
                })
            
            # Use ChatPromptTemplate (from notebook)
            prompt = ChatPromptTemplate.from_messages([
                ("system", "You are a helpful assistant that analyzes receipts and answers questions about expenses. "
                          "When asked about receipts, provide accurate information based on the images provided. "
                          "If the question is not related to receipts or expenses, politely decline."),
                ("human", human_message_parts),
            ])
            
            # Create chain and invoke
            chain = prompt | self.llm
            response = chain.invoke({})
            
            answer = response.content if hasattr(response, 'content') else str(response)
            
            return {
                "success": True,
                "answer": answer,
                "is_relevant": True,
                "images_processed": len(image_data_urls)
            }
            
        except Exception as e:
            return {
                "success": False,
                "answer": f"Error processing query: {str(e)}",
                "is_relevant": True,
                "error": str(e)
            }
    
    def _check_query_relevance(self, query: str) -> Dict[str, Any]:
        """
        Check if query is related to receipts/expenses using LLM
        """
        if not self.llm:
            # Simple keyword check
            relevant_keywords = [
                "receipt", "bill", "expense", "spend", "amount", "money", "payment",
                "purchase", "cost", "total", "discount", "discounted", "price"
            ]
            question_lower = query.lower()
            is_relevant = any(keyword in question_lower for keyword in relevant_keywords)
            
            if not is_relevant:
                return {
                    "is_relevant": False,
                    "reason": "This question is not related to receipts or expenses. I can only answer questions about receipts."
                }
            return {"is_relevant": True, "reason": ""}
        
        # Use LLM to check relevance
        try:
            prompt = ChatPromptTemplate.from_messages([
                ("system", "You are a query relevance checker. Determine if a question is related to receipts, bills, expenses, or financial transactions."),
                ("human", "Is this question related to receipts, bills, expenses, or financial transactions?\n\nQuestion: {query}\n\nAnswer only 'YES' or 'NO', then briefly explain why.")
            ])
            
            chain = prompt | self.llm
            response = chain.invoke({"query": query})
            response_text = response.content if hasattr(response, 'content') else str(response)
            
            if "NO" in response_text.upper() or "irrelevant" in response_text.lower():
                reason = response_text.split(":", 1)[-1].strip() if ":" in response_text else "This question is not related to receipts or expenses."
                return {
                    "is_relevant": False,
                    "reason": f"Sorry, {reason} I can only answer questions about receipts."
                }
            
            return {"is_relevant": True, "reason": ""}
            
        except Exception as e:
            # Fallback to simple check if LLM fails
            return self._check_query_relevance(query)
    
    def _mock_query_response(self, query: str, num_images: int) -> Dict[str, Any]:
        """Mock query response (for testing without API key)"""
        query_lower = query.lower()
        
        if "total" in query_lower or "sum" in query_lower or "spent" in query_lower:
            return {
                "success": True,
                "answer": f"Based on the {num_images} receipt image(s) uploaded, your total spending is approximately ¥{num_images * 100:.2f}.",
                "is_relevant": True,
                "images_processed": num_images
            }
        
        if "discount" in query_lower or "without" in query_lower or "original" in query_lower:
            return {
                "success": True,
                "answer": f"Based on the {num_images} receipt image(s) uploaded, the total before discount is approximately ¥{num_images * 120:.2f}, and you paid approximately ¥{num_images * 100:.2f}, saving approximately ¥{num_images * 20:.2f}.",
                "is_relevant": True,
                "images_processed": num_images
            }
        
        return {
            "success": True,
            "answer": f"Processed {num_images} receipt image(s). Please ask more specific questions like: What is the total spending? What is the amount before discount?",
            "is_relevant": True,
            "images_processed": num_images
        }


# ============================================================================
# Global Agent Instance
# ============================================================================

_agent = None

def get_agent() -> ReceiptAgent:
    """Get global Agent instance"""
    global _agent
    if _agent is None:
        _agent = ReceiptAgent()
    return _agent


# ============================================================================
# Gradio Interface Functions
# ============================================================================

def process_receipts_and_query(images, query, history):
    """
    Process multiple receipt images and a query
    
    Args:
        images: List of file objects returned by Gradio File component
        query: User query
        history: Conversation history
        
    Returns:
        Updated conversation history
    """
    agent = get_agent()
    
    # Process image input - Gradio File component returns file object list
    image_paths = []
    
    if images is None or (isinstance(images, list) and len(images) == 0):
        return history, "Please upload at least one receipt image."
    
    # Gradio File component returns file objects, need to read paths
    file_list = images if isinstance(images, list) else [images]
    
    try:
        for file_obj in file_list:
            if file_obj is None:
                continue
            
            # Gradio File component returns file objects with 'name' attribute
            if hasattr(file_obj, 'name'):
                file_path = file_obj.name
            elif isinstance(file_obj, str):
                file_path = file_obj
            else:
                continue
            
            if os.path.exists(file_path):
                image_paths.append(file_path)
        
        if not image_paths:
            return history, "Cannot process uploaded images. Please ensure they are valid image files."
        
        if not query or not query.strip():
            return history, "Please enter your question."
        
        # Add user query to conversation history
        query_text = f"📸 Uploaded {len(image_paths)} receipt image(s)\n\n**Question**: {query}"
        if not history:
            history = []
        history.append({"role": "user", "content": query_text})
        
        # Add loading indicator message
        loading_message = "🔄 Analyzing receipts... This may take 30-60 seconds for multiple images."
        history.append({"role": "assistant", "content": loading_message})
        
        # Process query
        result = agent.process_multiple_receipts_with_query(image_paths, query)
        
        # Remove loading message and add actual response
        history.pop()
        
        # Add response
        if result["success"]:
            answer = result["answer"]
            if not result.get("is_relevant", True):
                answer = f"⚠️ {answer}"
        else:
            answer = result.get("answer", "Sorry, I couldn't answer this question.")
            if not result.get("is_relevant", True):
                answer = f"⚠️ {answer}"
        
        history.append({"role": "assistant", "content": answer})
        
        return history, ""
        
    except Exception as e:
        import traceback
        error_msg = f"Error: {str(e)}"
        return history, error_msg


def clear_conversation():
    """Clear conversation"""
    return []


def create_gradio_interface():
    """Create Gradio interface - Simple and clean English UI"""
    with gr.Blocks(title="Receipt Agent") as demo:
        gr.Markdown("# 🧾 Receipt Analysis Agent")
        gr.Markdown("Upload receipt images and ask questions about your expenses.")
        
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### 📸 Upload Receipts")
                image_input = gr.File(
                    file_count="multiple",
                    file_types=["image"],
                    label="Select receipt images",
                    height=100
                )
                
                gr.Markdown("### 💬 Ask a Question")
                query_input = gr.Textbox(
                    label="Your question",
                    placeholder="e.g., What is the total spending?",
                    lines=2
                )
                
                with gr.Row():
                    submit_btn = gr.Button("Submit", variant="primary", size="md")
                    clear_btn = gr.Button("Clear", variant="stop", size="md")
            
            with gr.Column(scale=2):
                chatbot = gr.Chatbot(
                    label="Conversation",
                    height=450,
                    show_label=True
                )
        
        # Example queries
        gr.Markdown("### 💡 Example Questions")
        example_queries = [
            "What is the total spending across all receipts?",
            "How much would I have paid without discounts?",
            "What is the total discount amount?",
            "Which receipt has the highest spending?"
        ]
        gr.Examples(
            examples=example_queries,
            inputs=query_input
        )
        
        # Event bindings
        submit_btn.click(
            fn=process_receipts_and_query,
            inputs=[image_input, query_input, chatbot],
            outputs=[chatbot, query_input]
        )
        
        query_input.submit(
            fn=process_receipts_and_query,
            inputs=[image_input, query_input, chatbot],
            outputs=[chatbot, query_input]
        )
        
        clear_btn.click(
            fn=clear_conversation,
            outputs=[chatbot]
        )
    
    return demo


if __name__ == "__main__":
    demo = create_gradio_interface()
    demo.launch(share=True, server_name="0.0.0.0")  # Auto-select available port
