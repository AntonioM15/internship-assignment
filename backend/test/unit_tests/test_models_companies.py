from bson import ObjectId
from pymongo import DESCENDING

from backend.generic.models.companies import Company
from test_utils import BaseTestClass


class TestCompanyModel(BaseTestClass):
    # Company instances
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

    company_3 = Company(
        full_name='Company 3 name',
        field='Seguridad Web'
    )
    company_3._id = ObjectId('FFFF22CCFFFF22CCFFFF22CC')

    def test_db_returns_no_document_before_user_insertion(self):
        expected_result = None
        obtained_result = self.db.companies.find_one({"_id": ObjectId('000000000000000000000000')})
        self.assertEqual(expected_result, obtained_result)

    def test_db_returns_one_document_after_company_insertion(self):
        Company.put(self.db, self.company_1)
        obtained_result = self.db.companies.find_one({"_id": ObjectId('FFFF2222FFFF2222FFFF2222')})
        self.assertIsNotNone(obtained_result)
        self.assertEqual(ObjectId('FFFF2222FFFF2222FFFF2222'), obtained_result["_id"])
        self.assertEqual("Company name", obtained_result["full_name"])
        self.assertEqual("Programacion", obtained_result["field"])

    def test_db_returns_multiple_documents_after_multiple_company_insertion(self):
        Company.put_multi(self.db, [self.company_2, self.company_3])
        company_ids = [ObjectId('FFFF22BBFFFF22BBFFFF22BB'), ObjectId('FFFF22CCFFFF22CCFFFF22CC')]

        # Test only these two ids are returned
        query = {"_id": {"$in": company_ids}}
        obtained_result = self.db.companies.find(query).sort("created_date", DESCENDING)
        doc_count = 0
        for company in obtained_result:
            self.assertIsNotNone(company)
            self.assertIn(company.get('_id'), company_ids)
            doc_count += 1
        self.assertEqual(2, doc_count)

        # Test only company_2 is returned
        query["field"] = "Inteligencia Artificial"
        obtained_result = self.db.companies.find(query).sort("created_date", DESCENDING)
        doc_count = 0
        for company in obtained_result:
            self.assertIsNotNone(company)
            self.assertIn(company.get('_id'), company_ids)
            self.assertEqual(company.get('field'), "Inteligencia Artificial")
            doc_count += 1
        self.assertEqual(1, doc_count)
