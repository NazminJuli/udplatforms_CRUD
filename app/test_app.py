import unittest
from werkzeug.datastructures import ImmutableMultiDict
from start import app


class Flasktestcases (unittest.TestCase):

    def test_home(self):
        tester = app.test_client(self)
        response = tester.get('/',follow_redirects = True)
        assert response.status_code == 200


    # test if all fields are included in register form
    def test_registration_form(self): # test registration with NOT NULL constraint
        tester = app.test_client(self)
        response = tester.get('/register')
        assert response.status_code == 200
        html = response.get_data(as_text=True)

        # make sure all the fields are included
        assert 'name="firstname"' in html
        assert 'name="lastname"' in html
        assert 'name="street"' in html
        assert 'name="city"' in html
        assert 'name="state"' in html
        assert 'name="zip_code"' in html


    def test_registration_form_parent(self):
        tester = app.test_client(self)
        response = tester.post('/register', data = {
            'firstname':'Nazmin', 'lastname': 'Nahar', 'street':'Loan ofc',
            'city':'Jashore', 'state':'Khulna', 'zip_code':'7400'}, follow_redirects =True)
        assert response.status_code == 200

        with app.app_context():
         response.request.form = ImmutableMultiDict([("btn1", "save")])
         response.request.form = ImmutableMultiDict([("btn2", "add_child")])


    def test_add_child(self):
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['parentid'] = 1

            response = client.post('/addchild', data = {'child_firstname':'Arhaam', 'child_lastname':'Hossain','parent_id':session['parentid']})
            assert response.status_code == 200

if __name__ == "__main__":
    unittest.main()