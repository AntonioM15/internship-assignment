from bson import ObjectId
from datetime import datetime
from pymongo import DESCENDING

from backend.generic.models.companies import Company
from backend.generic.models.institutions import Institution, Degree
from backend.generic.models.internships import Internship
from backend.generic.models.users import Coordinator, Worker, Student, Tutor, Admin
from backend.generic.models.utils import Observation
from backend.test.test_utils import BaseTestClass


class TestUserModels(BaseTestClass):
    # User instances
    coordinator_1 = Coordinator(
        email="coordinator_email@gmail.com",
        hashed_password="1234",
        official_id='10000001A',
        full_name='Coordinator name',
        institution=ObjectId('FFFF1111FFFF1111FFFF1111'),
        observations=[ObjectId('FF22FF22FF22FF22FF22FF22')]
    )
    coordinator_1._id = ObjectId('AAAA1111AAAA1111AAAA1111')

    coordinator_2 = Coordinator(
        email="coordinator_2_email@gmail.com",
        hashed_password="4321",
        official_id='10000011A',
        full_name='Coordinator 2 name',
        institution=ObjectId('FFFF1111FFFF1111FFFF1111'),
        observations=[ObjectId('FF2BFF2BFF2BFF2BFF2BFF2B')]
    )
    coordinator_2._id = ObjectId('AAAA1111AAAA1111AAAA111B')

    coordinator_3 = Coordinator(
        email="coordinator_3_email@gmail.com",
        hashed_password="3412",
        official_id='10000111A',
        full_name='Coordinator 3 name',
        institution=ObjectId('FFFF11BBFFFF11BBFFFF11BB'),
        observations=[ObjectId('FF2CFF2CFF2CFF2CFF2CFF2C')]
    )
    coordinator_3._id = ObjectId('AAAA1111AAAA1111AAAA111C')

    worker_1 = Worker(
        email="worker_email@gmail.com",
        hashed_password="1234",
        official_id='10000002B',
        full_name='Worker name',
        company=ObjectId('FFFF2222FFFF2222FFFF2222'),
        interns=[ObjectId('CCCC3333CCCC3333CCCC3333')],
        internships=[ObjectId('FFFF3333FFFF3333FFFF3333')]
    )
    worker_1._id = ObjectId('BBBB2222BBBB2222BBBB2222')

    worker_2 = Worker(
        email="worker_2_email@gmail.com",
        hashed_password="4321",
        official_id='10000012B',
        full_name='Worker 2 name',
        company=ObjectId('FFFF22BBFFFF22BBFFFF22BB'),
        interns=[ObjectId('CCCC3333CCCC3333CCCC333B')],
        internships=[ObjectId('FFFF33BBFFFF33BBFFFF33BB')]
    )
    worker_2._id = ObjectId('BBBB2222BBBB2222BBBB222B')

    worker_3 = Worker(
        email="worker_3_email@gmail.com",
        hashed_password="3412",
        official_id='10000112B',
        full_name='Worker 3 name',
        company=ObjectId('FFFF2222FFFF2222FFFF2222'),
        interns=[ObjectId('CCCC3333CCCC3333CCCC333C')],
        internships=[ObjectId('FFFF33CCFFFF33CCFFFF33CC')]
    )
    worker_3._id = ObjectId('BBBB2222BBBB2222BBBB222C')

    student_1 = Student(
        email="student_email@gmail.com",
        hashed_password="1234",
        official_id='10000003C',
        full_name='Student name',
        status='assigned',
        institution=ObjectId('FFFF1111FFFF1111FFFF1111'),
        degree=ObjectId('FFFF4444FFFF4444FFFF4444'),
        internship=ObjectId('FFFF3333FFFF3333FFFF3333'),
        observations=[ObjectId('FF22FF22FF22FF22FF22FF22')]
    )
    student_1._id = ObjectId('CCCC3333CCCC3333CCCC3333')

    student_2 = Student(
        email="student_2_email@gmail.com",
        hashed_password="4321",
        official_id='10000013C',
        full_name='Student 2 name',
        status='provisional',
        institution=ObjectId('FFFF1111FFFF1111FFFF1111'),
        degree=ObjectId('FFFF44BBFFFF44BBFFFF44BB'),
        internship=ObjectId('FFFF33BBFFFF33BBFFFF33BB'),
        observations=[ObjectId('FF2BFF2BFF2BFF2BFF2BFF2B')]
    )
    student_2._id = ObjectId('CCCC3333CCCC3333CCCC333B')

    student_3 = Student(
        email="student_3_email@gmail.com",
        hashed_password="3412",
        official_id='10000113C',
        full_name='Student 3 name',
        status='assigned',
        institution=ObjectId('FFFF11BBFFFF11BBFFFF11BB'),
        degree=ObjectId('FFFF4444FFFF4444FFFF4444'),
        internship=ObjectId('FFFF33CCFFFF33CCFFFF33CC'),
        observations=[ObjectId('FF2CFF2CFF2CFF2CFF2CFF2C')]
    )
    student_3._id = ObjectId('CCCC3333CCCC3333CCCC333C')

    tutor_1 = Tutor(
        email="tutor_email@gmail.com",
        hashed_password="1234",
        official_id='10000004D',
        full_name='Tutor name',
        status='assigned',
        institution=ObjectId('FFFF1111FFFF1111FFFF1111'),
        degrees=[ObjectId('FFFF4444FFFF4444FFFF4444')],
        students=[ObjectId('CCCC3333CCCC3333CCCC3333')],
        internships=[ObjectId('FFFF3333FFFF3333FFFF3333')]
    )
    tutor_1._id = ObjectId('DDDD4444DDDD4444DDDD4444')

    tutor_2 = Tutor(
        email="tutor_2_email@gmail.com",
        hashed_password="4321",
        official_id='10000014D',
        full_name='Tutor 2 name',
        status='provisional',
        institution=ObjectId('FFFF1111FFFF1111FFFF1111'),
        degrees=[ObjectId('FFFF44BBFFFF44BBFFFF44BB')],
        students=[ObjectId('CCCC3333CCCC3333CCCC333B')],
        internships=[ObjectId('FFFF33BBFFFF33BBFFFF33BB')]
    )
    tutor_2._id = ObjectId('DDDD4444DDDD4444DDDD444B')

    tutor_3 = Tutor(
        email="tutor_3_email@gmail.com",
        hashed_password="3412",
        official_id='10000114D',
        full_name='Tutor 3 name',
        status='assigned',
        institution=ObjectId('FFFF11BBFFFF11BBFFFF11BB'),
        degrees=[ObjectId('FFFF4444FFFF4444FFFF4444'), ObjectId('FFFF44BBFFFF44BBFFFF44BB')],
        students=[ObjectId('CCCC3333CCCC3333CCCC333C')],
        internships=[ObjectId('FFFF33CCFFFF33CCFFFF33CC')]
    )
    tutor_3._id = ObjectId('DDDD4444DDDD4444DDDD444C')

    admin_1 = Admin(
        email="admin_email@gmail.com",
        hashed_password="1234",
        official_id='10000005E',
        full_name='Admin name'
    )
    admin_1._id = ObjectId('EEEE5555EEEE5555EEEE5555')

    admin_2 = Admin(
        email="admin_2_email@gmail.com",
        hashed_password="4321",
        official_id='10000015E',
        full_name='Admin 2 name'
    )
    admin_2._id = ObjectId('EEEE5555EEEE5555EEEE555B')

    admin_3 = Admin(
        email="admin_3_email@gmail.com",
        hashed_password="3412",
        official_id='10000115E',
        full_name='Admin 3 name'
    )
    admin_3._id = ObjectId('EEEE5555EEEE5555EEEE555C')

    # Related instances
    observation_1 = Observation(
        text='Observation text',
        creator=ObjectId('AAAA1111AAAA1111AAAA1111'),
        receiver=ObjectId('CCCC3333CCCC3333CCCC3333')
    )
    observation_1._id = ObjectId('FF22FF22FF22FF22FF22FF22')

    observation_2 = Observation(
        text='Observation text 2',
        creator=ObjectId('AAAA1111AAAA1111AAAA111B'),
        receiver=ObjectId('CCCC3333CCCC3333CCCC333B')
    )
    observation_2._id = ObjectId('FF2BFF2BFF2BFF2BFF2BFF2B')

    observation_3 = Observation(
        text='Observation text 3',
        creator=ObjectId('AAAA1111AAAA1111AAAA111C'),
        receiver=ObjectId('CCCC3333CCCC3333CCCC333C')
    )
    observation_3._id = ObjectId('FF2CFF2CFF2CFF2CFF2CFF2C')

    institution_1 = Institution(
        email='institution_email@gmail.com',
        full_name='Institution name',
    )
    institution_1._id = ObjectId('FFFF1111FFFF1111FFFF1111')

    institution_2 = Institution(
        email='institution_2_email@gmail.com',
        full_name='Institution 2 name',
    )
    institution_2._id = ObjectId('FFFF11BBFFFF11BBFFFF11BB')

    company_1 = Company(
        full_name='Company name',
        field='Programacion'
    )
    company_1._id = ObjectId('FFFF2222FFFF2222FFFF2222')

    company_2 = Company(
        full_name='Company 2 name',
        field='Inteligencia Artificial'
    )
    company_2._id = ObjectId('FFFF22BBFFFF22BBFFFF22BB')

    internship_1 = Internship(
        kind='regular',
        status='assigned',
        starting_day=datetime(2024, 1, 1),
        finishing_day=datetime(2024, 6, 20),
        title='Backend developer',
        description='New Flask API for internal usage',
    )
    internship_1._id = ObjectId('FFFF3333FFFF3333FFFF3333')

    internship_2 = Internship(
        kind='regular',
        status='provisional',
        starting_day=datetime(2024, 2, 1),
        finishing_day=datetime(2024, 7, 20),
        title='Frontend developer',
        description='New vue admin pages',
    )
    internship_2._id = ObjectId('FFFF33BBFFFF33BBFFFF33BB')

    internship_3 = Internship(
        kind='regular',
        status='assigned',
        starting_day=datetime(2024, 3, 1),
        finishing_day=datetime(2024, 8, 20),
        title='AI developer',
        description='New AI chat in the platform',
    )
    internship_3._id = ObjectId('FFFF33CCFFFF33CCFFFF33CC')

    degree_1 = Degree(
        code='PRG',
        full_name='Programacion'
    )
    degree_1._id = ObjectId('FFFF4444FFFF4444FFFF4444')

    degree_2 = Degree(
        code='IA',
        full_name='Inteligencia Artificial'
    )
    degree_2._id = ObjectId('FFFF44BBFFFF44BBFFFF44BB')

    def test_db_returns_no_document_before_user_insertion(self):
        expected_result = None
        obtained_result = self.db.users.find_one({"_id": ObjectId('000000000000000000000000')})
        self.assertEqual(expected_result, obtained_result)

    # COORDINATOR
    def test_db_returns_one_document_after_coordinator_insertion(self):
        Coordinator.put(self.db, self.coordinator_1)
        obtained_result = self.db.users.find_one({"_id": ObjectId('AAAA1111AAAA1111AAAA1111')})
        self.assertIsNotNone(obtained_result)
        self.assertEqual(ObjectId('AAAA1111AAAA1111AAAA1111'), obtained_result["_id"])
        self.assertEqual("coordinator_email@gmail.com", obtained_result["email"])
        self.assertEqual("1234", obtained_result["hashed_password"])
        self.assertEqual('10000001A', obtained_result["official_id"])
        self.assertEqual('Coordinator name', obtained_result["full_name"])
        self.assertEqual(ObjectId('FFFF1111FFFF1111FFFF1111'), obtained_result["institution"])
        self.assertEqual([ObjectId('FF22FF22FF22FF22FF22FF22')], obtained_result["observations"])

    def test_db_returns_multiple_documents_after_multiple_coordinator_insertion(self):
        Coordinator.put_multi(self.db, [self.coordinator_2, self.coordinator_3])
        coordinator_ids = [ObjectId('AAAA1111AAAA1111AAAA111B'), ObjectId('AAAA1111AAAA1111AAAA111C')]

        # Test only these two ids are returned
        query = {"_id": {"$in": coordinator_ids}}
        obtained_result = self.db.users.find(query).sort("created_date", DESCENDING)
        doc_count = 0
        for coordinator in obtained_result:
            self.assertIsNotNone(coordinator)
            self.assertIn(coordinator.get('_id'), coordinator_ids)
            doc_count += 1
        self.assertEqual(2, doc_count)

        # Test only coordinator_2 is returned
        query["email"] = "coordinator_2_email@gmail.com"
        obtained_result = self.db.users.find(query).sort("created_date", DESCENDING)
        doc_count = 0
        for coordinator in obtained_result:
            self.assertIsNotNone(coordinator)
            self.assertIn(coordinator.get('_id'), coordinator_ids)
            self.assertEqual(coordinator.get('email'), "coordinator_2_email@gmail.com")
            doc_count += 1
        self.assertEqual(1, doc_count)

    # WORKER
    def test_db_returns_one_document_after_worker_insertion(self):
        Worker.put(self.db, self.worker_1)
        obtained_result = self.db.users.find_one({"_id": ObjectId('BBBB2222BBBB2222BBBB2222')})
        self.assertIsNotNone(obtained_result)
        self.assertEqual(ObjectId('BBBB2222BBBB2222BBBB2222'), obtained_result["_id"])
        self.assertEqual("worker_email@gmail.com", obtained_result["email"])
        self.assertEqual("1234", obtained_result["hashed_password"])
        self.assertEqual('10000002B', obtained_result["official_id"])
        self.assertEqual('Worker name', obtained_result["full_name"])
        self.assertEqual(ObjectId('FFFF2222FFFF2222FFFF2222'), obtained_result["company"])
        self.assertEqual([ObjectId('CCCC3333CCCC3333CCCC3333')], obtained_result["interns"])
        self.assertEqual([ObjectId('FFFF3333FFFF3333FFFF3333')], obtained_result["internships"])

    def test_db_returns_multiple_documents_after_multiple_worker_insertion(self):
        Worker.put_multi(self.db, [self.worker_2, self.worker_3])
        worker_ids = [ObjectId('BBBB2222BBBB2222BBBB222B'), ObjectId('BBBB2222BBBB2222BBBB222C')]

        # Test only these two ids are returned
        query = {"_id": {"$in": worker_ids}}
        obtained_result = self.db.users.find(query).sort("created_date", DESCENDING)
        doc_count = 0
        for worker in obtained_result:
            self.assertIsNotNone(worker)
            self.assertIn(worker.get('_id'), worker_ids)
            doc_count += 1
        self.assertEqual(2, doc_count)

        # Test only worker_2 is returned
        query["full_name"] = "Worker 2 name"
        obtained_result = self.db.users.find(query).sort("created_date", DESCENDING)
        doc_count = 0
        for worker in obtained_result:
            self.assertIsNotNone(worker)
            self.assertIn(worker.get('_id'), worker_ids)
            self.assertEqual(worker.get('full_name'), "Worker 2 name")
            doc_count += 1
        self.assertEqual(1, doc_count)

    # STUDENT
    def test_db_returns_one_document_after_student_insertion(self):
        Student.put(self.db, self.student_1)
        obtained_result = self.db.users.find_one({"_id": ObjectId('CCCC3333CCCC3333CCCC3333')})
        self.assertIsNotNone(obtained_result)
        self.assertEqual(ObjectId('CCCC3333CCCC3333CCCC3333'), obtained_result["_id"])
        self.assertEqual("student_email@gmail.com", obtained_result["email"])
        self.assertEqual("1234", obtained_result["hashed_password"])
        self.assertEqual('10000003C', obtained_result["official_id"])
        self.assertEqual('Student name', obtained_result["full_name"])
        self.assertEqual('assigned', obtained_result["status"])
        self.assertEqual(ObjectId('FFFF1111FFFF1111FFFF1111'), obtained_result["institution"])
        self.assertEqual(ObjectId('FFFF4444FFFF4444FFFF4444'), obtained_result["degree"])
        self.assertEqual(ObjectId('FFFF3333FFFF3333FFFF3333'), obtained_result["internship"])
        self.assertEqual([ObjectId('FF22FF22FF22FF22FF22FF22')], obtained_result["observations"])

    def test_db_returns_multiple_documents_after_multiple_student_insertion(self):
        Student.put_multi(self.db, [self.student_2, self.student_3])
        student_ids = [ObjectId('CCCC3333CCCC3333CCCC333B'), ObjectId('CCCC3333CCCC3333CCCC333C')]

        # Test only these two ids are returned
        query = {"_id": {"$in": student_ids}}
        obtained_result = self.db.users.find(query).sort("created_date", DESCENDING)
        doc_count = 0
        for student in obtained_result:
            self.assertIsNotNone(student)
            self.assertIn(student.get('_id'), student_ids)
            doc_count += 1
        self.assertEqual(2, doc_count)

        # Test only student_2 is returned
        query["status"] = "provisional"
        obtained_result = self.db.users.find(query).sort("created_date", DESCENDING)
        doc_count = 0
        for student in obtained_result:
            self.assertIsNotNone(student)
            self.assertIn(student.get('_id'), student_ids)
            self.assertEqual(student.get('status'), "provisional")
            doc_count += 1
        self.assertEqual(1, doc_count)

    # TUTOR
    def test_db_returns_one_document_after_tutor_insertion(self):
        Tutor.put(self.db, self.tutor_1)
        obtained_result = self.db.users.find_one({"_id": ObjectId('DDDD4444DDDD4444DDDD4444')})
        self.assertIsNotNone(obtained_result)
        self.assertEqual(ObjectId('DDDD4444DDDD4444DDDD4444'), obtained_result["_id"])
        self.assertEqual("tutor_email@gmail.com", obtained_result["email"])
        self.assertEqual("1234", obtained_result["hashed_password"])
        self.assertEqual('10000004D', obtained_result["official_id"])
        self.assertEqual('Tutor name', obtained_result["full_name"])
        self.assertEqual('assigned', obtained_result["status"])
        self.assertEqual(ObjectId('FFFF1111FFFF1111FFFF1111'), obtained_result["institution"])
        self.assertEqual([ObjectId('FFFF4444FFFF4444FFFF4444')], obtained_result["degrees"])
        self.assertEqual([ObjectId('CCCC3333CCCC3333CCCC3333')], obtained_result["students"])
        self.assertEqual([ObjectId('FFFF3333FFFF3333FFFF3333')], obtained_result["internships"])

    def test_db_returns_multiple_documents_after_multiple_tutor_insertion(self):
        Tutor.put_multi(self.db, [self.tutor_2, self.tutor_3])
        tutor_ids = [ObjectId('DDDD4444DDDD4444DDDD444B'), ObjectId('DDDD4444DDDD4444DDDD444C')]

        # Test only these two ids are returned
        query = {"_id": {"$in": tutor_ids}}
        obtained_result = self.db.users.find(query).sort("created_date", DESCENDING)
        doc_count = 0
        for tutor in obtained_result:
            self.assertIsNotNone(tutor)
            self.assertIn(tutor.get('_id'), tutor_ids)
            doc_count += 1
        self.assertEqual(2, doc_count)

        # Test only tutor_2 is returned
        query["official_id"] = "10000014D"
        obtained_result = self.db.users.find(query).sort("created_date", DESCENDING)
        doc_count = 0
        for tutor in obtained_result:
            self.assertIsNotNone(tutor)
            self.assertIn(tutor.get('_id'), tutor_ids)
            self.assertEqual(tutor.get('official_id'), "10000014D")
            doc_count += 1
        self.assertEqual(1, doc_count)

    # ADMIN
    def test_db_returns_one_document_after_admin_insertion(self):
        Admin.put(self.db, self.admin_1)
        obtained_result = self.db.users.find_one({"_id": ObjectId('EEEE5555EEEE5555EEEE5555')})
        self.assertIsNotNone(obtained_result)
        self.assertEqual(ObjectId('EEEE5555EEEE5555EEEE5555'), obtained_result["_id"])
        self.assertEqual("admin_email@gmail.com", obtained_result["email"])
        self.assertEqual("1234", obtained_result["hashed_password"])
        self.assertEqual('10000005E', obtained_result["official_id"])
        self.assertEqual('Admin name', obtained_result["full_name"])

    def test_db_returns_multiple_documents_after_multiple_admin_insertion(self):
        Admin.put_multi(self.db, [self.admin_2, self.admin_3])
        admin_ids = [ObjectId('EEEE5555EEEE5555EEEE555B'), ObjectId('EEEE5555EEEE5555EEEE555C')]

        # Test only these two ids are returned
        query = {"_id": {"$in": admin_ids}}
        obtained_result = self.db.users.find(query).sort("created_date", DESCENDING)
        doc_count = 0
        for admin in obtained_result:
            self.assertIsNotNone(admin)
            self.assertIn(admin.get('_id'), admin_ids)
            doc_count += 1
        self.assertEqual(2, doc_count)

        # Test only admin_2 is returned
        query["full_name"] = "Admin 2 name"
        obtained_result = self.db.users.find(query).sort("created_date", DESCENDING)
        doc_count = 0
        for admin in obtained_result:
            self.assertIsNotNone(admin)
            self.assertIn(admin.get('_id'), admin_ids)
            self.assertEqual(admin.get('full_name'), "Admin 2 name")
            doc_count += 1
        self.assertEqual(1, doc_count)
