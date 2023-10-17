import os
import logging

import pandas as pd
import yaml as yml
from transformers import pipeline


__all__ = ["Model"]


class Model:
    name = "camembert_sfp"
    config_path = os.path.join("config", f"{name}.yml")
    models_cache = os.path.join("cache", "models")

    def __init__(self):
        self.logger = logging.getLogger("Model")

        with open(self.config_path, "r") as f:
            config = yml.safe_load(f)

        task = config["task"]
        model = config["model"]
        tokenizer = model[::]

        try:
            # load the model from cache/models
            self.pipe = pipeline(task, os.path.join(self.models_cache, self.name))
            self.logger.info("Model loaded from cache")
        except OSError:
            # download the model
            self.pipe = pipeline(task, model=model, tokenizer=tokenizer)
            self.pipe.save_pretrained(os.path.join(self.models_cache, self.name))
            self.logger.info("Model downloaded from latest endpoint")

        filename = os.path.join("assets", "sample.csv")
        if os.path.exists(f := os.path.join("assets", "data.csv")):
            filename = f

        # nom_batterie,pui_batterie_mAh,tension_V,poids_g,prix_euro
        raw_context = pd.read_csv(filename)
        self.context = "".join(
            (
                f"nom batterie: {row['nom_batterie']}, "
                "puissance {row['pui_batterie_mAh']} mAh, "
                "tension {row['tension_V']} V, "
                "poids {row['poids_g']} g, "
                "prix {row['prix_euro']} euro ;\n"
                for _, row in raw_context.iterrows()
            )
        )

    def get_build_response(self, message: str) -> str:
        """Get the response from the model"""
        return self.pipe(question=message, context=self.context)["answer"]
