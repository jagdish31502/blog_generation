import os
from llama_index.core import PromptTemplate
from llama_index.llms.gemini import Gemini
from llama_index.core import VectorStoreIndex, Document, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import chromadb
from llama_index.core import Settings
from dotenv import load_dotenv

load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv('GOOGLE_API_KEY')

# Load Model Function
def model_selection():
    try:
        Settings.llm = Gemini(model="models/gemini-pro")
        Settings.embed_model = HuggingFaceEmbedding(model_name=os.getenv('EMBED_MODEL'))
        return Settings.llm, Settings.embed_model
    except Exception as e:
        print(f"Error in model_selection: {e}")
        return None, None

# Function to get response from LLama2 model
def getLLamaresponse(input_text, no_words, llm):
    try:
        template = """
        You are an expert blog writer. Your task is to generate a well-structured, engaging, and informative blog post on the given topic. 
        The blog should be clear, concise, and within the specified word limit. Ensure that the content is relevant, accurate, and easy to read.

        Instructions:
        Topic: {input_text}
        Word Count: {no_words} Words

        Structure:

        Title: Create a catchy and relevant title.
        Paragraphs: Write the entire blog in a single, well-structured paragraph.
        Style and Tone: Write in a friendly and informative tone. Use active voice and short sentences. Ensure the content is free from grammatical and spelling errors.        
        Formatting: Write in a paragraph format.
        Additional Notes: Stick to the topic and avoid irrelevant information. Ensure the blog post is exactly {no_words} words.

        Example:
        Topic: The Benefits of Meditation
        Word Count: 100 Words
        
        Title: The Transformative Power of Meditation

        Meditation offers numerous benefits for both the mind and body. It helps reduce stress by lowering cortisol levels, 
        promoting a sense of calm and relaxation. Regular practice can improve concentration, making it easier to focus on tasks. 
        Additionally, meditation enhances emotional health by reducing symptoms of anxiety and depression, fostering a positive outlook on life. 
        It also increases self-awareness, encouraging personal growth and a deeper understanding of oneself. Incorporating meditation into your daily 
        routine, even for just a few minutes, can lead to significant improvements in overall well-being and inner peace.
        """
        qa_template = PromptTemplate(template)
        prompt = qa_template.format(input_text=input_text, no_words=no_words)
        response = llm.complete(prompt)
        return response
    except Exception as e:
        print(f"Error in getLLamaresponse: {e}")
        return None

# Load storage context from disk
def save_load_from_disk(response, embed_model):
    try:
        db = chromadb.PersistentClient(path="./chroma_db")
        chroma_collection = db.get_or_create_collection("bloggeneration")
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        document = Document(text=str(response))
        index = VectorStoreIndex.from_documents(documents=[document], storage_context=storage_context, embed_model=embed_model)
        index.storage_context.persist()
        return index
    except Exception as e:
        print(f"Error in save_load_from_disk: {e}")
        return None