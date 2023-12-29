from concurs import ConcursPlace


def get_programs_by_snils_in_vuz(vuz_total: dict[str, list[ConcursPlace]], target_snils: str) -> list[str]:
    result=[]
    for program, abiturients in vuz_total.items():
        if target_snils in abiturients:
            result.append(program)
    return result