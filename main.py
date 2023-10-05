import json
import random
from random import randrange
from xml.etree import ElementTree
import names

class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def sleeping(self):
        print(self.name + " sleeping...")


class Student(Person):
    def __init__(self, hobby: str, name, age, grade: str):
        Person.__init__(self, name, age)
        self.hobby = hobby
        self.grade = grade

    def to_dict(self):
        student_dict = {
            "name": self.name,
            "age": self.age,
            "hobby": self.hobby,
            "grade": self.grade
        }
        return student_dict

    def doing_homework(self):
        print(self.name + " Doing homework...")


class Professor(Person):
    def __init__(self, salary: int, name, age, degree: str):
        Person.__init__(self, name, age)
        self.salary = salary
        self.degree = degree

    def giving_a_lecture(self):
        print(self.name + " The professor is giving a lecture...")


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
                "name": self.professor.name,
                "age": self.professor.age,
                "degree": self.professor.degree,
            },
            "students": [student.to_dict() for student in self.students]
        }
        return course_dict

    @classmethod
    def from_json(cls, json_data):
        # Преобразование JSON данных в объект MathCourse
        course_dict = json.loads(json_data)
        course_code = course_dict["course_code"]
        course_name = course_dict["course_name"]

        # Создание объекта MathCourse
        math_course = cls(course_code, course_name)

        # Если в JSON данных также содержится информация о профессоре,
        # создаем объект Professor и присваиваем его атрибуту professor
        professor_data = course_dict.get("professor", None)
        if professor_data:
            professor = Professor(
                salary=professor_data["salary"],
                name=professor_data["name"],
                age=professor_data["age"],
                degree=professor_data["degree"]
            )
            math_course.professor = professor

        # Если в JSON данных также содержится информация о студентах,
        # создаем объекты Student и добавляем их к атрибуту students
        students_data = course_dict.get("students", [])
        for student_data in students_data:
            student = Student(
                name=student_data["name"],
                age=student_data["age"],
                hobby=student_data["hobby"],
                grade=student_data["grade"]
            )
            math_course.enroll_student(student)

        return math_course

    def to_xml(self):
        # Создаем корневой элемент <MathCourse>
        math_course_element = ElementTree.Element("MathCourse")

        # Добавляем атрибуты course_code и course_name
        math_course_element.set("course_code", str(self.course_code))
        math_course_element.set("course_name", self.course_name)

        # Если есть информация о профессоре, создаем элемент <Professor>
        if self.professor:
            professor_element = ElementTree.Element("Professor")
            professor_element.set("salary", str(self.professor.salary))
            professor_element.set("name", self.professor.name)
            professor_element.set("age", str(self.professor.age))
            professor_element.set("degree", self.professor.degree)
            math_course_element.append(professor_element)

        # Если есть информация о студентах, создаем элемент <Students>
        if self.students:
            students_element = ElementTree.Element("Students")
            for student in self.students:
                student_element = ElementTree.Element("Student")
                student_element.set("name", student.name)
                student_element.set("age", str(student.age))
                student_element.set("hobby", student.hobby)
                student_element.set("grade", student.grade)
                students_element.append(student_element)
            math_course_element.append(students_element)

        # Создаем XML-дерево
        xml_tree = ElementTree.ElementTree(math_course_element)

        # Возвращаем XML в виде строки
        return ElementTree.tostring(xml_tree.getroot(), encoding="utf-8", method="xml")

    @classmethod
    def from_xml(cls, xml_data):
        # Разбор XML данных
        xml_tree = ElementTree.ElementTree(ElementTree.fromstring(xml_data))
        math_course_element = xml_tree.getroot()

        # Извлечение атрибутов course_code и course_name
        course_code = int(math_course_element.get("course_code"))
        course_name = math_course_element.get("course_name")

        # Создание объекта MathCourse
        math_course = cls(course_code, course_name)

        # Извлечение информации о профессоре, если она есть
        professor_element = math_course_element.find("Professor")
        if professor_element is not None:
            salary = int(professor_element.get("salary"))
            name = professor_element.get("name")
            age = int(professor_element.get("age"))
            degree = professor_element.get("degree")
            math_course.professor = Professor(salary, name, age, degree)

        # Извлечение информации о студентах, если она есть
        students_element = math_course_element.find("Students")
        if students_element is not None:
            for student_element in students_element.findall("Student"):
                name = student_element.get("name")
                age = int(student_element.get("age"))
                hobby = student_element.get("hobby")
                grade = student_element.get("grade")
                student = Student(hobby, name, age, grade)
                math_course.students.append(student)

        return math_course


student1 = Student(hobby="football", name="Alice", age=20, grade="A")
student2 = Student(hobby="violin", name="Bob", age=22, grade="B")

math_course = MathCourse(course_code=101, course_name="Mathematics")

math_course.enroll_student(student1)
math_course.enroll_student(student2)

student1.sleeping()
student2.doing_homework()
math_course.professor.giving_a_lecture()

print(f"{student1.name} is {student1.age} years old and has a grade of {student1.grade}.")
print(f"{student2.name} is {student2.age} years old and has a grade of {student2.grade}.")
print(f"The professor for the {math_course.course_name} course is {math_course.professor.name}.")

hobby_list = ["Education", "Fashion", "Fitness", "Music", "Nature", "Playing"]

for i in range(0, 999):
    try:
        math_course.enroll_student(Student(hobby=hobby_list[randrange(len(hobby_list))], name=names.get_first_name(), age=random.randint(18, 27), grade=chr(random.randint(ord('A'), ord('Z')))))
    except TooManyStudentsEnrolledException:
        print("Custom exception handled")
        break

try:
    print(math_course.students[101])
except IndexError:
    print("IndexError handled")

course_data = math_course.to_dict()

with open('math_course_to_json.json', 'w') as json_file:
    json.dump(course_data, json_file, indent=4)

with open('math_course_from_json.json', 'r') as json_file:
    json_data = json_file.read()

math_course_from_json = MathCourse.from_json(json_data)


xml_data = math_course.to_xml()

with open('math_course_to_xml.xml', 'wb') as xml_file:
    xml_file.write(xml_data)

with open('math_course_from_xml.xml', 'r') as xml_file:
    xml_data = xml_file.read()

math_course_from_xml = MathCourse.from_xml(xml_data)
