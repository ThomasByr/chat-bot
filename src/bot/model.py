import os
import logging

import torch
from random import choice

import pandas as pd
import yaml as yml
from transformers import pipeline

from ..helper.capture import enable_proxy, disable_proxy


__all__ = ["Model"]


class Model:
    name = "camembert_sfp"  # classifier
    path = os.path.join("config", f"{name}.yml")
    cache = os.path.join("cache", "models")

    def __init__(self):
        self.logger = logging.getLogger("model")

        with open(self.path, "r") as f:
            self.config: list[str] = yml.safe_load(f)

        task = self.config["task"]
        model = self.config["model"]
        tokenizer = model[::]

        device = 0 if torch.cuda.is_available() else -1  # try using gpu
        try:
            # load the model from cache/models
            enable_proxy()
            self.pipe = pipeline(
                task, os.path.join(self.cache, self.name), device=device
            )
            disable_proxy()
            self.logger.info("Model loaded from cache")
        except:  # noqa
            # download the model
            enable_proxy()
            self.pipe = pipeline(task, model=model, tokenizer=tokenizer, device=device)
            self.pipe.save_pretrained(os.path.join(self.cache, self.name))
            disable_proxy()
            self.logger.info("Model downloaded from latest endpoint")

        filename = os.path.join("assets", "sample.csv")
        if os.path.exists(f := os.path.join("assets", "data.csv")):
            filename = f

        # nom_batterie,pui_batterie_mAh,tension_V,poids_g,prix_euro
        raw_context = pd.read_csv(filename)
        self.context = "".join(
            (
                f"nom batterie: {row['nom_batterie']}, "
                f"puissance {row['pui_batterie_mAh']} mAh, "
                f"tension {row['tension_V']} V, "
                f"poids {row['poids_g']} grammes, "
                f"prix {row['prix_euro']} euros ;\n"
                for _, row in raw_context.iterrows()
            )
        )
        with open(os.path.join("assets", "sentences.txt"), "r") as f:
            self.context += f.read()

        self.logger.info("Context loaded")

    def get_build_response(self, message: str) -> str:
        """Get the response from the model"""
        response = self.pipe(question=message, context=self.context)
        if response["score"] < self.config["threshold"]:
            # pipeline self.gp_context +
            return choice(["Je ne comprends pas", "Je ne sais pas"])
        return f"{response['answer'].strip()} ({response['score']})"

    def build_welcome_msg(self, username: str) -> str:
        welcome_msg: str = self.config["welcome_msg"]
        # welcome_msg placeholder for the username : {username}
        return welcome_msg.replace("{username}", username)
