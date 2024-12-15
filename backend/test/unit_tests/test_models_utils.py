import unittest

from bson import ObjectId
from copy import deepcopy
from datetime import datetime
from pymongo import DESCENDING

from backend.generic.models.utils import str_date_to_datetime, serialize_document, Location, Notification, Observation
from backend.test.test_utils import is_dict_json_friendly, BaseTestClass


class TestStrToDatetimeMethod(unittest.TestCase):
    none_value = None
    empty_str = ''
    valid_date_str = '2000-01-01'
    invalid_date_str = '00-01-01'

    def test_none_value_returns_none(self):
        expected_result = None
        obtained_result = str_date_to_datetime(self.none_value)
        self.assertEqual(expected_result, obtained_result)

    def test_empty_str_returns_none(self):
        expected_result = None
        obtained_result = str_date_to_datetime(self.empty_str)
        self.assertEqual(expected_result, obtained_result)

    def test_valid_date_str_returns_datetime(self):
        expected_result = datetime(2000, 1, 1)
        obtained_result = str_date_to_datetime(self.valid_date_str)
        self.assertEqual(expected_result, obtained_result)

    def test_invalid_date_str_raises_error(self):
        self.assertRaises(ValueError, str_date_to_datetime, self.invalid_date_str)


class TestSerializeDocumentMethod(unittest.TestCase):
    # Users
    coordinator_dict = {'created_date': datetime(2024, 11, 29, 23, 34, 31, 589211), 'last_updated': datetime(2024, 11, 29, 23, 34, 31, 589214), 'email': 'coordinator_email@gmail.com', 'hashed_password': '1234', 'role': 'coordinator', 'official_id': '10000001A', 'full_name': 'Coordinator name', 'hidden': False, 'avatar': None, 'location': {}, 'notifications': [], 'institution': ObjectId('ffff1111ffff1111ffff1111'), 'observations': [ObjectId('ff11ff11ff11ff11ff11ff11')], '_id': ObjectId('aaaa1111aaaa1111aaaa1111')}
    worker_dict = {'created_date': datetime(2024, 11, 30, 20, 57, 57, 896428), 'last_updated': datetime(2024, 11, 30, 20, 57, 57, 896428), 'email': 'worker_email@gmail.com', 'hashed_password': '1234', 'role': 'worker', 'official_id': '10000002B', 'full_name': 'Worker name', 'hidden': False, 'avatar': None, 'location': {}, 'notifications': [], 'company': ObjectId('ffff2222ffff2222ffff2222'), 'interns': [ObjectId('cccc3333cccc3333cccc3333')], 'internships': [ObjectId('ffff3333ffff3333ffff3333')], '_id': ObjectId('bbbb2222bbbb2222bbbb2222')}
    student_dict = {'created_date': datetime(2024, 11, 29, 23, 40, 24, 995604), 'last_updated': datetime(2024, 11, 29, 23, 40, 24, 995604), 'email': 'student_email@gmail.com', 'hashed_password': '1234', 'role': 'student', 'official_id': '10000003C', 'full_name': 'Student name', 'hidden': False, 'avatar': None, 'location': {}, 'notifications': [], 'status': 'assigned', 'internship_type': None, 'institution': ObjectId('ffff1111ffff1111ffff1111'), 'degree': ObjectId('ffff4444ffff4444ffff4444'), 'internship': ObjectId('ffff3333ffff3333ffff3333'), 'observations': [ObjectId('ff22ff22ff22ff22ff22ff22')], '_id': ObjectId('cccc3333cccc3333cccc3333')}
    tutor_dict = {'created_date': datetime(2024, 11, 30, 21, 1, 4, 412191), 'last_updated': datetime(2024, 11, 30, 21, 1, 4, 412191), 'email': 'tutor_email@gmail.com', 'hashed_password': '1234', 'role': 'tutor', 'official_id': '10000004D', 'full_name': 'Tutor name', 'hidden': False, 'avatar': None, 'location': {}, 'notifications': [], 'status': 'assigned', 'institution': ObjectId('ffff1111ffff1111ffff1111'), 'degrees': [ObjectId('ffff4444ffff4444ffff4444')], 'students': [ObjectId('cccc3333cccc3333cccc3333')], 'internships': [ObjectId('ffff3333ffff3333ffff3333')], '_id': ObjectId('dddd4444dddd4444dddd4444')}
    admin_dict = {'created_date': datetime(2024, 11, 30, 21, 2, 31, 913470), 'last_updated': datetime(2024, 11, 30, 21, 2, 31, 913471), 'email': 'admin_email@gmail.com', 'hashed_password': '1234', 'role': 'admin', 'official_id': '10000005E', 'full_name': 'Admin name', 'hidden': False, 'avatar': None, 'location': {}, 'notifications': [], '_id': ObjectId('eeee5555eeee5555eeee5555')}

    # Utils
    location_dict = {'created_date': datetime(2024, 11, 30, 23, 56, 30, 300258), 'last_updated': datetime(2024, 11, 30, 23, 56, 30, 300259), 'coordinates': [39.469836, -0.376989], 'country': 'Spain', 'city': 'Valencia', 'postal_code': '46002', 'address': "Pl. de l'Ajuntament, 1", 'users': [], 'institutions': [], 'companies': [], 'internships': []}
    notification_dict = {'created_date': datetime(2024, 11, 30, 23, 45, 9, 41383), 'last_updated': datetime(2024, 11, 30, 23, 45, 9, 41388), 'title': 'Notification title', 'description': 'Notification description', 'role': 'student', 'read': False, 'sender': None, 'receiver': ObjectId('cccc3333cccc3333cccc3333'), '_id': ObjectId('ff44ff44ff44ff44ff44ff44')}
    observation_dict = {'created_date': datetime(2024, 11, 30, 23, 32, 31, 174368), 'last_updated': datetime(2024, 11, 30, 23, 32, 31, 174369), 'text': 'Observation text', 'creator': ObjectId('aaaa1111aaaa1111aaaa1111'), 'receiver': ObjectId('cccc3333cccc3333cccc3333'), '_id': ObjectId('ff22ff22ff22ff22ff22ff22')}

    # Institutions
    institution_dict = {'created_date': datetime(2024, 11, 30, 23, 18, 11, 357159), 'last_updated': datetime(2024, 11, 30, 23, 18, 11, 357159), 'email': 'institution_email@gmail.com', 'full_name': 'Institution name', 'avatar': None, 'location': None, 'coordinators': [], 'degrees': [], 'tutors': [], 'students': [], 'internships': [], '_id': ObjectId('ffff1111ffff1111ffff1111')}
    degree_dict = {'created_date': datetime(2024, 11, 30, 23, 20, 58, 777026), 'last_updated': datetime(2024, 11, 30, 23, 20, 58, 777027), 'code': 'PRG', 'full_name': 'Programacion', 'avatar': None, 'institutions': [], 'tutors': [], 'students': [], '_id': ObjectId('ffff4444ffff4444ffff4444')}

    # Companies
    company_dict = {'created_date': datetime(2024, 11, 30, 23, 48, 5, 921754), 'last_updated': datetime(2024, 11, 30, 23, 48, 5, 921754), 'full_name': 'Company name', 'field': 'Programacion', 'hidden': False, 'avatar': None, 'location': None, 'workers': [], 'observations': [], 'internships': [], '_id': ObjectId('ffff2222ffff2222ffff2222')}

    # Internships
    internship_dict = {'created_date': datetime(2024, 11, 30, 23, 17, 8, 908912), 'last_updated': datetime(2024, 11, 30, 23, 17, 8, 908912), 'kind': 'regular', 'status': 'assigned', 'starting_day': datetime(2024, 1, 1, 0, 0), 'finishing_day': datetime(2024, 6, 20, 0, 0), 'title': 'Backend developer', 'description': 'New Flask API for internal usage', 'location': None, 'student': None, 'worker': None, 'tutor': None, 'company': None, 'institution': None, '_id': ObjectId('ffff3333ffff3333ffff3333')}

    def test_none_value(self):
        expected_result = {}
        obtained_result = serialize_document(None)
        self.assertEqual(expected_result, obtained_result)

    def test_empty_dict(self):
        expected_result = {}
        obtained_result = serialize_document({})
        self.assertEqual(expected_result, obtained_result)

    def test_coordinator_without_serialization(self):
        expected_result = False
        obtained_result = is_dict_json_friendly(deepcopy(self.coordinator_dict))
        self.assertEqual(expected_result, obtained_result)

    def test_coordinator_with_serialization(self):
        expected_result = True
        serialized_value = serialize_document(deepcopy(self.coordinator_dict))
        obtained_result = is_dict_json_friendly(serialized_value)
        self.assertEqual(expected_result, obtained_result)

    def test_worker_without_serialization(self):
        expected_result = False
        obtained_result = is_dict_json_friendly(deepcopy(self.worker_dict))
        self.assertEqual(expected_result, obtained_result)

    def test_worker_with_serialization(self):
        expected_result = True
        serialized_value = serialize_document(deepcopy(self.worker_dict))
        obtained_result = is_dict_json_friendly(serialized_value)
        self.assertEqual(expected_result, obtained_result)

    def test_student_without_serialization(self):
        expected_result = False
        obtained_result = is_dict_json_friendly(deepcopy(self.student_dict))
        self.assertEqual(expected_result, obtained_result)

    def test_student_with_serialization(self):
        expected_result = True
        serialized_value = serialize_document(deepcopy(self.student_dict))
        obtained_result = is_dict_json_friendly(serialized_value)
        self.assertEqual(expected_result, obtained_result)

    def test_tutor_without_serialization(self):
        expected_result = False
        obtained_result = is_dict_json_friendly(deepcopy(self.tutor_dict))
        self.assertEqual(expected_result, obtained_result)

    def test_tutor_with_serialization(self):
        expected_result = True
        serialized_value = serialize_document(deepcopy(self.tutor_dict))
        obtained_result = is_dict_json_friendly(serialized_value)
        self.assertEqual(expected_result, obtained_result)

    def test_admin_without_serialization(self):
        expected_result = False
        obtained_result = is_dict_json_friendly(deepcopy(self.admin_dict))
        self.assertEqual(expected_result, obtained_result)

    def test_admin_with_serialization(self):
        expected_result = True
        serialized_value = serialize_document(deepcopy(self.admin_dict))
        obtained_result = is_dict_json_friendly(serialized_value)
        self.assertEqual(expected_result, obtained_result)

    def test_location_without_serialization(self):
        expected_result = False
        obtained_result = is_dict_json_friendly(deepcopy(self.location_dict))
        self.assertEqual(expected_result, obtained_result)

    def test_location_with_serialization(self):
        expected_result = True
        serialized_value = serialize_document(deepcopy(self.location_dict))
        obtained_result = is_dict_json_friendly(serialized_value)
        self.assertEqual(expected_result, obtained_result)

    def test_notification_without_serialization(self):
        expected_result = False
        obtained_result = is_dict_json_friendly(deepcopy(self.notification_dict))
        self.assertEqual(expected_result, obtained_result)

    def test_notification_with_serialization(self):
        expected_result = True
        serialized_value = serialize_document(deepcopy(self.notification_dict))
        obtained_result = is_dict_json_friendly(serialized_value)
        self.assertEqual(expected_result, obtained_result)

    def test_observation_without_serialization(self):
        expected_result = False
        obtained_result = is_dict_json_friendly(deepcopy(self.observation_dict))
        self.assertEqual(expected_result, obtained_result)

    def test_observation_with_serialization(self):
        expected_result = True
        serialized_value = serialize_document(deepcopy(self.observation_dict))
        obtained_result = is_dict_json_friendly(serialized_value)
        self.assertEqual(expected_result, obtained_result)

    def test_institution_without_serialization(self):
        expected_result = False
        obtained_result = is_dict_json_friendly(deepcopy(self.institution_dict))
        self.assertEqual(expected_result, obtained_result)

    def test_institution_with_serialization(self):
        expected_result = True
        serialized_value = serialize_document(deepcopy(self.institution_dict))
        obtained_result = is_dict_json_friendly(serialized_value)
        self.assertEqual(expected_result, obtained_result)

    def test_degree_without_serialization(self):
        expected_result = False
        obtained_result = is_dict_json_friendly(deepcopy(self.degree_dict))
        self.assertEqual(expected_result, obtained_result)

    def test_degree_with_serialization(self):
        expected_result = True
        serialized_value = serialize_document(deepcopy(self.degree_dict))
        obtained_result = is_dict_json_friendly(serialized_value)
        self.assertEqual(expected_result, obtained_result)

    def test_company_without_serialization(self):
        expected_result = False
        obtained_result = is_dict_json_friendly(deepcopy(self.company_dict))
        self.assertEqual(expected_result, obtained_result)

    def test_company_with_serialization(self):
        expected_result = True
        serialized_value = serialize_document(deepcopy(self.company_dict))
        obtained_result = is_dict_json_friendly(serialized_value)
        self.assertEqual(expected_result, obtained_result)

    def test_internship_without_serialization(self):
        expected_result = False
        obtained_result = is_dict_json_friendly(deepcopy(self.internship_dict))
        self.assertEqual(expected_result, obtained_result)

    def test_internship_with_serialization(self):
        expected_result = True
        serialized_value = serialize_document(deepcopy(self.internship_dict))
        obtained_result = is_dict_json_friendly(serialized_value)
        self.assertEqual(expected_result, obtained_result)


class TestLocationModel(BaseTestClass):
    location_1 = Location(
        coordinates=[39.469836, -0.376989],
        country='Spain',
        city='Valencia',
        postal_code='46002',
        address='Pl. de l\'Ajuntament, 1'
    )
    location_1._id = ObjectId('FF33FF33FF33FF33FF33FF33')

    location_2 = Location(
        coordinates=[39.474722, -0.358333],
        country='Spain',
        city='Valencia',
        postal_code='46010',
        address='Avenida de Suecia'
    )
    location_2._id = ObjectId('FF3BFF3BFF3BFF3BFF3BFF3B')

    location_3 = Location(
        coordinates=[40.45306, -3.68835],
        country='Spain',
        city='Madrid',
        postal_code='28036',
        address='Paseo de la Castellana'
    )
    location_3._id = ObjectId('FF3CFF3CFF3CFF3CFF3CFF3C')

    def test_db_returns_no_document_before_location_insertion(self):
        expected_result = None
        obtained_result = self.db.locations.find_one({"_id": ObjectId('000000000000000000000000')})
        self.assertEqual(expected_result, obtained_result)

    def test_db_returns_one_document_after_location_insertion(self):
        Location.put(self.db, self.location_1)
        obtained_result = self.db.locations.find_one({"_id": ObjectId('FF33FF33FF33FF33FF33FF33')})
        self.assertIsNotNone(obtained_result)
        self.assertEqual(ObjectId('FF33FF33FF33FF33FF33FF33'), obtained_result["_id"])
        self.assertEqual([39.469836, -0.376989], obtained_result["coordinates"])
        self.assertEqual('Spain', obtained_result["country"])
        self.assertEqual('Valencia', obtained_result["city"])
        self.assertEqual('46002', obtained_result["postal_code"])
        self.assertEqual('Pl. de l\'Ajuntament, 1', obtained_result["address"])

    def test_db_returns_multiple_documents_after_multiple_location_insertion(self):
        Location.put_multi(self.db, [self.location_2, self.location_3])
        location_ids = [ObjectId('FF3BFF3BFF3BFF3BFF3BFF3B'), ObjectId('FF3CFF3CFF3CFF3CFF3CFF3C')]

        # Test only these two ids are returned
        query = {"_id": {"$in": location_ids}}
        obtained_result = self.db.locations.find(query).sort("created_date", DESCENDING)
        doc_count = 0
        for location in obtained_result:
            self.assertIsNotNone(location)
            self.assertIn(location.get('_id'), location_ids)
            doc_count += 1
        self.assertEqual(2, doc_count)

        # Test only Mestalla is returned
        query["city"] = 'Valencia'
        obtained_result = self.db.locations.find(query).sort("created_date", DESCENDING)
        doc_count = 0
        for location in obtained_result:
            self.assertIsNotNone(location)
            self.assertIn(location.get('_id'), location_ids)
            self.assertEqual(location.get('city'), 'Valencia')
            doc_count += 1
        self.assertEqual(1, doc_count)


class TestNotificationModel(BaseTestClass):
    notification_1 = Notification(
        title='Notification title',
        description='Notification description',
        role='student',
        read=False,
        sender=None,
        receiver=ObjectId('CCCC3333CCCC3333CCCC3333')
    )
    notification_1._id = ObjectId('FF44FF44FF44FF44FF44FF44')

    notification_2 = Notification(
        title='Notification title 2',
        description='Notification description 2',
        role='student',
        read=False,
        sender=None,
        receiver=ObjectId('CCCC3333CCCC3333CCCC3333')
    )
    notification_2._id = ObjectId('FF4BFF4BFF4BFF4BFF4BFF4B')

    notification_3 = Notification(
        title='Notification title 3',
        description='Notification description 3',
        role='tutor',
        read=False,
        sender=None,
        receiver=ObjectId('DDDD4444DDDD4444DDDD4444')
    )
    notification_3._id = ObjectId('FF4CFF4CFF4CFF4CFF4CFF4C')

    def test_db_returns_no_document_before_notification_insertion(self):
        expected_result = None
        obtained_result = self.db.notifications.find_one({"_id": ObjectId('000000000000000000000000')})
        self.assertEqual(expected_result, obtained_result)

    def test_db_returns_one_document_after_notification_insertion(self):
        Notification.put(self.db, self.notification_1)
        obtained_result = self.db.notifications.find_one({"_id": ObjectId('FF44FF44FF44FF44FF44FF44')})
        self.assertIsNotNone(obtained_result)
        self.assertEqual(ObjectId('FF44FF44FF44FF44FF44FF44'), obtained_result["_id"])
        self.assertEqual('Notification title', obtained_result["title"])
        self.assertEqual('Notification description', obtained_result["description"])
        self.assertEqual('student', obtained_result["role"])
        self.assertEqual(False, obtained_result["read"])
        self.assertEqual(None, obtained_result["sender"])
        self.assertEqual(ObjectId('CCCC3333CCCC3333CCCC3333'), obtained_result["receiver"])

    def test_db_returns_multiple_documents_after_multiple_notification_insertion(self):
        Notification.put_multi(self.db, [self.notification_2, self.notification_3])
        notification_ids = [ObjectId('FF4BFF4BFF4BFF4BFF4BFF4B'), ObjectId('FF4CFF4CFF4CFF4CFF4CFF4C')]

        # Test only these two ids are returned
        query = {"_id": {"$in": notification_ids}}
        obtained_result = self.db.notifications.find(query).sort("created_date", DESCENDING)
        doc_count = 0
        for notification in obtained_result:
            self.assertIsNotNone(notification)
            self.assertIn(notification.get('_id'), notification_ids)
            doc_count += 1
        self.assertEqual(2, doc_count)

        # Test only tutor notification is returned
        query["role"] = 'tutor'
        obtained_result = self.db.notifications.find(query).sort("created_date", DESCENDING)
        doc_count = 0
        for notification in obtained_result:
            self.assertIsNotNone(notification)
            self.assertIn(notification.get('_id'), notification_ids)
            self.assertEqual(notification.get('role'), 'tutor')
            doc_count += 1
        self.assertEqual(1, doc_count)


class TestObservationModel(BaseTestClass):
    observation_1 = Observation(
        text='Observation text',
        creator=ObjectId('AAAA1111AAAA1111AAAA1111'),
        receiver=ObjectId('CCCC3333CCCC3333CCCC3333')
    )
    observation_1._id = ObjectId('FF22FF22FF22FF22FF22FF22')

    observation_2 = Observation(
        text='Observation text 2',
        creator=ObjectId('AAAA1111AAAA1111AAAA1111'),
        receiver=ObjectId('CCCC3333CCCC3333CCCC3333')
    )
    observation_2._id = ObjectId('FF2BFF2BFF2BFF2BFF2BFF2B')

    observation_3 = Observation(
        text='Observation text 3',
        creator=ObjectId('AAAA1111AAAA1111AAAA1111'),
        receiver=ObjectId('DDDD4444DDDD4444DDDD4444')
    )
    observation_3._id = ObjectId('FF2CFF2CFF2CFF2CFF2CFF2C')

    def test_db_returns_no_document_before_observation_insertion(self):
        expected_result = None
        obtained_result = self.db.observations.find_one({"_id": ObjectId('000000000000000000000000')})
        self.assertEqual(expected_result, obtained_result)

    def test_db_returns_one_document_after_observation_insertion(self):
        Observation.put(self.db, self.observation_1)
        obtained_result = self.db.observations.find_one({"_id": ObjectId('FF22FF22FF22FF22FF22FF22')})
        self.assertIsNotNone(obtained_result)
        self.assertEqual(ObjectId('FF22FF22FF22FF22FF22FF22'), obtained_result["_id"])
        self.assertEqual('Observation text', obtained_result["text"])
        self.assertEqual(ObjectId('AAAA1111AAAA1111AAAA1111'), obtained_result["creator"])
        self.assertEqual(ObjectId('CCCC3333CCCC3333CCCC3333'), obtained_result["receiver"])

    def test_db_returns_multiple_documents_after_multiple_observation_insertion(self):
        Observation.put_multi(self.db, [self.observation_2, self.observation_3])
        observation_ids = [ObjectId('FF2BFF2BFF2BFF2BFF2BFF2B'), ObjectId('FF2CFF2CFF2CFF2CFF2CFF2C')]

        # Test only these two ids are returned
        query = {"_id": {"$in": observation_ids}}
        obtained_result = self.db.observations.find(query).sort("created_date", DESCENDING)
        doc_count = 0
        for observation in obtained_result:
            self.assertIsNotNone(observation)
            self.assertIn(observation.get('_id'), observation_ids)
            doc_count += 1
        self.assertEqual(2, doc_count)

        # Test only tutor notification is returned
        query["receiver"] = ObjectId('DDDD4444DDDD4444DDDD4444')
        obtained_result = self.db.observations.find(query).sort("created_date", DESCENDING)
        doc_count = 0
        for observation in obtained_result:
            self.assertIsNotNone(observation)
            self.assertIn(observation.get('_id'), observation_ids)
            self.assertEqual(observation.get('receiver'), ObjectId('DDDD4444DDDD4444DDDD4444'))
            doc_count += 1
        self.assertEqual(1, doc_count)
