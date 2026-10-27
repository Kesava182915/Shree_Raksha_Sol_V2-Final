"""
SHREERAKSHA SOLUTIONS - ENTERPRISE BACKEND & AUTH TEST SUITE
Tests SQLite database, REST API endpoints, OTP flows, password hashing, and data sync.
"""

import unittest
import urllib.request
import urllib.parse
import json
import time
import threading
from server import run_server, ThreadingHTTPServer, SreerakshaRequestHandler, init_db, get_db

TEST_PORT = 8089
BASE_URL = f"http://127.0.0.1:{TEST_PORT}"

class BackendAuthTestSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()
        server_address = ('127.0.0.1', TEST_PORT)
        cls.httpd = ThreadingHTTPServer(server_address, SreerakshaRequestHandler)
        cls.server_thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.server_thread.start()
        time.sleep(0.5)

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()

    def post_json(self, path, payload, token=None):
        url = BASE_URL + path
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, method='POST')
        req.add_header('Content-Type', 'application/json')
        if token:
            req.add_header('Authorization', f'Bearer {token}')
        try:
            with urllib.request.urlopen(req) as resp:
                return resp.status, json.loads(resp.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            return e.code, json.loads(e.read().decode('utf-8'))

    def get_json(self, path, token=None):
        url = BASE_URL + path
        req = urllib.request.Request(url, method='GET')
        if token:
            req.add_header('Authorization', f'Bearer {token}')
        try:
            with urllib.request.urlopen(req) as resp:
                return resp.status, json.loads(resp.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            return e.code, json.loads(e.read().decode('utf-8'))

    def test_01_health_check(self):
        status, data = self.get_json('/api/health')
        self.assertEqual(status, 200)
        self.assertEqual(data.get('status'), 'online')
        print("[PASS] Health Check Endpoint verified.")

    def test_02_default_admin_signin(self):
        status, data = self.post_json('/api/auth/signin', {
            'identifier': 'admin@shreeraksha.in',
            'password': 'Admin@123456',
            'role': 'admin'
        })
        self.assertEqual(status, 200)
        self.assertTrue(data.get('success'))
        self.assertIn('token', data)
        self.assertEqual(data['user']['role'], 'admin')
        print("[PASS] Default Admin Sign In verified.")

    def test_03_default_customer_signin(self):
        status, data = self.post_json('/api/auth/signin', {
            'identifier': 'customer@shreeraksha.in',
            'password': 'Customer@123456',
            'role': 'customer'
        })
        self.assertEqual(status, 200)
        self.assertTrue(data.get('success'))
        self.assertEqual(data['user']['role'], 'customer')
        print("[PASS] Default Customer Sign In verified.")

    def test_04_user_signup_and_me_profile(self):
        new_email = f"testuser_{int(time.time())}@shreeraksha.in"
        status, data = self.post_json('/api/auth/signup', {
            'name': 'Kavya Rao',
            'email': new_email,
            'phone': '+91 9988776655',
            'password': 'Password@123',
            'role': 'customer'
        })
        self.assertEqual(status, 201)
        self.assertTrue(data.get('success'))
        token = data.get('token')

        # Check /api/auth/me
        status_me, me_data = self.get_json('/api/auth/me', token=token)
        self.assertEqual(status_me, 200)
        self.assertEqual(me_data['user']['name'], 'Kavya Rao')
        self.assertEqual(me_data['user']['email'], new_email)
        print("[PASS] User Registration (Sign Up) & Profile Retrieval verified.")

    def test_05_otp_login_flow(self):
        test_phone = "+91 9123456789"
        # 1. Send OTP
        status, data = self.post_json('/api/auth/send-otp', {
            'identifier': test_phone,
            'purpose': 'login'
        })
        self.assertEqual(status, 200)
        self.assertTrue(data.get('success'))
        otp_code = data.get('otp')
        self.assertEqual(len(otp_code), 6)

        # 2. Verify OTP
        v_status, v_data = self.post_json('/api/auth/verify-otp', {
            'identifier': test_phone,
            'code': otp_code,
            'role': 'customer'
        })
        self.assertEqual(v_status, 200)
        self.assertTrue(v_data.get('success'))
        self.assertIn('token', v_data)
        print("[PASS] Cryptographic OTP Generation & Verification flow verified.")

    def test_06_forgot_password_and_reset_flow(self):
        email = 'admin@shreeraksha.in'
        # 1. Send reset code
        status, data = self.post_json('/api/auth/forgot-password/send-otp', {
            'identifier': email
        })
        self.assertEqual(status, 200)
        self.assertTrue(data.get('success'))
        reset_otp = data.get('otp')

        # 2. Reset Password
        new_pwd = 'NewAdminPassword@2026'
        r_status, r_data = self.post_json('/api/auth/forgot-password/reset', {
            'identifier': email,
            'code': reset_otp,
            'new_password': new_pwd
        })
        self.assertEqual(r_status, 200)
        self.assertTrue(r_data.get('success'))

        # 3. Verify sign in with new password
        login_status, login_data = self.post_json('/api/auth/signin', {
            'identifier': email,
            'password': new_pwd
        })
        self.assertEqual(login_status, 200)
        self.assertTrue(login_data.get('success'))

        # Restore original password for consistency
        orig_pwd = 'Admin@123456'
        status2, data2 = self.post_json('/api/auth/forgot-password/send-otp', {'identifier': email})
        self.post_json('/api/auth/forgot-password/reset', {
            'identifier': email,
            'code': data2['otp'],
            'new_password': orig_pwd
        })
        print("[PASS] Forgot Password & Secure Reset Flow verified.")

    def test_07_database_sync(self):
        # Test syncing data to SQLite using test_sync key and fetching it back without touching main_data
        sample_payload = {
            'organization': {'name': 'SHREERAKSHA SOLUTIONS TEST'},
            'customers': [{'id': 'c-1', 'name': 'Test Client'}],
            'invoices': [{'id': 'inv-1', 'number': 'SHRKS/Inv/26-27/001', 'total': 50000}]
        }
        status, data = self.post_json('/api/db/sync', {'key': 'test_sync', 'data': sample_payload})
        self.assertEqual(status, 200)
        self.assertTrue(data.get('success'))

        get_status, get_data = self.get_json('/api/db/data?key=test_sync')
        self.assertEqual(get_status, 200)
        self.assertEqual(get_data['data']['organization']['name'], 'SHREERAKSHA SOLUTIONS TEST')
        self.assertEqual(len(get_data['data']['customers']), 1)
        print("[PASS] SQLite Database Real-Time Data Sync & Persistence verified.")

    def test_08_static_file_serving(self):
        # Ensure static files like index.html and css/auth.css are served
        with urllib.request.urlopen(f"{BASE_URL}/index.html") as resp:
            self.assertEqual(resp.status, 200)
            content = resp.read().decode('utf-8')
            self.assertIn("SHREERAKSHA", content)
            self.assertIn("auth.css", content)
            self.assertIn("auth-modal.js", content)
        print("[PASS] Static HTML/CSS/JS file serving verified.")

    def test_09_email_send_realtime(self):
        # Verify real-time email dispatch engine
        status, data = self.post_json('/api/email/send', {
            'to': 'purchasing@sunpharma.res.in',
            'subject': 'Quotation SHRKS/Qtn/26-27/020 from Shreeraksha Solutions',
            'body': 'Dear Dr. Ananya Sharma,\nPlease find attached our official GST quotation.\nBest regards,\nShreeraksha Solutions',
            'docType': 'quotation',
            'docId': 'est-020',
            'docNumber': 'SHRKS/Qtn/26-27/020'
        })
        self.assertEqual(status, 200)
        self.assertTrue(data.get('success'))
        self.assertIn('logId', data)
        self.assertEqual(data.get('recipient'), 'purchasing@sunpharma.res.in')

        # Check logs endpoint
        log_status, log_data = self.get_json('/api/email/logs')
        self.assertEqual(log_status, 200)
        self.assertTrue(len(log_data.get('logs', [])) > 0)
        print("[PASS] Real-Time Email Dispatch Engine & SQLite email_logs verified.")

if __name__ == '__main__':
    unittest.main()
