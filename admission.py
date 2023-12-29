import concurs


def list_to_dict(l_data: list[concurs.ConcursPlace]) -> dict[int, list[concurs.ConcursPlace]]:
	d_data = dict()
	for x in l_data:
		if x.snils not in d_data:
			d_data[x.snils] = [x]
		else:
			d_data[x.snils].append(x)
	return d_data


def find_all_with_snils(target_snils: int, all_data: dict[int, list[concurs.ConcursPlace]]):
	return all_data.get(target_snils, [])
