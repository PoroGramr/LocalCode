from setuptools import setup, find_packages

setup(
    name="ollama-agent",
    version="0.1.0",
    packages=find_packages(),
    py_modules=["agent", "cli", "ollama_client", "schemas", "state", "tools"],
    install_requires=[
        "requests",
        "pydantic",
    ],
    entry_points={
        "console_scripts": [
            "oa=cli:main", # 다시 'oa'로 설정
        ],
    },
)
