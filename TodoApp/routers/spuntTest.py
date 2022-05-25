import sys
sys.path.append("..")
from fastapi import APIRouter,Depends,HTTPException,Request
import uuid

router=APIRouter(prefix="/Projects",tags=["Spunt"],responses={404:{"Description":"Not found"}})





from typing import Optional, List
# class Soilprofile(BaseModel):
#     id:str
#     lag_navn:List[str]
#     phi:Optional[List[float]]=0
#     c:Optional[List[float]]=0
#     c_inc:Optional[List[float]]=0
#     gamma_sat:[List[float]]
#     gamma_unsat:[List[float]]

#     @validator("lag_navn","phi","gamma_sat")
#     def length_of_list_equal(cls,field_value):
#         print(f'{cls} Field value {field_value')
#         return field_value





from dataclasses import dataclass,field
@dataclass
class SpuntBeregning:
    id:int
    phi:List[float]=field(default_factory=list)
    lag:List[str]=field(default_factory=list)
    f:Optional[List[float]]=field(default_factory=list)
    def calc(self):
        for i,Lag in enumerate(self.lag):
            if Lag.lower()=="sand":
                self.f.append((self.phi[i]*10)/12)
            elif Lag.lower()=="leire":
                self.f.append((self.phi[i]*5)/12)
        return self.f





@router.get("/Spunt/init")
async def spunt_init(lag:str,phi:float):
    global spunt
    spunt=SpuntBeregning(id=uuid.uuid4(),lag=[lag],phi=[phi])
    return {"Spunt initialized":{"lag":lag,"phi":phi}}



@router.post("/Spunt/add")
async def spunt_add(lag:str,phi:float):
    spunt.lag.append(lag)
    spunt.phi.append(phi)
    return {"Spunt added layer":{"lag":lag,"phi":phi}}

@router.put("/Spunt/update")
async def spunt_update(lag_modified:str,phi_modified:float):
    for index,Lag in enumerate(spunt.lag):
        if Lag==lag_modified:
            spunt.lag[index]=lag_modified
            spunt.phi[index]=phi_modified
    return {"Spunt updated ":{"lag":lag_modified,"phi":phi_modified}}



@router.get("/Spunt/calc")
async def spunt_calc():
    return spunt.calc()


@router.get("/Spunt/")
async def spunt_get():
    return spunt.__dict__


