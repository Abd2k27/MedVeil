"""Télécharge PARHAF et sa version annotée pour la pseudonymisation dans data/."""
from huggingface_hub import snapshot_download

for repo in ["HealthDataHub/PARHAF", "HealthDataHub/PARHAF-pseudo-annotated"]:
    chemin = snapshot_download(
        repo_id=repo,
        repo_type="dataset",
        local_dir=f"data/{repo.split('/')[1]}",
        allow_patterns=["data/*", "data/**/*", "README.md", "guidelines/*", "doc/*"],
    )
    print("OK", repo, "->", chemin)
