from backend.generic.models.utils import TimestampMixin


class Degree(TimestampMixin):
    def __init__(self, code, full_name, avatar=None):
        super().__init__()
        self.code = code
        self.full_name = full_name
        self.avatar = avatar

        # Keys from other collections
        self.institutions = []
        self.tutors = []
        self.students = []

    def add_institution(self, institution_id):
        if not institution_id or institution_id in self.institutions:
            return
        self.institutions.append(institution_id)

    def remove_institution(self, institution_id):
        if not institution_id or institution_id not in self.institutions:
            return
        self.institutions.remove(institution_id)

    def add_tutor(self, tutor_id):
        if not tutor_id or tutor_id in self.tutors:
            return
        self.tutors.append(tutor_id)

    def remove_tutor(self, tutor_id):
        if not tutor_id or tutor_id not in self.tutors:
            return
        self.tutors.remove(tutor_id)

    def add_student(self, student_id):
        if not student_id or student_id in self.students:
            return
        self.students.append(student_id)

    def remove_student(self, student_id):
        if not student_id or student_id not in self.students:
            return
        self.students.remove(student_id)


class Institution(TimestampMixin):
    def __init__(self, email, full_name, avatar=None, location=None):
        super().__init__()
        self.email = email
        self.full_name = full_name
        self.avatar = avatar

        # Keys from other collections
        self.location = location
        self.coordinators = []
        self.degrees = []
        self.tutors = []
        self.students = []
        self.internships = []

    def update_location(self, location):
        if not location:
            return
        self.location = location

    def add_coordinator(self, coordinator_id):
        if not coordinator_id or coordinator_id in self.coordinators:
            return
        self.coordinators.append(coordinator_id)

    def remove_coordinator(self, coordinator_id):
        if not coordinator_id or coordinator_id not in self.coordinators:
            return
        self.coordinators.remove(coordinator_id)

    def add_degree(self, degree_id):
        if not degree_id or degree_id in self.degrees:
            return
        self.degrees.append(degree_id)

    def remove_degree(self, degree_id):
        if not degree_id or degree_id not in self.degrees:
            return
        self.degrees.remove(degree_id)

    def add_tutor(self, tutor_id):
        if not tutor_id or tutor_id in self.tutors:
            return
        self.tutors.append(tutor_id)

    def remove_tutor(self, tutor_id):
        if not tutor_id or tutor_id not in self.tutors:
            return
        self.tutors.remove(tutor_id)

    def add_student(self, student_id):
        if not student_id or student_id in self.students:
            return
        self.students.append(student_id)

    def remove_student(self, student_id):
        if not student_id or student_id not in self.students:
            return
        self.students.remove(student_id)

    def add_internship(self, internship_id):
        if not internship_id or internship_id in self.internships:
            return
        self.internships.append(internship_id)

    def remove_internship(self, internship_id):
        if not internship_id or internship_id not in self.internships:
            return
        self.internships.remove(internship_id)
