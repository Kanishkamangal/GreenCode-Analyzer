from pydantic import BaseModel, ConfigDict
from typing import Optional


class ProgrammingLanguageCreate(BaseModel):
    lang_name: str
    compiler: str
    version: str
    compile_command: Optional[str] = None
    run_command: str


class ProgrammingLanguageResponse(BaseModel):
    lang_id: int
    lang_name: str
    compiler: str
    version: str
    compile_command: Optional[str]
    run_command: str

    model_config = ConfigDict(from_attributes=True)