import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key from .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Model
model = genai.GenerativeModel("gemini-1.5-flash")

# Inventory list
inventory = []

# === Tools ===

def addItem(product_id: int, name: str, qty: int, action: str):
    if not product_id:
        return "⚠️ Product id missing."
    
    item = {
        "product_id": product_id,
        "name": name,
        "qty": qty,
        "action": action
    }
    inventory.append(item)
    return f"✅ Added: {item['name']} (id: {item['product_id']}, qty: {item['qty']}, action: {item['action']})"

def deleteItem(product_id: int):
    for i, item in enumerate(inventory):
        if item["product_id"] == product_id:
            inventory.pop(i)
            return f"🗑️ Removed item with id {product_id}."
    return f"❌ No item found with id {product_id}."

def updateItem(product_id: int, name: str, qty: int, action: str):
    for i, item in enumerate(inventory):
        if item["product_id"] == product_id:
            inventory[i] = {
                "product_id": product_id,
                "name": name,
                "qty": qty,
                "action": action
            }
            return f"🔄 Updated item {product_id} → {name}, qty: {qty}, action: {action}"
    return f"❌ No item found with id {product_id}."

# === Chat Loop ===
print("🤖 Inventory Agent Ready (type 'exit' to quit)")

while True:
    ask = input("You: ")
    if ask.lower() == "exit":
        break
    
    # Simple "AI-style" reply from Gemini
    prompt = f"""
    User said: {ask}
    
    You are the inventory guy. You can use these tools to manage the inventory, According to structure defined below, you can:

    - addItem(product_id, name, qty, action)
    - deleteItem(product_id)
    - updateItem(product_id, name, qty, action)

    You can only use the tools defined above. If you need to add an item, use addItem. 
    If you need to delete an item, use deleteItem. 
    If you need to update an item, use updateItem. 
    If you don't know what to do, just say "I don't know" or "I can't help with that".
    """

    response = model.generate_content(prompt)
    print("Bot:", response.text)
