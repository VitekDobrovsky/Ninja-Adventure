
old_list = [1,2,3,4,5]

def flip_order(old_list):
		new_list = []
		odl_index = 0
		new_index = len(old_list) - 1
		
		for i in old_list:
			new_list.append(None)

		for i in new_list:
			new_list[new_index] = old_list[odl_index]
			new_index -= 1
			odl_index += 1

		return new_list

print(flip_order(old_list))