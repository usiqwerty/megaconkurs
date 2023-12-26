from classes import ConcursPlace
def list_to_dict(l_data: list[ConcursPlace]) -> dict[str, ConcursPlace]:
    d_data=dict()
    for x in l_data:
        d_data[x.snils]=x
    return d_data

def get_programs_by_snils_in_vuz(vuz_total: dict[str, list[ConcursPlace]], target_snils: str) -> list[str]:
    result=[]
    for program, abiturients in vuz_total.items():
        if target_snils in abiturients:
            result.append(program)
    return result