from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain.callbacks.base import BaseCallbackHandler
import queue
import threading

# Get the API key from the environment variable
openai_api_key = ""

if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set")


llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    temperature=0.7,
    max_tokens=500,
    api_key=openai_api_key,
    streaming=True
)


memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)


embeddings = OpenAIEmbeddings(api_key=openai_api_key)  # Also pass the API key here

vector_db = Chroma(embedding_function=embeddings, collection_name="my_collection", persist_directory="./my_chroma_db")

retriever = ContextualCompressionRetriever(
    base_compressor=LLMChainExtractor.from_llm(llm),
    base_retriever=vector_db.as_retriever()
)

prompt_template = ChatPromptTemplate.from_template("""
    Context: {context}
    Chat History: {chat_history}
    Human: {question}
    AI: Please provide a relevant and direct answer based on the context and chat history.
""")

conversation_chain = ConversationalRetrievalChain.from_llm(
    llm,
    memory=memory,
    retriever=retriever,
    combine_docs_chain_kwargs={"prompt": prompt_template},
)

class TokenStreamHandler(BaseCallbackHandler):
    def __init__(self, stream_to_terminal=False):
        self.queue = queue.Queue()

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.queue.put(token)


    def get_tokens(self):
        while True:
            token = self.queue.get()
            if token is None:
                break
            yield token


def chatbot_response(user_input, stream_to_terminal=False):
    handler = TokenStreamHandler(stream_to_terminal=stream_to_terminal)
    
    thread = threading.Thread(target=conversation_chain, args=({"question": user_input},), kwargs={"callbacks": [handler]})
    thread.start()

    for token in handler.get_tokens():
        yield token

    thread.join()
    handler.queue.put(None)
