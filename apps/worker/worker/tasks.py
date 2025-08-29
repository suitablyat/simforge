import time

def hello(name: str) -> str:
    time.sleep(1)
    return f"Hello {name} from worker!"
