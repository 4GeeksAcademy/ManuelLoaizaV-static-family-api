class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name
        self._members = []
        self._next_id = 1

    def _generate_id(self):
        generated_id = self._next_id
        self._next_id += 1
        return generated_id
    
    def _search(self, member_id):
        if len(self._members) == 0:
            return None
        if self._members[-1]["id"] < member_id:
            return None
        if self._members[0]["id"] >= member_id:
            if self._members[0]["id"] == member_id:
                return 0
            return None
        
        l = 0
        r = len(self._members) - 1
        while r - l > 1:
            m = (l + r) // 2
            if self._members[m]["id"] >= member_id:
                r = m
            else:
                l = m

        if self._members[r]["id"] == member_id:
            return r
        return None

    def add_member(self, member):
        member["id"] = self._generate_id()
        self._members.append(member)
        return self._members[-1]

    def delete_member(self, id):
        member_index = self._search(id)
        if member_index is None:
            return False
        del self._members[member_index]
        return True

    def get_member(self, id):
        member_index = self._search(id)
        if member_index is None:
            return None
        return self._members[member_index]

    def get_all_members(self):
        return self._members
