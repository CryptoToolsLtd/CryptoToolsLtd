class JobType:
    def __init__(self, job_type: str, immediate: bool):
        """
        immediate: whether the job is executed immediately or queued
        """
        self.job_type = job_type
        self.immediate = immediate
    
    def __call__(self, input: str) -> str:
        raise NotImplementedError
