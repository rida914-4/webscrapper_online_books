import time
import os
import shutil
import csv
import pandas as pd
import booksearch as p
import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

home_path = "C:\\Users\\ridah.naseem\\"
base_path = "C:\\Users\\ridah.naseem\\PycharmProjects\\profile"


def login(credentials):
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(executable_path='C:\\chrome-driver\\chromedriver.exe', options=chrome_options)
    # driver = webdriver.Chrome()
    driver.get("https://www.pdfdrive.com/auth/login")
    username = driver.find_element_by_name("identity")
    password = driver.find_element_by_name("password")

    username.send_keys(credentials[0])
    password.send_keys(credentials[1])
    window_before = driver.window_handles[0]
    print(window_before)
    driver.find_element_by_xpath("//button[contains(.,'Sign in')]").click()
    return driver


def search(driver, tag, book_count=10):
    book = {}
    iterations = 1

    try:
        print('iter ', tag)

        # time.sleep(10)
        # Search for books
        driver.find_element_by_id("q").send_keys("{}".format(tag))
        time.sleep(2)
        auto_complete = driver.find_elements_by_xpath(
            "//div[starts-with(@class, 'autocomplete-suggestion')]")
        time.sleep(5)
        if not auto_complete:
            print('nothing found')
            return
        auto_complete[0].click()
        time.sleep(2)

        # Download books
        try:
            for index, element in enumerate(driver.find_elements_by_xpath('//*[contains(@id, "save-link")]')):

                print('Try No {}'.format(index))
                lst = os.listdir('C:\\Users\\ridah.naseem\\Downloads')
                # PDF drive will not allow more than 10 books download
                if index == book_count:
                    return book
                try:
                    print('Book element : ', element)
                    # get books id and title
                    book_id = element.get_attribute('data-id')

                    # book_size = driver.find_elements_by_xpath("//div[@class='file-info']/span[@class='fi-size']")
                    # print(book_size)

                    # clean the title
                    book_title = driver.find_element_by_id("preview-link-{}".format(book_id)).get_attribute(
                        'data-title')

                    # if book_title in book_list:
                    #     print('Ignoring books ({}) as already downloaded'.format(book_title))
                    #     continue

                    # save image download url and save as cover file
                    url = element.get_attribute('data-cover')
                    print('book url : ', url)
                    urllib.request.urlretrieve(url, '{}/cover/{}.jpg'.format(base_path, book_id))

                    # Save to drive
                    element.click()
                    time.sleep(5)

                    # download
                    driver.find_element_by_id("download-link-{}".format(book_id)).click()

                    # Get author

                    book[book_id] = (book_title.replace(',', ''), author_name(book_title))
                    print('book author : ', book_id, book[book_id])
                    time.sleep(30)

                    def get_new_file():
                        newlst = os.listdir('C:\\Users\\ridah.naseem\\Downloads')
                        file = set(newlst) - set(lst)
                        if file:
                            return list(file)[0]
                        return []

                    file = get_new_file()
                    print('Found new file that is downloaded', file)

                    if file:
                        filename = file
                        if filename:
                            while 'crdownload' in filename:
                                time.sleep(2)
                                print('File is being downloaded. Trying after 2 secs')
                                filename = get_new_file()

                            print('Book downloaded', filename)
                            shutil.move(os.path.join('C:\\Users\\ridah.naseem\\Downloads', filename),
                                        os.path.join('{}/books'.format(base_path), '{}.pdf'.format(book_id)))
                    else:
                        print("NO FILE DOWNLOADED ! ")

                except Exception as e:
                    print(e)
        except Exception as e:
            print('save linke cannot be found')
    except Exception as e:
        print("Cannot search", e)
    return book


def delete_books(driver):
    # driver = webdriver.Chrome()
    driver.get("https://www.pdfdrive.com/home/cloud")
    for element in driver.find_elements_by_xpath('//*[contains(@id, "save-link")]'):
        element.click()
        time.sleep(1)
    return driver


def read_csv(file_name):
    book_list = []
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row:
                if row[1] not in book_list:
                    book_list.append(row[1])
    return book_list


def move_books_to_local_folder(book):
    # move books from downloads to books
    lst = os.listdir('C:\\Users\\ridah.naseem\\Downloads')
    reference = dict()
    for index, x in enumerate(lst):

        if "crdownload" in x:
            time.sleep(60)

        if '.pdf' in x:
            new = x.strip().replace(' ( PDFDrive.com )', '').replace(' ', '_').replace(',', '').replace("'",
                                                                                                        "").replace(
                '.pdf', '')
            reference[new] = index

    print(reference)
    print(book)
    for k, value in book.items():
        v = value.strip().replace('( PDFDrive.com )', '').replace(' ', '_').replace(',', '').replace("'", "").replace(
            '.pdf', '')
        if v in reference.keys():
            file_path = os.path.join('{}/Downloads/{}'.format(home_path, lst[reference[v]]))
            print(file_path)
            if os.path.exists(file_path):
                shutil.move(file_path, os.path.join('{}/books'.format(base_path), '{}.pdf'.format(k)))

    with open('{}/test.csv'.format(base_path), 'a+', ) as f:
        for key in book.keys():
            f.write("%s,%s\n" % (key, book[key]))


def author_name(book_title):
    return p.author(book_title).replace(',', ';')


def write_to_csv(book_dict):
    with open('test.csv', 'a') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in book_dict.items():
            writer.writerow([key, value[0], value[1].replace('authors:', '')])


def upload(book_dict):
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(executable_path='C:\\chrome-driver\\chromedriver.exe', options=chrome_options)
    driver.get("http://elibrary.lgu.edu.pk/Home/Login")
    username = driver.find_element_by_name("Email")
    password = driver.find_element_by_name("Password")

    username.send_keys("drzarghunanaseem@lgu.edu.pk")
    password.send_keys("123")
    window_before = driver.window_handles[0]
    print(window_before)
    driver.find_element_by_xpath("//input[@value='Login']").click()
    time.sleep(5)
    #
    # window_after = driver.window_handles[1]
    # print(window_after)
    # driver.switch_to.window(window_after)
    # driver.implicitly_wait(10) # seconds
    # driver.get("http:// enter your URL.")
    # myDynamicElement = driver.find_element_by_id("myDynamicElement")
    driver.find_element_by_link_text("Create New Book").click()
    time.sleep(5)

    for id, title in book_dict.items():

        cover_image = os.getcwd() + "/cover/{}.jpg".format(id)
        file_path = os.getcwd() + "/books/{}.pdf".format(id)

        if not os.path.exists(cover_image) or not os.path.exists(file_path):
            print("Book or cover does not exist. {}, {}, {}".format(title, cover_image, file_path))
            continue

        # author = author_name(title)
        name = driver.find_element_by_id("Name").send_keys('{}'.format(title[0]))
        author = driver.find_element_by_id("Author").send_keys('{}'.format(title[1].replace('authors: ', '')))
        coverimage = driver.find_element_by_id("CoverImage").send_keys(cover_image)
        pdf = driver.find_element_by_id("PDF").send_keys(file_path)
        fid = driver.find_element_by_xpath("//select[@id='FacultyID']/option[text()='Social Sciences']").click()
        did = driver.find_element_by_xpath("//select[@id='DepartmentID']/option[text()='Psychology']").click()
        driver.find_element_by_id("Create").click()

        obj = driver.switch_to.alert

        # Retrieve the message on the Alert window
        msg = obj.text
        print(title[0])
        print("Alert shows following message: " + msg)

        time.sleep(2)

        # use the accept() method to accept the alert
        obj.accept()


def upload_from_file():
    driver = webdriver.Chrome(executable_path='C:\\chrome-driver\\chromedriver.exe')
    driver.get("http://elibrary.lgu.edu.pk/Home/Login")
    username = driver.find_element_by_name("Email")
    password = driver.find_element_by_name("Password")

    username.send_keys("drzarghunanaseem@lgu.edu.pk")
    password.send_keys("123")
    window_before = driver.window_handles[0]
    print(window_before)
    driver.find_element_by_xpath("//input[@value='Login']").click()
    time.sleep(10)
    driver.find_element_by_link_text("Create New Book").click()

    df = pd.read_csv('test.csv')
    for index, row in df.iterrows():
        title = row["title"]
        id = row["id"]
        author = row["author"]
        print(title, id, author)
        # for title, v in book_dict.items():
        name = driver.find_element_by_id("Name").send_keys('{}'.format(title))
        author = driver.find_element_by_id("Author").send_keys('{}'.format(author))
        coverimage = driver.find_element_by_id("CoverImage").send_keys(os.getcwd() + "/cover/new/{}.jpg".format(id))
        pdf = driver.find_element_by_id("PDF").send_keys(os.getcwd() + "/books/new/{}.pdf".format(id))
        fid = driver.find_element_by_xpath("//select[@id='FacultyID']/option[text()='Social Sciences']").click()
        did = driver.find_element_by_xpath("//select[@id='DepartmentID']/option[text()='Psychology']").click()
        driver.find_element_by_id("Create").click()

        obj = driver.switch_to.alert

        # Retrieve the message on the Alert window
        msg = obj.text
        print("Alert shows following message: " + msg)

        time.sleep(2)

        # use the accept() method to accept the alert
        obj.accept()


def upload_books():
    from csv import reader
    book_dictionary = {}
    with open('test.csv', 'r') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = reader(read_obj)
        # Iterate over each row in the csv using reader object
        for row in csv_reader:
            # print(row)
            if row and row[0] is not 'id':
                # row variable is a list that represents a row in csv
                id, title, author = row[0], row[1], row[2]
                book_dictionary[id] = (title, author)
        # give some time to upload
    upload(book_dictionary)


def download_books():
    topic_list = [

        "positive psychology",
        "self esteem",
        "organizational behavior",
        "motivation psychology",
        "educational psychology",
        "learning psychology"
        'assertiveness',
        'resilience',
        'flow',
        'violence',
        'coping',
        'violence',
        'forgiveness',
        'altruism',

        'Human resource psychology',
        'Employee satisfaction',
        'Motivation',
        'Artificial intelligence psychology',
        'Machine learning and psychology',
        'Pedagogy',
        'Endragogy psychology',
        'Learning psychology',
        'Memory psychology',
        'Cognitive psychology',
        'Logic psychology',
        'Problem solving psychology',
        'Sport psychology',
        'Environmental psychology',
        'Individual differences in psychology',
        'Correlation psychology',
        'Political psychology',

        'Propoganda  psychology'
        'Brain washing',
        'Emotional intelligence',
        'Fluid IQ',
        'Inferiority complex',
        'Superiority complex',
        'Self image ',
        'Self identity ',
        'Self efficacy ',
        'Self worth ',
        'dark psycholog',
        'psycholog',
        'psychological effects of bullyin',
        'psychological effects of abortio',
        'psychological effects of divorc',
        'psychological effects of stres',
        'psychological effects of social',
        'psychological effects of wa',
        'psychological effects of music',

        'psychology of learning'
        'reasoning proce',
        'reasoning cycl',
        'reasoning approac',
        'imagination and creativit',
        'imagination cognition and pers',
        'psychology of religio',
        'religion psyc',
        'psychology patien',
        'crisis',
        'statistical',
        'mind '
        'psychological'
        'psychological differences in '
    ]
    for user in [("<email>", "<give password>"), ]:

        # for a in range(1, 3):
        driver = login(user)

        for topic in topic_list:
            delete_books(driver)
            book_dict = search(driver, tag='{}'.format(topic), book_count=30)
            driver.refresh()
            write_to_csv(book_dict)
            # move_books_to_local_folder(book_dict)
            time.sleep(10)


if __name__ == '__main__':
    download_books()
    # upload_books()
