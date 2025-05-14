from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

class ToolCallingChatbot:
    def __init__(self):
        self.model = "meta-llama/Llama-3.3-70B-Instruct-Turbo"
        self.client = OpenAI(
            api_key=os.getenv("TOGETHER_API_KEY"),
            base_url="https://api.together.xyz/v1"
        )
        self.tools = [{
            "type": "function",
            "function": {
                "name": "search_legal_knowledge_base",
                "description": "Searches the knowledge base to retrieve relevant legal information.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The user question or search query."
                        }
                    },
                    "required": [
                        "query"
                    ],
                    "additionalProperties": False
                },
                "strict": True
            }
        }]
        
        system_msg = """Role: You are a friendly Azerbaijani-speaking legal assistant that answers questions related to the Azerbaijani Labor Code (Əmək Məcəlləsi). Always respond in Azerbaijani.

Capabilities:
-   You may engage in general conversational exchanges such as greetings, farewells, and polite small talk (e.g., “Salam”, “Necəsiz?”, “Sağ olun”).
-   When a user greets you, respond with: "Salam! Mən Əmək Məcəlləsi üzrə ixtisaslaşmış çatbotam. Əmək Məcəlləsi ilə bağlı hər hansı sualınız var?"
-   You must use the search_legal_knowledge_base tool to retrieve information when answering questions related to the Labor Code.
-   When responding to legal questions, always refer to the metadata in the retrieved context (e.g., chapter names, article numbers, etc.).

Restrictions:
-   Do not answer substantive legal questions that are unrelated to the Labor Code. Instead, reply with: "Bağışlayın, yalnız Əmək Məcəlləsi ilə bağlı sualları cavablandıra bilərəm."
-   Do not use the search_legal_knowledge_base tool for general or non-legal conversations.
-   Do not provide legal advice outside the scope of the Labor Code.

Tone: Always be polite, friendly, and helpful — while staying strictly within the boundaries of the Labor Code for legal responses."""
            
        self.messages = [{"role": "system", "content": system_msg}]
        
    def append_message(self, role, content, tool_call_id=None):
        if role=="tool":
            self.messages.append({
            "role": role,
            "tool_call_id": tool_call_id,
            "content": content
        })
        else:
            self.messages.append({"role": role, "content": content})

    def ask(self, query, function=None):
        self.append_message(role="user", content=query)
        
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            tools=self.tools,
            tool_choice="auto"
        )
        
        if completion.choices[0].message.tool_calls: # if we have tool calling
            tool_call = completion.choices[0].message.tool_calls[0]
            
            args = json.loads(tool_call.function.arguments)

            result = function(query)

            self.messages.append(completion.choices[0].message)
            self.append_message(role="tool", content=str(result), tool_call_id=tool_call.id)

            completion = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                tools=self.tools,
                tool_choice="auto"
            )
                        
        assistant_message = completion.choices[0].message.content
        self.append_message(role="assistant", content=assistant_message)
        
        return {"message": assistant_message}


if __name__=="__main__":
    chatbot = ToolCallingChatbot()
    
    def rag(a):
        return "No info"

    print(chatbot.ask("men bilmek isteyirdim ki, maximum nece iste isleye bilerem?", function=rag))