# hello_pipeline.py

from redun import task

@task()
def add(a: int, b: int) -> int:
    return a + b

@task()
def main() -> int:
    return add(2, 3)
