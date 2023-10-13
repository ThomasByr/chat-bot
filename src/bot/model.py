from transformers import pipeline


__all__ = ["get_build_response"]


task = "question-answering"
model = "etalab-ia/camembert-base-squadFR-fquad-piaf"
tokenizer = model[::]
pipe = pipeline(task, model=model, tokenizer=tokenizer)

context = """
nom batterie: AF700, puissance: 700, tension: 12, type: plomb, capacite: 70, poids: 23, prix: 100 ;
nom batterie: AF800, puissance: 800, tension: 12, type: plomb, capacite: 80, poids: 25, prix: 120 ;
nom batterie: CGF4A, puissance: 1000, tension: 24, type: gel, capacite: 100, poids: 30, prix: 150 ;
nom batterie: CGF5A, puissance: 1200, tension: 24, type: gel, capacite: 120, poids: 35, prix: 180 ;
"""


def get_build_response(message: str) -> str:
    return pipe(question=message, context=context)["answer"]
