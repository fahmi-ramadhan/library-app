# Library Management System

🌐[Link Aplikasi](https://youtu.be/dQw4w9WgXcQ?si=4shjklB1tHnOYQMi)🌐

Nama: Fahmi Ramadhan<br>
NPM: 2206026473<br>
Kelas: PBP A<br>


# Tugas 3: Implementasi _Form_ dan _Data Delivery_ pada Django

<details open>

## Perbedaan _form_ `POST` dan _form_ `GET` dalam Django

`POST` dan `GET` adalah dua metode HTTP yang digunakan saat berurusan dengan _form_. Berikut adalah perbedaannya.

### 1. POST
* Data _form_ dikemas oleh _browser_, di-_encode_ untuk pengiriman, dan kemudian dikirim ke _server_.
* Digunakan untuk _request_ yang dapat mengubah status sistem, seperti mengubah _database_
* Lebih aman untuk data sensitif seperti _password_ karena data tidak terlihat dalam URL dan tidak muncul dalam _browser history_ atau _server log_ dalam bentuk _plain text_.
* Cocok untuk mengirim data besar atau data biner seperti gambar, serta untuk formulir administrasi dengan perlindungan tambahan seperti CSRF (_Cross-site Request Forgery_) _protection_.

### 2. GET
* Data yang dikirimkan dikemas sebagai _string_ dan dijadikan bagian dari URL yang dikirimkan ke _server_.
* Digunakan untuk _request_ yang tidak memengaruhi status sistem.
* Data muncul dalam URL, yang berarti dapat terlihat dalam _browser history_ dan _server log_ sehingga kurang aman untuk data sensitif.
* Cocok untuk formulir pencarian web karena URL yang dihasilkan dapat dengan mudah di-_bookmark_, dibagikan, atau di-_resubmit_.

Sumber: https://docs.djangoproject.com/en/4.2/topics/forms/

## Perbedaan XML, JSON, dan HTML dalam konteks pengiriman data

### 1. XML (eXtensible Markup Language)
* XML adalah sebuah _markup language_ yang dirancang untuk menyimpan dan mengantarkan data yang mudah dibaca oleh manusia.
* XML menggunakan _tag-tag_ yang mendefinisikan struktur data dalam dokumen.

### 2. JSON (JavaScript Object Notation)
* JSON adalah sebuah format yang digunakan untuk menyimpan, membaca, dan menukar informasi dari _web server_ yang mudah dibaca oleh manusia.
* JSON menggunakan _key-value pairs_ untuk merepresentasikan data seperti object pada JavaScript.
* JSON biasanya lebih efisien dalam hal ukuran file dibandingkan dengan XML.

### 3. HTML (HyperText Markup Language)
* HTML adalah sebuah sebuah _markup language_ yang digunakan untuk mengatur tampilan dan struktur konten di halaman web.
* HTML mengandung _tag-tag_ bawaan untuk mengatur elemen-elemen halaman web dan biasanya memiliki atribut yang digunakan untuk menambahkan informasi tambahan mengenai elemen tersebut.

Jadi, perbedaan mendasar antara ketiganya adalah XML dan JSON digunakan untuk menyimpan dan mengirimkan data sedangkan HTML digunakan untuk mengatur tampilan halaman web.

## Mengapa JSON sering digunakan dalam pertukaran data antara aplikasi web modern?

* JSON mudah untuk dipahami oleh manusia karena menggunakan format _key-value pairs_ yang bentuknya sering ditemui di banyak bahasa pemrograman dibandingkan dengan XML yang menggunakan _tag_.
* JSON didukung oleh sebagian besar bahasa pemrograman modern sehingga data dalam format JSON dapat dengan mudah diolah dan dimanipulasi di berbagai _platform_. _Browser_ modern memiliki dukungan bawaan untuk melakukan _parsing_ dan konversi data JSON menjadi _object_ JavaScript.
* JSON memiliki format yang lebih ringan dibandingkan XML karena ukurannya yang lebih kecil, struktur yang lebih simpel, tidak adanya informasi yang redundan, seperti _closing tag_ atau _namespace_ sehingga mengurangi _bandwidth_ dan waktu pemrosesan yang dibutuhkan untuk transfer dan manipulasi data.

## Implementasi _Checklist_

### 1. Membuat input `form` untuk menambahkan objek model

Sebelum membuat _form_, saya membuat kerangka _views_ terlebih dahulu agar kode lebih terstruktur dan nantinya akan memudahkan saya untuk memastikan konsistensi desain dan memperkecil kemungkinan redundansi kode. Untuk itu, saya membuat berkas baru bernama `base.html` pada _folder_ `templates` di _root folder_ dan menjadikannya sebagai _template_ dasar dengan menyesuaikan isi `TEMPLATES` pada `settings.py`. Kemudian, saya mengubah `main.html` agar meng-_extends_ `base.html` dan _tag-tag_ html ada di dalam _block content_

Selanjutnya, saya membuat berkas `forms.py` pada direktori `main` untuk membuat struktur _form_ penambahan buku baru.

``` python
from django.forms import ModelForm
from main.models import Item

class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ["name", "author", "category", "amount", "description"]
```

Kemudian, saya membuat fungsi `add_book` yang menerima parameter `request` pada `views.py` untuk menerima data buku baru, menyimpannya ke _database_, dan kembali ke halaman utama setelah berhasil menyimpan.

```python
def add_book(request):
    form = ItemForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('main:show_main'))
    
    context = {'form': form}
    return render(request, "add_book.html", context)
```

Setelah fungsi dibuat, saya menambahkan _path url_ ke dalam `urlpatterns` pada `urls.py` di `main` untuk mengakses fungsi tersebut.

```python
urlpatterns = [
    ...
    path('add_book', add_book, name='add_book'),
    ...
]
```

Kemudian, saya membuat berkas `add_book.html` pada direktori `main/templates` yang berisi _fields_ `form` untuk menambahkan data buku baru dan tombol _submit_ untuk mengirimkan _request_ ke fungsi `add_book(request)`.

```html
{% extends 'base.html' %} 

{% block content %}
<h1>Add New Book</h1>

<form method="POST">
    {% csrf_token %}
    <table>
        {{ form.as_table }}
        <tr>
            <td></td>
            <td>
                <input type="submit" value="Add Book"/>
            </td>
        </tr>
    </table>
</form>

{% endblock %}
```

### 2. Menambahkan lima fungsi `views` untuk melihat objek yang sudah ditambahkan dalam format HTML, XML, JSON, XML _by_ ID, dan JSON _by_ ID

#### a. Fungsi untuk melihat objek dalam format HTML

Saya menambahkan `books` yang berisi semua _object Item_ dari _database_ ke dalam `context` pada fungsi `show_main` untuk ditampilkan di halaman utama.

```python
def show_main(request):
    books = Item.objects.all()

    context = {
        'app_name': 'Library Management System',
        'student_name': 'Fahmi Ramadhan',
        'class': 'PBP A',
        'books': books, 
    }

    return render(request, "main.html", context)
```

Selanjutnya, saya menambahkan kode pada `main.html` untuk menampilkan banyak judul buku yang ada **(BONUS)**, informasi setiap buku dalam bentuk tabel, serta tombol 'Add New Book' yang akan _redirect_ ke `add_book.html`.

```html
{% block content %}
    ...

    <h3>There are currently {{books|length}} book titles stored in the system</h3>

    <table>
        <tr>
            <th>Name</th>
            <th>Author</th>
            <th>Category</th>
            <th>Amount</th>
            <th>Description</th>
        </tr>

        {% for book in books %}
            <tr>
                <td>{{book.name}}</td>
                <td>{{book.author}}</td>
                <td>{{book.category}}</td>
                <td>{{book.amount}}</td>
                <td>{{book.description}}</td>
            </tr>
        {% endfor %}
    </table>

    <br />

    <a href="{% url 'main:add_book' %}">
        <button>
            Add New Book
        </button>
    </a>

{% endblock content %}
```

#### b. Fungsi untuk melihat objek dalam format XML, JSON, XML _by_ ID, dan JSON _by_ ID

```python
def show_xml(request):
    data = Item.objects.all()
    return HttpResponse(serializers.serialize('xml', data), content_type="application/xml")

def show_json(request):
    data = Item.objects.all()
    return HttpResponse(serializers.serialize('json', data), content_type="application/json")

def show_xml_by_id(request, id):
    data = Item.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = Item.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
```

### 3. Membuat routing URL untuk masing-masing `views`

Untuk membuat routing URL, saya membuka `urls.py` pada direktori `main`, kemudian meng-_import_ fungsi-fungsi `views` dan menambahkannya ke dalam `urlpatterns`.

```python
from django.urls import path
from main.views import show_main, add_book, show_xml, show_json, show_xml_by_id, show_json_by_id

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('add_book', add_book, name='add_book'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<int:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<int:id>/', show_json_by_id, name='show_json_by_id'),
]
```

### 4. Mengakses kelima URL di poin 2 menggunakan Postman

![HTML](Images/objectInHTML.png)
![XML](Images/objectInXML.png)
![JSON](Images/objectInJSON.png)
![XML By ID](Images/objectInXMLByID.png)
![JSON By ID](Images/objectInJSONByID.png)

### 5. Melakukan `add`-`commit`-`push` ke GitHub

Sebelum melakukan `add`-`commit`-`push`, saya membuat dan beralih ke _branch_ baru bernama `dev` dengan menggunakan perintah `git checkout -b dev`. Kemudian, saya baru melakukan `add`, `commit`, serta `push` menggunakan `git push origin dev`.

</details>

# Tugas 2: Implementasi _Model-View-Template_ (MVT) pada Django

<details>

## Implementasi _Checklist_

### 1. Membuat sebuah proyek Django baru.
Pertama-tama, saya membuat repositori GitHub baru bernama `library-app` dengan visibilitas _public_.
Setelah itu, saya membuat direktori lokal baru bernama `library_app` dan menginisiasi direktori tersebut sebagai repositori Git, menghubungkan repositori lokal dengan repositori GitHub, serta menambahkan _file_ `.gitignore`.
Kemudian, saya membuat _virtual environment_ pada direktori tersebut dengan menjalankan perintah berikut: <pre>python -m venv env</pre>
Selanjutnya, saya aktifkan _virtual environment_ tersebut dengan menjalankan perintah berikut: <pre>env\Scripts\activate.bat</pre>
Dalam _virtual environment_ tersebut, saya meng-_install_ _dependencies_ dari berkas `requirements.txt` yang berisi:
```
django
gunicorn
whitenoise
psycopg2-binary
requests
urllib3
coverage
```
dengan menjalankan perintah berikut: <pre>pip install -r requirements.txt</pre>
Setelah semua _dependencies_ ter-_install_, saya mulai membuat proyek Django dengan menjalankan perintah berikut: <pre>django-admin startproject library_app .</pre>
Setelah proyek dibuat, saya menambahkan `*` pada `ALLOWED_HOST` di `settings.py` agar aplikasi dapat diakses secara luas.

### 2. Membuat aplikasi dengan nama `main` pada proyek tersebut.
Untuk membuat aplikasi dengan nama `main`, saya menjalankan perintah berikut: <pre>python manage.py startapp main</pre>
Kemudian, saya menambahkan `'main'` pada `INSTALLED_APPS` di `settings.py` yang ada di direktori `library_app`.

### 3. Membuat model pada aplikasi `main` dengan nama `Item`.
model saya memiliki atribut sebagai berikut:
```python
class Item(models.Model):
    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    amount = models.IntegerField()
    description = models.TextField()
```
Selanjutnya, saya menjalankan perintah berikut untuk membuat migrasi model dan menerapkan migrasi tersebut ke dalam basis data lokal.
```
python manage.py makemigrations
python manage.py migrate
```
### 4. Membuat sebuah fungsi `views.py` untuk dikembalikan ke dalam sebuah _template_ HTML.
Dalam tahap ini, saya membuat fungsi `show_main` pada `views.py` untuk me-_render_ tampilan HTML dengan menggunakan data yang diberikan.
```python
from django.shortcuts import render

def show_main(request):
    context = {
        'app_name': 'Library Management System',
        'student_name': 'Fahmi Ramadhan',
        'class': 'PBP A',
        'name': 'Operating System Concepts',
        'author': 'Abraham Silberschatz, Peter B. Galvin, and Greg Gagne',
        'category': 'Computer Science',
        'amount': '10',
        'description': 'Operating System Concepts book is an informative guide to operating systems with an overview of all the major aspects. The book deals with topics like computer process, operating systems and their functioning, and design. It also looks at special-purpose systems, storage management, security, distributed systems and memory.'
    }

    return render(request, "main.html", context)
```
Selanjutnya, saya membuat _file_ `main.html` pada direktori `templates` di aplikasi `main` dan mengisinya untuk menampilkan nama aplikasi,
identitas saya, dan lainnya dari _dictionary_ `context` sebagai berikut:
```html
<h1>{{app_name}}</h1>

<h2>{{student_name}} - {{class}}</h2>

<p><strong>Name: </strong>{{name}}</p>
<p><strong>Author: </strong>{{author}}</p>
<p><strong>Category: </strong>{{category}}</p>
<p><strong>Amount: </strong>{{amount}}</p>
<p><strong>Description: </strong>{{description}}</p>
```

### 5. Membuat sebuah _routing_ pada `urls.py` aplikasi `main` untuk memetakan fungsi yang telah dibuat pada `views.py`.
Untuk membuat sebuah _routing_ yang memetakan fungsi `show_main` pada `views.py`, saya membuat _file_ `urls.py` yang berisi:
```python
from django.urls import path
from main.views import show_main

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
]
```

### 6. Melakukan _routing_ pada proyek agar dapat menjalankan aplikasi `main`.
Saya mengonfigurasi _routing_ URL proyek dengan menambahkan _path_ yang mengarah ke aplikasi `main` pada `urls.py` di direktori `library_app`.
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', include('main.urls')),
]
```

### 7. Melakukan _deployment_ ke Adaptable terhadap aplikasi yang sudah dibuat.
Untuk melakukan _deployment_ ke Adaptable, saya login ke [Adaptable.io](https://adaptable.io/) dengan menggunakan akun GitHub yang saya gunakan untuk membuat proyek. Kemudian, saya menghubungkan repositori proyek `library_app` ke Adaptable untuk membuat aplikasi baru di Adaptable. Saya memilih `Python App Template` sebagai _template deployment_ dan `PostgreSQL` sebagai tipe basis data yang digunakan. Selanjutnya, saya mengonfigurasikan versi Python dan _start command_. Kemudian, saya memasukkan nama aplikasi `library-app` yang akan menjadi _domain_ situs web aplikasi saya. Terakhir, saya centang bagian `HTTP listener on PORT` dan klik `Deploy App` untuk memulai proses _deployment_ aplikasi.

## Bagan _Client Request and Response_ Aplikasi Web Berbasis Django

![Alt text](Images/bagan.jpg)

1. _Client_ mengakses website dan _Web Server_ menerima _request_.
2. WSGI memproses server HTTP untuk situs web berbasis Python.
3. `urls.py` berisi path yang mengarahkan _request_ ke fungsi pada `views.py`.
4. `views.py` mengambil data dari `models.py` dan me-_render_ HTML dari _template_.
5. `models.py` berisi _class_ `model` untuk mengelola data pada _database_.

## Mengapa Menggunakan _Virtual Environment_?

_Virtual environment_ memungkinkan kita untuk membuat lingkungan terisolasi untuk setiap proyek Django kita. Dengan ini, kita bisa dengan mudah megelola berbagai dependensi untuk masing-masing proyek Django dan menghindari konflik antara `library` atau `package` dengan versi yang berbeda yang mungkin dibutuhkan oleh proyek yang berbeda. Selain itu, _virtual environment_ juga memudahkan kita dalam pemindahan proyek yang sedang dikembangkan ke _host_ lain tanpa khawatir akan konflik antara dependensi. Meskipun kita bisa saja membuat aplikasi web berbasis Django tanpa menggunakan _virtual environment_, tetapi ini tidak disarankan karena akan lebih sulit untuk mengelola berbagai dependensi dan lebih berisiko terjadi konflik dengan proyek-proyek lain.

## Penjelasan MVC, MVT, MVVM Beserta Perbedaannya

MVC, MVT, dan MVVM adalah beberapa contoh paradigma pemrograman web yang memisahkan komponen-komponen pada aplikasi, seperti logika dan tampilan aplikasi untuk memudahkan pengelolaannya.

- MVC memisahkan aplikasi menjadi tiga komponen, yaitu _model, view, dan controller_. _Model_ berisi definisi dari data-data yang akan disimpan ke dalam _database_. Kemudian, _view_ berhubungan dengan _user interface_ untuk menampilkan halaman ke pengguna. Sementara itu, _Controller_ berisi logika utama program yang mungkin memerlukan informasi dari _database_ melalui _model_.
- MVT memisahkan aplikasi menjadi tiga komponen, yaitu _mode, view, dan template_. Sama halnya seperti MVC, _model_ berisi definisi dari data-data yang akan disimpan ke _database_. Namun, perbedaan antara keduanya terletak pada _view_ dan _template_. _View_ dalam MVT melakukan fungsi yang sama dengan _controller_ dalam MVC, sedangkan _template_ dalam MVT melakukan fungsi yang sama dengan _view_ dalam MVC. Django adalah salah satu framework yang menggunakan MVT.
- MVVM memisahkan juga aplikasi menjadi tiga komponen, yaitu _model, view, dan view-model_. Secara dasar, MVVM mirip dengan MVC, di mana _model_ dan _view_ dalam kedua paradigma tersebut melakukan fungsi yang serupa. Kemudian, _view-model_ melakukan fungsi yang sama dengan _controller_ dalam MVC.

Secara keseluruhan, ketiganya memiliki tujuan yang serupa, yaitu mengisolasi logika aplikasi dari _user interface_. Namun, perbedaan utama di antara ketiganya terletak pada bagaimana okmponen-komponen tersebut disusun dan berhubungan satu sama lain.

## BONUS

Pada _file_ `tests.py`, saya menambahkan sebuah _unit test_ tambahan untuk mengetes apakah _model_ benar dan apakah data berhasil dimasukkan ke _database_.
```python
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
            description="Operating System Concepts book is an informative guide to operating systems with an overview of all the major aspects. The book deals with topics like computer process, operating systems and their functioning, and design. It also looks at special-purpose systems, storage management, security, distributed systems and memory."
        )
        self.assertEqual(item.name, "Operating System Concepts")
        self.assertEqual(item.author, "Abraham Silberschatz, Peter B. Galvin, and Greg Gagne")
        self.assertEqual(item.category, "Computer Science")
        self.assertEqual(item.amount, 10)
        self.assertEqual(item.description, "Operating System Concepts book is an informative guide to operating systems with an overview of all the major aspects. The book deals with topics like computer process, operating systems and their functioning, and design. It also looks at special-purpose systems, storage management, security, distributed systems and memory.")
```
Berikut adalah hasil _test_ dan _report_-nya:
```
(env) C:\Users\USER\library_app>coverage run --source="." manage.py test
Found 3 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
...
----------------------------------------------------------------------
Ran 3 tests in 0.054s

OK
Destroying test database for alias 'default'...

(env) C:\Users\USER\library_app>coverage report --show-missing
Name                                       Stmts   Miss  Cover   Missing
------------------------------------------------------------------------
library_app\__init__.py                        0      0   100%
library_app\asgi.py                            4      4     0%   10-16
library_app\settings.py                       18      0   100%
library_app\urls.py                            3      0   100%
library_app\wsgi.py                            4      4     0%   10-16
main\__init__.py                               0      0   100%
main\admin.py                                  1      0   100%
main\apps.py                                   4      0   100%
main\migrations\0001_initial.py                5      0   100%
main\migrations\0002_book_author.py            4      0   100%
main\migrations\0003_rename_book_item.py       4      0   100%
main\migrations\__init__.py                    0      0   100%
main\models.py                                 7      0   100%
main\tests.py                                 17      0   100%
main\urls.py                                   4      0   100%
main\views.py                                  4      0   100%
manage.py                                     12      2    83%   12-13
------------------------------------------------------------------------
TOTAL                                         91     10    89%
```
</details>