from .JobType import JobType
from typing import override
from crypto import random_prime_fast # type: ignore
import multiprocessing as mp

def call_random_prime_fast(type: str, numBits: int, queue) -> None: # type: ignore
    result = random_prime_fast(f"{numBits}b", f"{numBits+2}b", 1)[0]
    queue.put({ "type": type, "result": result }) # type: ignore

class RSAGenerateStep1JobType(JobType):
    @override
    def __init__(self):
        super().__init__(job_type="RSAGenerateStep1", immediate=True)
    
    @override
    def __call__(self, input: str) -> str:
        numBitsP, numBitsQ = map(int, input.split(','))
        if abs(numBitsP - numBitsQ) <= 2:
            numBitsP = numBitsQ = max(numBitsP, numBitsQ)
            p, q = random_prime_fast(f"{numBitsP}b", f"{numBitsP+2}b", 2)
        else:
            queue: mp.Queue[dict[str, str|int]] = mp.Queue()
            processes: list[mp.Process] = []
            args_list = [("p", numBitsP, queue), ("q", numBitsQ, queue)]
            for args in args_list:
                process = mp.Process(target=call_random_prime_fast, args=args) # type: ignore
                process.start()
                processes.append(process)
            
            for process in processes:
                process.join()
            
            pack1, pack2 = [queue.get() for _ in args_list]
            if pack1["type"] == "p":
                p = pack1["result"]
                q = pack2["result"]
            else:
                p = pack2["result"]
                q = pack1["result"]

        return f"{p},{q}"
