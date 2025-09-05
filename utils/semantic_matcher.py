from sentence_transformers import SentenceTransformer, util
from typing import List, Dict

MODEL = SentenceTransformer("all-MiniLM-L6-v2")

def semantic_similarity(resume_text: str, jobs: List[Dict], top_k: int = 5) -> List[Dict]:
    """Rank jobs by semantic similarity to resume text."""
    # Ensure resume_text is a string
    if not resume_text or not isinstance(resume_text, str):
        resume_text = str(resume_text) if resume_text else ""

    emb_resume = MODEL.encode([resume_text], convert_to_tensor=True)  # wrap in list!

    # Collect only valid job descriptions
    job_texts, valid_jobs = [], []
    for job in jobs:
        desc = job.get("job_description") or job.get("description")
        if isinstance(desc, str) and desc.strip():
            job_texts.append(desc)
            valid_jobs.append(job)

    if not job_texts:
        return []

    emb_jobs = MODEL.encode(job_texts, convert_to_tensor=True)

    scores = util.pytorch_cos_sim(emb_resume, emb_jobs)[0]
    ranked_idx = scores.argsort(descending=True)

    top_matches = []
    for idx in ranked_idx[:top_k]:
        job = valid_jobs[int(idx)]
        job["similarity"] = float(scores[idx])
        top_matches.append(job)

    return top_matches
