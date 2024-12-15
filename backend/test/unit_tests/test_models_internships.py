from bson import ObjectId
from datetime import datetime
from pymongo import DESCENDING

from backend.generic.models.internships import Internship
from backend.test.test_utils import BaseTestClass


class TestInternshipModel(BaseTestClass):
    # Internship instances
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

    def test_db_returns_no_document_before_user_insertion(self):
        expected_result = None
        obtained_result = self.db.internships.find_one({"_id": ObjectId('000000000000000000000000')})
        self.assertEqual(expected_result, obtained_result)

    def test_db_returns_one_document_after_internship_insertion(self):
        Internship.put(self.db, self.internship_1)
        obtained_result = self.db.internships.find_one({"_id": ObjectId('FFFF3333FFFF3333FFFF3333')})
        self.assertIsNotNone(obtained_result)
        self.assertEqual(ObjectId('FFFF3333FFFF3333FFFF3333'), obtained_result["_id"])
        self.assertEqual("regular", obtained_result["kind"])
        self.assertEqual("assigned", obtained_result["status"])
        self.assertEqual(datetime(2024, 1, 1), obtained_result["starting_day"])
        self.assertEqual(datetime(2024, 6, 20), obtained_result["finishing_day"])
        self.assertEqual('Backend developer', obtained_result["title"])
        self.assertEqual('New Flask API for internal usage', obtained_result["description"])

    def test_db_returns_multiple_documents_after_multiple_internship_insertion(self):
        Internship.put_multi(self.db, [self.internship_2, self.internship_3])
        internship_ids = [ObjectId('FFFF33BBFFFF33BBFFFF33BB'), ObjectId('FFFF33CCFFFF33CCFFFF33CC')]

        # Test only these two ids are returned
        query = {"_id": {"$in": internship_ids}}
        obtained_result = self.db.internships.find(query).sort("created_date", DESCENDING)
        doc_count = 0
        for internship in obtained_result:
            self.assertIsNotNone(internship)
            self.assertIn(internship.get('_id'), internship_ids)
            doc_count += 1
        self.assertEqual(2, doc_count)

        # Test only coordinator_2 is returned
        query["status"] = "provisional"
        obtained_result = self.db.internships.find(query).sort("created_date", DESCENDING)
        doc_count = 0
        for internship in obtained_result:
            self.assertIsNotNone(internship)
            self.assertIn(internship.get('_id'), internship_ids)
            self.assertEqual(internship.get('status'), "provisional")
            doc_count += 1
        self.assertEqual(1, doc_count)
