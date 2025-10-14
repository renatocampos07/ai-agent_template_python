import os
from langchain.prompts import PromptTemplate

DEFAULT_SYSTEM_PROMPT = os.getenv(
    "SYSTEM_PROMPT",
    "Você é um agente que responde com base nos documentos fornecidos. " \
    "Resuma e explique de forma clara e avise quando não encontrar informação relevante."
)

QA_PROMPT_TEMPLATE = """
{system_prompt}

Contexto:
{context}

Pergunta:
{question}

Resposta estruturada:
- Insight principal:
- Referências internas relevantes:
- Próximos passos recomendados:
""".strip()


def get_qa_prompt(system_prompt: str = DEFAULT_SYSTEM_PROMPT) -> PromptTemplate:
    return PromptTemplate(
        input_variables=["context", "question"],
        template=QA_PROMPT_TEMPLATE,
        partial_variables={"system_prompt": system_prompt},
    )
