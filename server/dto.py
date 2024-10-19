class Student:
    def __init__(self, index):
        self.index = index

class DeansOffice:
    def __init__(self):
        self.students = []

    def add_student(self, student):
        if not any(existing_student.index == student.index for existing_student in self.students):
            self.students.append(student)
            return True
        return False


    def update_student(self, old_index, new_index):
        for student in self.students:
            if student.index == old_index:
                student.index =  new_index
                return True
        return False

    def delete_student(self, index):
        self.students = [student for student in self.students if student.index != index]

    def get_students(self):
        return [student.index for student in self.students]

    def generate_random_students(self, amount=1000):
        for i in range(amount):
            index = str(i).zfill(6)
            self.add_student(Student(f"s{index}"))

