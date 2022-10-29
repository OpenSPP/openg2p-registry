from datetime import date
from typing import List, Optional

from .individual import IndividualInfoOut
from .naive_orm_model import NaiveOrmModel
from .registrant import PhoneNumberIn, RegistrantIDIn, Relationship1In, Relationship2In


class GroupMembershipKindInfo(NaiveOrmModel):
    name: str


class GroupMembersInfoOut(NaiveOrmModel):
    id: int
    individual: IndividualInfoOut
    kind: Optional[
        List[GroupMembershipKindInfo]
    ] = None  # TODO: Would be nicer to have it as a list of str


class GroupMembersInfoIn(NaiveOrmModel):
    name: str
    given_name: str = None
    family_name: str = None
    ids: List[RegistrantIDIn] = None
    registration_date: date = None
    phone_numbers: List[PhoneNumberIn] = None
    email: str = None
    address: str = None
    gender: str = None
    birthdate: date = None
    birth_place: str = None
    is_group = False
    relationships_1: List[Relationship1In] = None
    relationships_2: List[Relationship2In] = None
    kind: List[
        GroupMembershipKindInfo
    ] = None  # TODO: Would be nicer to have it as a list of str
