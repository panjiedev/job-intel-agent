import os
import yaml
from langchain_core.prompts import PromptTemplate

class PromptManager:
    """Prompt-as-Code 管理器，从 YAML 文件加载提示词模板"""
    def __init__(self, prompt_dir: str = "prompts"):
        self.prompt_dir = prompt_dir

    def load_template(self, prompt_name: str) -> PromptTemplate:
        file_path = os.path.join(self.prompt_dir, f"{prompt_name}.yaml")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Prompt template {prompt_name} not found in {self.prompt_dir}")
            
        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            
        return PromptTemplate.from_template(data["template"])

# 单例对象供全局调用
prompt_manager = PromptManager()
