from __future__ import annotations
import os
from prefect import flow, task
from src.train import train
from src.evaluate import evaluate




@task
def task_train(output_dir: str = "models") -> str:
return train(output_dir)




@task
def task_evaluate(model_path: str) -> str:
report = evaluate(model_path)
print(report)
return report




@flow(name="cancer_detection_pipeline")
def main_flow():
model_path = task_train()
_ = task_evaluate(model_path)




if __name__ == "__main__":
main_flow()