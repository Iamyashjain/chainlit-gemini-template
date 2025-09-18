import chainlit as cl
from model import stream_gemini_response

@cl.on_chat_start

async def on_chat_start():
    text = """
👋 Hello! I’m your Nagar Mitra, here to help you register civic complaints with ease.  

Whether it’s a pothole, a broken streetlight, or garbage that needs clearing just tell me, and I’ll make sure your concern gets logged.  
Ready? Let’s get started! 🚀
"""

    await cl.Message(content=text).send()
    cl.user_session.set(
        "message_history",
        [{"role": "system", "content": "You are a helpful assistant."}],
    )

@cl.on_message
async def main(message: cl.Message):
    message_history = cl.user_session.get("message_history")
    
    message_content = message.content

    message_history.append({"role": "user", "content": message_content})
    
    msg = cl.Message(content="", author="Tommy")
    response = ""
    async for chunk in stream_gemini_response(message_content):
        await msg.stream_token(chunk)
        response += chunk
    await msg.send()

    message_history.append({"role": "assistant", "content": msg.content})
    await msg.update()
    