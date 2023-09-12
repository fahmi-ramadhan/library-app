from django.test import TestCase, Client
from main.models import Item

class mainTest(TestCase):
    def test_main_url_is_exist(self):
        response = Client().get('/main/')
        self.assertEqual(response.status_code, 200)

    def test_main_using_main_template(self):
        response = Client().get('/main/')
        self.assertTemplateUsed(response, 'main.html')

class itemTest(TestCase):
    def test_item(self):
        item = Item.objects.create(
            name="Operating System Concepts",
            author="Abraham Silberschatz, Peter B. Galvin, and Greg Gagne",
            category="Computer Science",
            amount=10,
            description="Operating System Concepts is a book written by Abraham Silberschatz, Peter B. Galvin, and Greg Gagne. It is an informative guide to operating systems with an overview of all the major aspects. The book deals with topics like process, operating systems and their functioning, and design. It also looks at special-purpose systems, storage management, security, distributed systems and memory."
        )
        self.assertEqual(item.name, "Operating System Concepts")
        self.assertEqual(item.author, "Abraham Silberschatz, Peter B. Galvin, and Greg Gagne")
        self.assertEqual(item.category, "Computer Science")
        self.assertEqual(item.amount, 10)
        self.assertEqual(item.description, "Operating System Concepts is a book written by Abraham Silberschatz, Peter B. Galvin, and Greg Gagne. It is an informative guide to operating systems with an overview of all the major aspects. The book deals with topics like process, operating systems and their functioning, and design. It also looks at special-purpose systems, storage management, security, distributed systems and memory.")