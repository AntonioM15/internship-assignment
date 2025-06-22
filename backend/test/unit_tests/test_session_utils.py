from flask import session, jsonify

from backend.generic.session_utils import save_session, clear_session, limited_access, login_required
from backend.test.test_utils import BaseTestClass


class BaseSessionTestClass(BaseTestClass):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Testing endpoints
        @cls.app.route('/login')
        def simulate_login():
            save_session("test@example.com", "coordinator")
            return jsonify(dict(session))

        @cls.app.route('/login-admin')
        def simulate_login_admin():
            save_session("test@example.com", "admin")
            return jsonify(dict(session))

        @cls.app.route('/logout')
        def simulate_logout():
            clear_session()
            return jsonify(dict(session))

        @cls.app.route('/protected')
        @login_required
        def protected_route():
            return jsonify({"status": "success", "message": "Acceso permitido"})

        @cls.app.route('/admin-only')
        @limited_access(['admin'])
        def admin_only():
            return jsonify({"status": "success", "message": "Admin OK"})


class TestSaveSession(BaseSessionTestClass):

    def test_there_is_no_session_before_save_session(self):
        with self.client.session_transaction() as test_session:
            self.assertFalse('email' in test_session)
            self.assertFalse('role' in test_session)

    def test_session_is_saved_after_save_session(self):
        _ = self.client.get('/login')
        with self.client.session_transaction() as test_session:
            self.assertEqual(test_session['email'], "test@example.com")
            self.assertEqual(test_session['role'], "coordinator")


class TestClearSession(BaseSessionTestClass):

    def test_session_is_cleared_when_no_session(self):
        with self.client.session_transaction() as test_session:
            self.assertFalse('email' in test_session)
            self.assertFalse('role' in test_session)

    def test_session_is_cleared_after_logout(self):
        _ = self.client.get('/login')
        with self.client.session_transaction() as test_session:
            self.assertEqual(test_session['email'], "test@example.com")
            self.assertEqual(test_session['role'], "coordinator")

        _ = self.client.get('/logout')
        with self.client.session_transaction() as test_session:
            self.assertFalse('email' in test_session)
            self.assertFalse('role' in test_session)


class TestLoginRequired(BaseSessionTestClass):

    def test_login_required_without_session(self):
        res = self.client.get('/protected')
        data = res.get_json()
        self.assertEqual(res.status_code, 401)
        self.assertEqual("Usuario no autorizado. Por favor, inicie sesión.", data.get("message"))

    def test_login_required_with_session(self):
        _ = self.client.get('/login')
        with self.client.session_transaction() as test_session:
            self.assertEqual(test_session['email'], "test@example.com")
            self.assertEqual(test_session['role'], "coordinator")

        res = self.client.get('/protected')
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual("Acceso permitido", data.get("message"))


class TestLimitedAccess(BaseSessionTestClass):

    def test_limited_access_without_session(self):
        res = self.client.get('/admin-only')
        data = res.get_json()
        self.assertEqual(res.status_code, 403)
        self.assertEqual("Usuario no autorizado. Página restringida.", data.get("message"))

    def test_limited_access_denied(self):
        _ = self.client.get('/login')
        with self.client.session_transaction() as test_session:
            self.assertEqual(test_session['email'], "test@example.com")
            self.assertEqual(test_session['role'], "coordinator")

        res = self.client.get('/admin-only')
        data = res.get_json()
        self.assertEqual(res.status_code, 403)
        self.assertEqual("Usuario no autorizado. Página restringida.", data.get("message"))

    def test_limited_access_allowed(self):
        _ = self.client.get('/login-admin')
        with self.client.session_transaction() as test_session:
            self.assertEqual(test_session['email'], "test@example.com")
            self.assertEqual(test_session['role'], "admin")

        res = self.client.get('/admin-only')
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual("Admin OK", data.get("message"))
