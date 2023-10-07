import json
from xml.etree import ElementTree


class PersonAgeException(Exception):
    def __init__(self, message):
        super().__init__(message)


class Person:
    def __init__(self, name: str, age: int):
        if age <= 100:
            self.__age = age
        else:
            raise PersonAgeException("Student's age must be less than 100")

        self.__name = name

    def set_name(self, name):
        self.__name = name

    def set_age(self, age):
        if age <= 100:
            self.__age = age
        else:
            raise PersonAgeException("Student's age must be less than 100")

    def get_name(self):
        return self.__name

    def get_age(self):
        return self.__age

    def sleeping(self):
        print(self.__name + " sleeping...")


class Student(Person):
    def __init__(self, hobby: str, name, age, grade: str):
        Person.__init__(self, name, age)
        self.hobby = hobby
        self.grade = grade

    def to_dict(self):
        student_dict = {
            "name": self.get_name(),
            "age": self.get_age(),
            "hobby": self.hobby,
            "grade": self.grade
        }
        return student_dict

    def doing_homework(self):
        print(self.get_name() + " Doing homework...")

    def to_xml(self):
        student_element = ElementTree.Element("Student")

        name_element = ElementTree.Element("Name")
        name_element.text = self.get_name()
        student_element.append(name_element)

        age_element = ElementTree.Element("Age")
        age_element.text = str(self.get_age())
        student_element.append(age_element)

        hobby_element = ElementTree.Element("Hobby")
        hobby_element.text = self.hobby
        student_element.append(hobby_element)

        grade_element = ElementTree.Element("Grade")
        grade_element.text = self.grade
        student_element.append(grade_element)

        xml_tree = ElementTree.ElementTree(student_element)

        return ElementTree.tostring(xml_tree.getroot(), encoding="utf-8", method="xml", xml_declaration=True)


class Professor(Person):
    def __init__(self, salary: int, name, age, degree: str):
        Person.__init__(self, name, age)
        self.salary = salary
        self.degree = degree

    def giving_a_lecture(self):
        print(self.get_name() + " The professor is giving a lecture...")


class TooManyStudentsEnrolledException(Exception):
    def __init__(self, message):
        super().__init__(message)


class MathCourse:
    def __init__(self, course_code: int, course_name: str):
        self.course_code = course_code
        self.course_name = course_name
        self.professor = Professor(salary=500000, name="Ludmila", age=55, degree="PhD in Mathematics")  # Композиция
        self.students = []  # Агрегация

    def enroll_student(self, student):
        if len(self.students) <= 100:
            self.students.append(student)
        else:
            raise TooManyStudentsEnrolledException('No more than 100 people can enroll in a math course!')

    def to_dict(self):
        course_dict = {
            "course_code": self.course_code,
            "course_name": self.course_name,
            "professor": {
                "salary": self.professor.salary,
                "name": self.professor.get_name(),
                "age": self.professor.get_age(),
                "degree": self.professor.degree,
            },
            "students": [student.to_dict() for student in self.students]
        }
        return course_dict

    @classmethod
    def from_json(cls, json_data):

        course_dict = json.loads(json_data)
        course_code = course_dict["course_code"]
        course_name = course_dict["course_name"]

        math_course_json = cls(course_code, course_name)

        professor_data = course_dict.get("professor", None)
        if professor_data:
            professor = Professor(
                salary=professor_data["salary"],
                name=professor_data["name"],
                age=professor_data["age"],
                degree=professor_data["degree"]
            )
            math_course_json.professor = professor

        students_data = course_dict.get("students", [])
        for student_data in students_data:
            student = Student(
                name=student_data["name"],
                age=student_data["age"],
                hobby=student_data["hobby"],
                grade=student_data["grade"]
            )
            math_course_json.enroll_student(student)

        return math_course_json

    def to_xml(self):

        math_course_element = ElementTree.Element("MathCourse")

        math_course_element.set("course_code", str(self.course_code))
        math_course_element.set("course_name", self.course_name)

        if self.professor:
            professor_element = ElementTree.Element("Professor")
            professor_element.set("salary", str(self.professor.salary))
            professor_element.set("name", self.professor.get_name())
            professor_element.set("age", str(self.professor.get_age()))
            professor_element.set("degree", self.professor.degree)
            math_course_element.append(professor_element)

        if self.students:
            students_element = ElementTree.Element("Students")
            for student in self.students:
                student_element = ElementTree.Element("Student")
                student_element.set("name", student.get_name())
                student_element.set("age", str(student.get_age()))
                student_element.set("hobby", student.hobby)
                student_element.set("grade", student.grade)
                students_element.append(student_element)
            math_course_element.append(students_element)

        xml_tree = ElementTree.ElementTree(math_course_element)

        return ElementTree.tostring(xml_tree.getroot(), encoding="utf-8", method="xml")

    @classmethod
    def from_xml(cls, xml_data):

        xml_tree = ElementTree.ElementTree(ElementTree.fromstring(xml_data))
        math_course_element = xml_tree.getroot()

        course_code = int(math_course_element.get("course_code"))
        course_name = math_course_element.get("course_name")

        math_course_xml = cls(course_code, course_name)

        professor_element = math_course_element.find("Professor")
        if professor_element is not None:
            salary = int(professor_element.get("salary"))
            name = professor_element.get("name")
            age = int(professor_element.get("age"))
            degree = professor_element.get("degree")
            math_course_xml.professor = Professor(salary, name, age, degree)

        students_element = math_course_element.find("Students")
        if students_element is not None:
            for student_element in students_element.findall("Student"):
                name = student_element.get("name")
                age = int(student_element.get("age"))
                hobby = student_element.get("hobby")
                grade = student_element.get("grade")
                student = Student(hobby, name, age, grade)
                math_course_xml.students.append(student)

        return math_course_xml


# 1) Заполняю данными объекты и проверяю, что ничего не сломается

student1 = Student(hobby="football", name="Alice", age=20, grade="A")
student2 = Student(hobby="violin", name="Bob", age=22, grade="B")

math_course = MathCourse(course_code=101, course_name="Mathematics")

math_course.enroll_student(student1)
math_course.enroll_student(student2)

student1.sleeping()
student2.doing_homework()
math_course.professor.giving_a_lecture()

print(f"{student1.get_name()} is {student1.get_age()} years old and has a grade of {student1.grade}.")
print(f"{student2.get_name()} is {student2.get_age()} years old and has a grade of {student2.grade}.")
print(f"The professor for the {math_course.course_name} course is {math_course.professor.get_name()}.")

# 2) Обрабатываю собственное исключение. Если попытаться записать больше 100 студентов на курс по математике,
#    то бросится исключение


for i in range(0, 999):
    try:
        math_course.enroll_student(Student(hobby="dummy", name="dummy",
                                           age=0, grade="A"))
    except TooManyStudentsEnrolledException:
        print("Custom exception handled")
        break

# 3) Обрабатываю дефолтное исключение

try:
    print(math_course.students[101])
except IndexError:
    print("IndexError handled")

# 4) Сначала сериализую объект в json и записываю в файл
#    Потом десереализую в объект из файла

course_json = math_course.to_dict()

with open('math_course_to_json.json', 'w') as json_file:
    json.dump(course_json, json_file, indent=4)

try:
    with open('math_course_from_json.json', 'r') as json_file:
        json_data = json_file.read()
        math_course_from_json = MathCourse.from_json(json_data)
except FileNotFoundError:
    print("File 'math_course_from_json.json' not found")

# 5) Сначала сериализую объект в xml и записываю в файл
#    Потом десереализую в объект из файла

course_xml = math_course.to_xml()

with open('math_course_to_xml.xml', 'wb') as xml_file:
    xml_file.write(course_xml)

try:
    with open('math_course_from_xml.xml', 'r') as xml_file:
        xml_data = xml_file.read()
        math_course_from_xml = MathCourse.from_xml(xml_data)
except FileNotFoundError:
    print("File 'math_course_from_xml.xml' not found")


# 6) Дальше идёт код для взаимодействия с программой из консоли
#    Пользователь может ввести имя, возраст, хобби, оценку студента, имя файла и формат(xml или json)
#    После ввода он может сделать это ещё раз, пока не откажется продолжать
#    После выхода из цикла программа завершится и создадутся нужные файлы
class InvalidFileFormat(Exception):
    def __init__(self, message):
        super().__init__(message)


is_input = True
while is_input:
    try:
        student_name = input("\nEnter student's name: ")
        student_age = int(input("Enter student's age: "))
        student_hobby = input("Enter student's hobby: ")
        student_grade = input("Enter student's garde: ")
        new_student = Student(student_hobby, student_name, student_age, student_grade)

        file_name = input("Enter file name: ")
        file_format = input("Enter file format(xml or json): ")

        if file_format == "json":
            student_json = new_student.to_dict()

            with open(file_name + ".json", 'w') as json_file:
                json.dump(student_json, json_file, indent=4)
        elif file_format == "xml":
            student_xml = new_student.to_xml()

            with open(file_name + ".xml", 'wb') as xml_file:
                xml_file.write(student_xml)
        else:
            raise InvalidFileFormat("Invalid file format. Please enter 'xml' or 'json'")

        continue_input = input("Do you want to enter another student? (yes/no): ")
        if continue_input.lower() != "yes":
            is_input = False

    except PersonAgeException:
        print("Student's age must be less than 100!\n")
    except ValueError:
        print("Invalid input, try again\n")
    except InvalidFileFormat as e:
        print("Invalid file format. Please enter 'xml' or 'json'\n")
