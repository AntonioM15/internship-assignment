from bson import ObjectId
from pymongo import DESCENDING

from backend.generic.models.institutions import Institution, Degree
from test_utils import BaseTestClass


class TestInstitutionModel(BaseTestClass):
    # Institution instances
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

    institution_3 = Institution(
        email='institution_3_email@gmail.com',
        full_name='Institution 3 name',
    )
    institution_3._id = ObjectId('FFFF11CCFFFF11CCFFFF11CC')

    def test_db_returns_no_document_before_user_insertion(self):
        expected_result = None
        obtained_result = self.db.institutions.find_one({"_id": ObjectId('000000000000000000000000')})
        self.assertEqual(expected_result, obtained_result)

    def test_db_returns_one_document_after_institution_insertion(self):
        Institution.put(self.db, self.institution_1)
        obtained_result = self.db.institutions.find_one({"_id": ObjectId('FFFF1111FFFF1111FFFF1111')})
        self.assertIsNotNone(obtained_result)
        self.assertEqual(ObjectId('FFFF1111FFFF1111FFFF1111'), obtained_result["_id"])
        self.assertEqual("institution_email@gmail.com", obtained_result["email"])
        self.assertEqual("Institution name", obtained_result["full_name"])

    def test_db_returns_multiple_documents_after_multiple_institution_insertion(self):
        Institution.put_multi(self.db, [self.institution_2, self.institution_3])
        institution_ids = [ObjectId('FFFF11BBFFFF11BBFFFF11BB'), ObjectId('FFFF11CCFFFF11CCFFFF11CC')]

        # Test only these two ids are returned
        query = {"_id": {"$in": institution_ids}}
        obtained_result = self.db.institutions.find(query).sort("created_date", DESCENDING)
        doc_count = 0
        for institution in obtained_result:
            self.assertIsNotNone(institution)
            self.assertIn(institution.get('_id'), institution_ids)
            doc_count += 1
        self.assertEqual(2, doc_count)

        # Test only institution_2 is returned
        query["full_name"] = "Institution 2 name"
        obtained_result = self.db.institutions.find(query).sort("created_date", DESCENDING)
        doc_count = 0
        for institution in obtained_result:
            self.assertIsNotNone(institution)
            self.assertIn(institution.get('_id'), institution_ids)
            self.assertEqual(institution.get('full_name'), "Institution 2 name")
            doc_count += 1
        self.assertEqual(1, doc_count)


class TestDegreeModel(BaseTestClass):
    # Degree instances
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

    degree_3 = Degree(
        code='SWEB',
        full_name='Seguridad Web'
    )
    degree_3._id = ObjectId('FFFF44CCFFFF44CCFFFF44CC')

    def test_db_returns_no_document_before_user_insertion(self):
        expected_result = None
        obtained_result = self.db.degrees.find_one({"_id": ObjectId('000000000000000000000000')})
        self.assertEqual(expected_result, obtained_result)

    def test_db_returns_one_document_after_degree_insertion(self):
        Degree.put(self.db, self.degree_1)
        obtained_result = self.db.degrees.find_one({"_id": ObjectId('FFFF4444FFFF4444FFFF4444')})
        self.assertIsNotNone(obtained_result)
        self.assertEqual(ObjectId('FFFF4444FFFF4444FFFF4444'), obtained_result["_id"])
        self.assertEqual("PRG", obtained_result["code"])
        self.assertEqual("Programacion", obtained_result["full_name"])

    def test_db_returns_multiple_documents_after_multiple_degree_insertion(self):
        Degree.put_multi(self.db, [self.degree_2, self.degree_3])
        degree_ids = [ObjectId('FFFF44BBFFFF44BBFFFF44BB'), ObjectId('FFFF44CCFFFF44CCFFFF44CC')]

        # Test only these two ids are returned
        query = {"_id": {"$in": degree_ids}}
        obtained_result = self.db.degrees.find(query).sort("created_date", DESCENDING)
        doc_count = 0
        for degree in obtained_result:
            self.assertIsNotNone(degree)
            self.assertIn(degree.get('_id'), degree_ids)
            doc_count += 1
        self.assertEqual(2, doc_count)

        # Test only degree_2 is returned
        query["code"] = "IA"
        obtained_result = self.db.degrees.find(query).sort("created_date", DESCENDING)
        doc_count = 0
        for degree in obtained_result:
            self.assertIsNotNone(degree)
            self.assertIn(degree.get('_id'), degree_ids)
            self.assertEqual(degree.get('code'), "IA")
            doc_count += 1
        self.assertEqual(1, doc_count)
