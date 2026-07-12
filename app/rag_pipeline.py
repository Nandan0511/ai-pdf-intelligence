import uuid
import traceback
from openai import OpenAI
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from core.config import (
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    EMBEDDING_MODEL,
    OPENROUTER_API_KEY,
    OPENROUTER_BASE_URL,
    LLM_MODEL,
)


client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url=OPENROUTER_BASE_URL,
)


# =====================================
# Embedding Model
# =====================================

_embedding_model = None


def get_embedding_model():
    global _embedding_model

    if _embedding_model is None:
        _embedding_model = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL
        )

    return _embedding_model


# =====================================
# PDF Loader
# =====================================

def load_pdf(pdf_path):

    loader = PyPDFLoader(pdf_path)

    return loader.load()


# =====================================
# Split Documents
# =====================================
def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    chunks = splitter.split_documents(
        documents
    )

    # Add page number metadata
    for chunk in chunks:

        chunk.metadata["page"] = (
            chunk.metadata.get("page", 0) + 1
        )

    return chunks

# =====================================
# Create Vector Store
# =====================================

def create_vectorstore(chunks):

    collection_name = (
        f"pdf_{uuid.uuid4()}"
    )

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=get_embedding_model(),
        collection_name=collection_name,
    )

    return vectorstore


# =====================================
# Retrieve Documents
# =====================================

def retrieve_documents(
    query,
    vectorstore,
):

    retriever = vectorstore.as_retriever(
        search_kwargs={
            "k": 3
        }
    )

    return retriever.invoke(query)


# =====================================
# Rewrite Query
# =====================================

def rewrite_query(
    query,
    chat_history,
):

    query_lower = query.lower()

    if "conclusion" in query_lower:
        return (
        "conclusion final remarks "
        "project outcome findings "
        "learning outcomes future scope"
      )

    if ("summary" in query_lower
     or "summarize" in query_lower
     or "overview" in query_lower
     or "executive summary" in query_lower
     or "brief summary" in query_lower):
      return (
        "summary overview document summary"
       )

    if "risk" in query_lower:
     return (
        "risk risks challenges issues "
        "limitations drawbacks problems"
    )

    if "limitation" in query_lower:
     return (
        "limitations drawbacks constraints"
    )

    if "advantage" in query_lower:
     return (
        "advantages benefits strengths"
    )

    if "chapter" in query_lower:
     return (
        query + " section heading"
    )

    if not chat_history:
        return query

    if len(query.split()) > 8:
        return query

    history_text = "\n".join(
        [
            f"{msg['role']}: {msg['content']}"
            for msg in chat_history[-4:]
        ]
    )

    prompt = f"""
Rewrite the latest user message
as a standalone search query.

Conversation:
{history_text}

Question:
{query}

Standalone Query:
"""

    try:

        response = (
            client.chat.completions.create(
                model=LLM_MODEL,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            )
        )

        return (
            response.choices[0]
            .message.content
            .strip()
        )

    except Exception:

        return query


# =====================================
# Prompt Builder
# =====================================

def build_prompt(
    query,
    context,
    chat_history,
):

    history_text = "\n".join(
        [
            f"{msg['role']}: {msg['content']}"
            for msg in chat_history[-4:]
        ]
    )

    return f"""
You are an expert AI PDF Intelligence Assistant specialized in Retrieval-Augmented Generation (RAG).

Your job is to answer questions ONLY using the provided PDF Context.

=================================================
SOURCE OF TRUTH
=================================================

The PDF Context is the ONLY source of factual information.

Never:
• Use outside knowledge.
• Guess missing information.
• Hallucinate facts.
• Infer information not present in the PDF.
• Use information from previous PDFs.

Conversation History may ONLY be used to understand follow-up references such as:
• this
• that
• those
• explain further
• tell me more
• continue

Conversation History is NEVER a source of factual information.

=================================================
REASONING PROCESS
=================================================

Before answering:

1. Read the retrieved PDF Context.
2. Determine whether the answer exists.
3. If fully available:
   Answer using ONLY the PDF Context.
4. If partially available:
   Answer using only the available information and clearly state that no additional details are available in the document.
5. If no relevant information exists, reply EXACTLY:

This information is not available in the uploaded document.

Never provide both an answer and the fallback response.

=================================================
FORMATTING RULES
=================================================

Summary / Overview
• Use heading "Summary"
• Present concise bullet points.
• Include:
  - Purpose
  - Main topics
  - Important findings
  - Technologies (if applicable)
  - Conclusion (if available)

Insights / Risks / Benefits / Features
• Use a heading.
• Present bullet points.

Definitions / Explanations
• Use a concise paragraph.

Comparisons
• Use a markdown table whenever appropriate.

Processes / Workflows
• Use numbered steps.

Lists
• Use bullet points.

Structured Data
• Present marks, scores, tables, expenses, statistics, schedules, etc. using markdown tables whenever appropriate.

Resume / CV / Portfolio
Summarize professionally using sections such as:
• Education
• Skills
• Experience
• Projects
• Achievements

Do NOT reveal personal contact information unless explicitly requested.

=================================================
EXTRACTION RULES
=================================================

When asked to extract:

• Name
• Date
• Number
• Email
• Phone Number
• CGPA
• Percentage
• Address
• Skills
• Certifications
• Project Title
• Technologies
• Organization
• Any specific field

Extract the value exactly as written in the PDF.

Do not invent, modify or rephrase extracted values unless necessary.

=================================================
PAGE REFERENCE
=================================================

Whenever possible, mention the page number(s) where the information was found.

Examples:

According to Page 5...

The document mentions on Pages 2 and 3...

If multiple retrieved pages contain relevant information, combine them naturally without repeating the same information.

=================================================
RESPONSE STYLE
=================================================

Responses should be:

• Accurate
• Professional
• Well-structured
• Concise
• Easy to read

Prefer:

• Markdown headings
• Bullet lists
• Tables
• Numbered steps

Avoid unnecessary repetition and long unstructured paragraphs.

=================================================
CONVERSATION HISTORY
=================================================

{history_text}

=================================================
PDF CONTEXT
=================================================

{context}

=================================================
QUESTION
=================================================

{query}

=================================================
ANSWER
=================================================
"""

    
    # return f"""
# You are an intelligent PDF Question Answering Assistant.

# Your job is to answer questions using ONLY the information available in the provided PDF Context.

# =================================================
# CORE RULES
# =================================================

# 1. Use ONLY information from PDF Context.

# 2. Never use your own knowledge.

# 3. Never use information from previous PDFs.

# 4. Never invent facts.

# 5. Never guess missing information.

# 6. Never infer facts that are not explicitly supported by the PDF Context.

# 7. If only partial information is available, answer using only the available information.

# 8. If the PDF Context contains insufficient information, do NOT complete the answer using assumptions.

# 9. Conversation History may ONLY be used to understand references such as:
#    - this
#    - that
#    - tell me more
#    - explain further
#    - what about that

# 10. Conversation History is NOT a source of factual information.

# 11. PDF Context is the ONLY source of truth.

# 12. If the PDF Context contains partial information relevant to the question:

# - Answer using only the available information.
# - Clearly state that no additional information is available in the document.

# If the PDF Context contains no relevant information:

# Reply exactly:

# This information is not available in the uploaded document.

# =================================================
# FORMATTING RULES
# =================================================

# 1. SUMMARY REQUESTS

# If the user asks:
# - Summarize
# - Give an overview
# - Executive summary
# - Brief summary

# Format:

# Summary

# • Point 1

# • Point 2

# • Point 3

# =================================================

# 2. INSIGHTS / RISKS / BENEFITS / FEATURES

# If the user asks:
# - Key insights
# - Main points
# - Highlights
# - Findings
# - Benefits
# - Risks
# - Features
# - Advantages
# - Disadvantages

# Format:

# Heading

# • Point 1

# • Point 2

# • Point 3

# =================================================

# 3. PERSON QUESTIONS

# If the user asks:
# - Who is...
# - Tell me about...
# - Describe the person

# Format:

# Provide a concise professional paragraph.

# =================================================

# 4. DEFINITION / EXPLANATION QUESTIONS

# If the user asks:
# - What is...
# - Define...
# - Explain...
# - Describe...

# Format:

# Provide a concise explanation in paragraph form.

# =================================================

# 5. COMPARISON QUESTIONS

# If the user asks:
# - Compare
# - Difference between
# - X vs Y

# Format:

# Use a markdown table whenever appropriate.

# Example:

# | Feature | Option A | Option B |
# |----------|----------|----------|
# | Item 1 | Value | Value |
# | Item 2 | Value | Value |

# =================================================

# 6. LIST EXTRACTION QUESTIONS

# If the user asks:
# - List all
# - What are the skills
# - What technologies are used
# - What certifications are present
# - What tools are used

# Format:

# Use bullet points.

# =================================================

# 7. PROCESS / WORKFLOW QUESTIONS

# If the user asks:
# - How does it work
# - Workflow
# - Process
# - Steps involved
# - Procedure

# Format:

# 1. Step one

# 2. Step two

# 3. Step three

# =================================================

# 8. CONTACT INFORMATION QUESTIONS

# If the user asks:
# - Contact details
# - Email
# - Phone number
# - Address
# - LinkedIn

# Format:

# Use bullet points.

# =================================================

# 9. RESUME / PROFILE QUESTIONS

# For resumes, CVs, portfolios, and profiles:

# - Present information in a professional profile format.
# - Summarize education, skills, experience, projects, and achievements.
# - Do NOT expose email, phone number, address, or personal links unless explicitly requested.

# =================================================

# 10. STRUCTURED DATA QUESTIONS

# If the PDF contains structured information such as:

# - Marks
# - Scores
# - Expenses
# - Statistics
# - Tables

# Use markdown tables whenever appropriate.

# =================================================

# 11. FOLLOW-UP QUESTIONS

# For questions like:

# - Tell me more
# - Explain further
# - Expand on this
# - What about that

# Use Conversation History only to resolve references.

# Use PDF Context as the source of truth.

# =================================================

# 12. MISSING INFORMATION HANDLING

# A. If the PDF Context contains relevant information:

# - Answer using ONLY the available information.
# - Do NOT add the fallback message.

# B. If the PDF Context contains partial information:

# - Answer using ONLY the available information.
# - Clearly state that no additional details are available in the document.
# - Do NOT add the fallback message.

# Example:

# Question:
# What is Python?

# Answer:
# Python Programming is listed as one of the skills mentioned in the document.
# No further explanation or definition of Python is provided in the document.

# C. If the PDF Context contains NO relevant information:

# Reply EXACTLY:

# This information is not available in the uploaded document.

# 13. RESPONSE CONSISTENCY

# - Never provide both an answer and the fallback message in the same response.

# Choose exactly one:

# 1. Answer using PDF information.

# OR

# 2. Return:

# This information is not available in the uploaded document.

# 14. EXTRACTION QUESTIONS

# If the user asks for a specific value, field, number, date, name, email, phone number, CGPA, percentage, project title, or similar information:

# - Extract the information exactly as written in the PDF Context.
# - Do not rephrase unless necessary.
# - Do not add extra information that was not requested.

# 15. RELEVANCE RULE

# If a term is only mentioned but not explained in the PDF Context:

# - State that the term is mentioned in the document.
# - Do not provide a definition.
# - Clearly state that no further explanation is available in the document.
# =================================================

# Conversation History:
# {history_text}

# =================================================
# PDF Context:
# {context}
# =================================================

# Question:
# {query}

# Answer:
# """


# =====================================
# LLM Completion
# =====================================

# def stream_completion(prompt):

#     response = client.chat.completions.create(
#         model=LLM_MODEL,
#         messages=[
#             {
#                 "role": "user",
#                 "content": prompt,
#             }
#         ],
#         stream=True,
#     )

#     answer = ""

#     for chunk in response:

#         try:

#             content = chunk.choices[0].delta.content

#             if content:
#                 answer += content

#         except Exception:
#             pass

#     return answer

def stream_completion(prompt):

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        max_tokens=800,
        temperature=0.2,
        stream=False,
    )

    return response.choices[0].message.content
# =====================================
# Generate Answer
# =====================================

def generate_answer(
    query,
    retrieved_docs,
    chat_history,
):

    if not retrieved_docs:

        return (
            "This information is not available in the uploaded document.",
            []
        )

    context = "\n\n".join(
    f"[Page {doc.metadata.get('page', '?')}]\n"
    f"{doc.page_content}"
    for doc in retrieved_docs
)

    prompt = build_prompt(
        query=query,
        context=context,
        chat_history=chat_history,
    )

    try:

        answer = stream_completion(
            prompt
        )

        import re

        # Fix numbered lists
        answer = re.sub(
           r'(\d+\.)\s',
           r'\n\n\1 ',
           answer
        )



    except Exception as e:

        traceback.print_exc()
        st.error(f"Error: {e}")
        return "Sorry, something went wrong while generating the answer.", []

    return answer, retrieved_docs


# =====================================
# Complete Pipeline
# =====================================

import re

def ask_pdf(
    query,
    vectorstore,
    chat_history,
):

    page_match = re.search(
        r"page\s+(\d+)",
        query.lower()
    )

    if page_match:

        page_num = int(
            page_match.group(1)
        )

        all_docs = vectorstore.get()

        print(
            "Requested page:",
            page_num
        )

        print(
            "Pages found:",
            [
                m.get("page")
                for m in all_docs["metadatas"]
            ]
        )

        page_docs = []

        for i, metadata in enumerate(
            all_docs["metadatas"]
        ):

            if metadata.get("page") == page_num:

                from langchain_core.documents import Document

                page_docs.append(
                    Document(
                        page_content=
                        all_docs["documents"][i],
                        metadata=metadata,
                    )
                )

        print(
            "Page docs found:",
            len(page_docs)
        )

        if page_docs:

            return generate_answer(
                query,
                page_docs,
                chat_history,
            )

        return (
            "Page not found in the uploaded document.",
            []
        )

    search_query = rewrite_query(
        query,
        chat_history,
    )

    docs = retrieve_documents(
        search_query,
        vectorstore,
    )

    return generate_answer(
        query,
        docs,
        chat_history,
    )