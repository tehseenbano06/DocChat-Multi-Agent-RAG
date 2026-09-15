import hashlib
import gradio as gr

from document_processor import DocumentProcessor
from retriever import RetrieverBuilder
from workflow import AgentWorkflow

processor = DocumentProcessor()
builder = RetrieverBuilder()
workflow = AgentWorkflow()

def file_hashes(files):
    return frozenset(
        hashlib.sha256(open(f.name, "rb").read()).hexdigest()
        for f in files
    )

def ask(files, question, state):
    if not files:
        return "Upload a document first.", "", state
    if not question.strip():
        return "Enter a question.", "", state

    try:
        hashes = file_hashes(files)

        if state.get("retriever") is None or hashes != state.get("hashes"):
            documents = processor.process(files)
            retriever = builder.build(documents)
            state = {"hashes": hashes, "retriever": retriever}

        result = workflow.run(question.strip(), state["retriever"])
        return result["answer"], result["verification"], state

    except Exception as e:
        return f"Error: {e}", "", state

def reset():
    return {"hashes": frozenset(), "retriever": None}

with gr.Blocks(title="DocChat - Multi-Agent RAG") as demo:
    gr.Markdown("""
# DocChat — Multi-Agent RAG

Upload documents and ask questions grounded in their content.

**Scope Check → Hybrid Retrieval → Research → Verification → Self-Correction**
""")

    state = gr.State({"hashes": frozenset(), "retriever": None})

    files = gr.File(
        label="Documents",
        file_count="multiple",
        file_types=[".pdf", ".docx", ".txt", ".md"],
    )
    question = gr.Textbox(
        label="Question",
        placeholder="Ask a question about your documents...",
        lines=3,
    )
    submit = gr.Button("Submit")

    with gr.Row():
        answer = gr.Markdown(label="Answer")
        verification = gr.Markdown(label="Verification")

    submit.click(
        ask,
        inputs=[files, question, state],
        outputs=[answer, verification, state],
    )

    clear = gr.Button("Clear Session")
    clear.click(reset, outputs=state)

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=5000)
