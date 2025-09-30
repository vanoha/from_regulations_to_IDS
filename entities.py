from typing import Optional
from dataclasses import dataclass
from pydantic import BaseModel, Field
from enum import Enum


@dataclass
class Section:
    text: str = ''
    headings: tuple[str, ...] = ()

    def __bool__(self) -> bool:
        return bool(self.text) or bool(self.headings)


@dataclass
class SectionRequirements:
    section: Section
    reqs: list[str]
    paragraph: str


@dataclass
class Source:
    paragraph: str
    document: str
    chapter: str


@dataclass
class BaseRequirement:
    req_text: str
    source: Source


class Entity(str, Enum):
    SUBJECT = "subject_entity"
    OBJECT = "object_entity"


class Operator(str, Enum):
    EQUAL = "=="
    NOT_EQUAL = "!="
    GREATER_THAN = ">"
    GREATER_EQUAL = ">="
    LESS_THAN = "<"
    LESS_EQUAL = "<="
    BELONGS_TO = "∈"


class Applicability(BaseModel):
    entity: Entity = Field(description="Сущность, на которую накладывается условие применимости требования. "
                                       "Если subject_entity == object_entity, то entity = \"object_entity\".")
    property: str = Field(description="Свойство сущности, на которое накладывается условие применимости требования.")
    operator: Operator = Field(description="Тип условия, накладываемого на property.")
    value: str = Field(description="Значение условия, накладываемого на property.")


class StatementType(str, Enum):
    REQUIREMENT = "requirement"
    ASSUMPTION = "assumption"


class Statement(BaseModel):
    property: str = Field(description="Свойство object_entity, на которое накладывается ограничение.")
    operator: Operator = Field(description="Тип ограничения, накладываемого на property.")
    value: str = Field(description="Значение ограничения, накладываемого на property.")
    type: StatementType = Field(description="Тип требования, определяющий его силу.")


class ExternalReference(BaseModel):
    document: str = Field(description="Название документа или пункт списка литературы.")
    domain: Optional[str] = Field(default=None, description="Область требования.")


class GraphRequirement(BaseModel):
    req_text: str
    object_entity: str
    subject_entity: str
    relation: str
    applicability: list[Applicability]
    statement: Statement
    external_refs: list[ExternalReference]
    source: Source

    def model_post_init(self, __context) -> None:
        for ref in self.external_refs:
            if ref.domain is None:
                ref.domain = ""


class QueryType(str, Enum):
    DUPLICATE = "Дубликат"
    CONTRADICTION = "Противоречие"
    QUESTION = "Вопрос"
    OTHER = "Остальное"


class Query(BaseModel):
    type: QueryType = Field(description="Тип запроса")
    mean: str = Field(description="Суть запрошаемого требования")


class StructuredQuery(Query):
    statement: Optional[dict]
