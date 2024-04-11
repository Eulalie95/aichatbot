import streamlit as st
from langchain_community.llms import llamacpp
from langchain.prompts import PromptTemplate
from langchain.callbacks.base import BaseCallbackManager
from huggingface_hub import hf_hub_download



def stream_handler(container,initial_text):
    text = initial_text

    def on_llm_token(token: str, **kwargs)-> None:
        nonlocal text
        text +=token 
        container.markdown(text)
        return on_llm_token
    
    @st.cache_resource
    def creat_chain(system_prompt):
        (repo_id,model_file_name)=("TheBloke/Mistra-7B-Instruction-v0.1-GGUF",
                                "mistral-7b-instruct-v0.1.04_0.gguf")
        model_path = hf_hub_download(repo_id=repo_id,filename=model_file_name,repo_type="model")
        llm = llamacpp(model_path=model_path,
                       temperature=a,
                       max_tokens=512,
                       top_p=1,
                       stop=["[INST]"],
                       verbose=False,
                       streaming=True
                       )
        
        template = f"""
        "<s>[INST]{system_prompt}[/INST]</s>
        [INST]{"{question}"}


        """
        prompt = PromptTemplate(template=template,input_variables=["question"])
        llm_chain = prompt | llm
        return llm_chain
    st.set_page_config(
        page_title="Omonlaye WIADA aichat! "
        )
    st.header(" Omonlaye WIADA aichat!")

    sytem_prompt= st.text_area(
        label="System Prompt",
        value="You are a helpful AI assistant who answers questions in short sentences.",
        key="system_prompt"
        )
    llm_chain = creat_chain(sytem_prompt)
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"rale":"assistant","content":"Hey,Am Omonlaye WIADA aichat,how may i help you today ?"}
        ]
    if "current_response" not in st.session_state:
        st.session_state.current_response=""
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
        
    if user_prompt :=st.chat_input("Your message") : # message qui s'affiche eu niveau de la barre d'entrée des questions de l'utilisateur:
        st.session_state.message.append(
            {"role":"user","content":user_prompt}
        )
        with st.chat_message("user"):
            st.markdownr(user_prompt)
        response=llm_chain.invoke({"question":user_prompt})
    
        st.session_state.messages.append(
            {"role":"assistant","content":response}
        )
    
        with st.chat_message("assistant"):
            st.markdown(response)
        
        
    
