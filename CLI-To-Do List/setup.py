from setuptools import setup

setup(
    name="todo-cli",
    version="1.0",
    py_modules=["todo"],
    entry_points={
        "console_scripts": [
            "todo=todo:main",
        ],
    },
)
