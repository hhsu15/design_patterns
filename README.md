# Design Pattern

# SOLID Principles
## Single Responsibility Principle (SRP or SOP)
Essentially one class should only have a singble resposibility.
For example:
```python

class Journal:

	def __init__(self):
		self.entries = []

	def add_journal(self, txt):
		self.entries.append(txt)

	def delete_journal(self, pos):
		delete self.entries[pos]

# ----so far ok, but once we add more things like
    def save(self, filename):
		pass
	
	def load(self, filename)
		pass

# it breaks the principle :(
# ---instead we should have another class for this, for example

class PersistentManager:
	@staticmethold
	def save_to_file(journal, file):
		with open(file, 'w') as f:
			f.write(str(journal))
```

## Open Close Principle (OCP)
Basically we should not jump in and modify and existing code that has been working. We should, though, be able to extend it. This will mean inheritance. 
- We can enforce this principle by using an Enterprise design pattern called `Specification`
```python
class Specification:
	def is_satisfied(self, item):
		pass

	def __and__(self, other):
		"""so we can use and operator as syntatic sugur
		So basically if we do:
		large_blue = SizeSpecification(Size.Large) and ColorSpecification(Color.GREEN)
		this will return AndSpecifcation which you can just use for the filter
		"""
		return AndSpecification(self, other)

class Filter:
	def filter(self, items, spec):
		pass

class ColorSpecification(Specification):
	def __init__(self, color):
		self.color = color

	def is_satissfied(self, item):
		return item.color == self.color

class SizeSpecification(Specification):
	def __init__(self, size):
		self.size = size

	def is_satissfied(self, item):
		return item.size == self.size

# combinator
class AndSpecification(Specification):
	def __init__(self, spec1, spec2):
		self.spec1 = spec1
		self.spec2 = spec2
	
	def is_satisfied(self, item):
		return self.spec1.is_satisfied(item) and \
		       self.spec2.is_satisfied(item)


class BetterFilter(Filter):
	def filter(self, items, spec):
		for item in items:
			if spec.is_satisfied(item):
				yield item

apple = Product("Apple", Color.GREEN, Size.SMALL)
tree = Product("Tree", Color.GREEN, Size.BIG)
orange = Product("Orange", Color.ORANGE, Size.SMALL)

products = [apple, tree, orange]
green = ColorSpecification(Color.GREEN)
bf = Betterfilter()
for p in bf.filter(products, green):
	print(f'{p} is green')

large_blue = SizeSpecification(Size.LARGE) and ColorSpecification(Color.GREEN)
for p in bf.filter(large_blue):
	print(f'{p} is green and large')



```

## Liskov Substitution Principle (LSP)
If you take inheritance from the base class you should be able to stick to it and everything should still work correctly.
- The example of breaking this principle could be you inherit a base class of Rectangle for a subclass of Square (which assumes same height and width, if you set the height -> it should also change the width -> if we have a function that caches the width to get expected vaule and then allow you to set height it will no longer work properly due to this side effect. 

## Interface Segregation Principle (ISP)
The idea is you do not want to stick too many methods into an interface. So instead of having a base class that does many things that might not be applicable to the subclass, we should create more granular classes for each purpose. 
- For example 
```python
# instead of having a base class defining the interface like this
class Machine:
	
	@abstractmethod
	def scan(self):
		pass
	
	@abstractmethod
	def print(self):
		pass

# consider using these
class Printer:
	
	@abstractmethod
	def print(self):
		pass

class Scanner:
	@abstractmethod
	def scan(self):
		pass

class MultiFunctionDevice(Printer, Scanner):
	
	@abstractmethod
	def print(self):
		pass
    
	@abstractmethod
	def scan(self):
		pass

class CannonMultiPrinter(MultiFunctionDevice):
	
	def print(self):
		do something

	def scan(self):
		do something
```

## Dependency Inversion Principle
High level module should not depend on low level module. It should depend on abstract interface rather than implementation
- high level module - uses some other functions closer to the hardware. Say, something like InspectRelationship
- low level module - for example module dealing with storage, say you a class called Relationships that stores the relations as a list
- You should not have InspectRelationship depend on Relationships because if Relasionships changes the way the data is stored then InspectRelationship will break.

Example
```python
# instead of having something like this:
class Relationships: # low level module
	def __init__(self):
		self.relations = []  # if this changes we have to rewrite the code for InspectRelaship

	...

class InspectRelationship: # high level module
	def __init__(self, rel, name):
		for r rel.relations: # We are depending on the low level module!! Remenber, this should not depend on concret implementation but should depend on abstractions
			...


# This is better version to fix above issue
class RelationshipBrowser:
	@abstractmethod
	def find_relasionship(self, name):
		pass

class Relationships(RelationshipBrowser):
    def find_relationship(self, name):
		"""your concret implementation here"""
	    ...

class InspectRelationship: # so now this is only depending on an abstraction
	def __init__(self, rel_browser, name):
		rel_browser.find_relationship(name)
```

# Gamma Categorization
Design Patterns are typically split into three categories
- Creational Patterns (Builder Patterns)
  - think about contruction of objects
- Structure Patterns
  - concerned with the structures (e.g., class members)
  - stress the importance of good API design
- Behavioral Patterns
  - they are all different

## Builder Desgin Pattern
Eseentially to solve the problem if you have a complex constructor
Example, you want to construct an HTML paragraph. Rather than just join all the strings with tags, let's outsource to a beautiful builder that can build complicated html.
Example:
```python
class HtmlElement:
    indent_size = 2
    
    def __init__(self, name='', text=''):
        self.text = text
        self.name = name
        self.elements = []
    
    def __str(self, indent):
        """implementation of formatting the html element"""
        lines = []
        i = ' ' * (indent * self.indent_size)
        lines.append(f'{i}<{self.name}>')
        
        if self.text:
            i1 = ' ' * ((indent + 1) * self.indent_size)
            lines.append(f'{i1}{self.text}')
    
        for e in self.elements:
            # this is recursion part, append each string representation of an element
            lines.append(e.__str(indent + 1))
        
        lines.append(f'{i}</{self.name}>')
        return '\n'.join(lines)
    
    def __str__(self):
        """for the print function"""
        return self.__str(0)
    
    @staticmethod
    def build(name):
        """Provide another way to start the builder"""
        return HtmlBuilder(name)
    
class HtmlBuilder:
    """This is how you can construct a builder"""
    def __init__(self, root_name):
        self.root_name = root_name
        self.__root = HtmlElement(root_name)
        
    def add_child(self, child_name, child_text):
        self.__root.elements.append(
        HtmlElement(child_name, child_text)
        )
        
    def add_child_fluent(self, child_name, child_text):
        """This is very neat! 
        By returning self, you allow chainning these things
        """
        self.__root.elements.append(
        HtmlElement(child_name, child_text)
        )
        return self
        
    
    def __str__(self):
        """This is the cool part!
        when you print the builder obj, it calling the string representation 
        of HtmlElement
        """
        return str(self.__root)
    
# builder = HtmlBuilder('ul') # samething
builder = HtmlElement.build('ul')
builder.add_child_fluent('li', 'Kyle').add_child_fluent('li', 'Kyly')
 """  
  <ul>
    <li>
      Kyle
    </li>
    <li>
      Kyly
    </li>
  </ul>

 """
```

### Builder Facets
You can use a base builder class and jump between sub-builder classes using certain tricks. Essentially by 
  - passing the object around using fluent interface
  - use @property to create sub-class object
Example: 
```python
class Person:
    def __init__(self):
        self.street_address = None
        self.postcode = None
        self.city = None
        
        self.company_name = None
        self.position = None
        self.annual_income = None
        
    def __str__(self):
        return f'Address {self.street_address}, {self.postcode}, {self.city}' + \
               f'Employed at {self.company_name} as a {self.position} earning {self.annual_income}'

class PersonBuilder:
    """Show off a pretty cool trick here
    We have the PersonBilder as base class which allows to you switch the subbuilders
    
    """
    def __init__(self, person=Person()): # a little trick here to create a Person but also allow a already built person
        self.person = person
        
    @property
    def works(self):
        """by calling this property you create a JobBuilder
        the trick here is you pass the 'self.person'
        when it goes JobBuilder it comes back to PersonBuilder
        This allows to you use the base class to toggle the subclasses 
        """
        return PersonJobBuilder(self.person)
    
    @property
    def lives(self):
        """by calling this property you create a JobBuilder
        the trick here is you pass the 'self.person'
        when it goes JobBuilder it comes back to PersonBuilder
        This allows to you use the base class to toggle the subclasses 
        """
        return PersonAddressBuilder(self.person)
        
    def build(self):
        return self.person # so you return
    

class PersonJobBuilder(PersonBuilder):
    def __inti__(self, person):
        super().__init__(person)
        
    def at(self, company_name):
        self.person.company_name = company_name
        return self  # make it fluent interface
    
    def as_a(self, position):
        self.person.position = position
        return self
    
    def earning(self, annual_income):
        self.person.annual_income = annual_income
        return self
    
class PersonAddressBuilder(PersonBuilder):
    def __inti__(self, person):
        super().__init__(person)
        
    def at(self, street_address):
        self.person.street_address = street_address
        return self  # make it fluent interface
    
    def with_postcode(self, postcode):
        self.person.postcode = postcode
        return self
    
    def in_city(self, city):
        self.person.city = city
        return self
    
pb = PersonBuilder()
person = pb\
    .lives\
        .at("1123 street")\
        .in_city("Tokyo")\
    .works\
        .at("Bloomberg")\
        .as_a("Data Engineer")\
        .earning(100000)\
    .build()
print(person)  # Address 1123 street, None, TokyoEmployed at Bloomberg as a Data Engineer earning 100000  

```
- By the way, if we do not want to violate the Open Close Principle (Open to extension, close to modification) - since we have to modify the base PersonBuilder everytime we make a new class - there is an alternative, like so:
```python
# An alternative way using inheritance so you do not violate Open Close Priciple

class Person:
    def __init__(self):
        self.street_address = None
        self.postcode = None
        self.city = None
        
        self.company_name = None
        self.position = None
        self.annual_income = None
        
    @staticmethod
    def new():
        return PersonBuilder()
        
    def __str__(self):
        return f'Address {self.street_address}, {self.postcode}, {self.city}' + \
               f'Employed at {self.company_name} as a {self.position} earning {self.annual_income}'

class PersonBuilder:
    
    def __init__(self): # a little trick here to create a Person but also allow a already built person
        self.person = Person()
        
    
    def build(self):
        return self.person

    
class PersonAddressBuilder(PersonBuilder):
    def at(self, street_address):
        self.person.street_address = street_address
        return self  # make it fluent interface
    
    def with_postcode(self, postcode):
        self.person.postcode = postcode
        return self
    
    def in_city(self, city):
        self.person.city = city
        return self
    
class PersonJobBuilder(PersonAddressBuilder):
    def at_company(self, company_name):
        self.person.company_name = company_name
        return self  # make it fluent interface
    
    def as_a(self, position):
        self.person.position = position
        return self
    
    def earning(self, annual_income):
        self.person.annual_income = annual_income
        return self
    
# and you can go on and on....

pb = PersonJobBuilder()
me = pb\
    .at("New Jersey")\
    .with_postcode("0000")\
    .in_city("Princeton")\
    .at_company("BBG")\
    .as_a("Engineer")\
    .earning(10000000)\
    .build() 
    
print(me)    #Address New Jersey, 0000, PrincetonEmployed at BBG as a Engineer earning 10000000

```

## Factories
A component responsible solely for the wholesale(not piecewise) creation of objects

### Factory Methods
Methods (typically staticmethods) that create objects
Example:
```python
from math import *
from enum import Enum

class CoordinateSystem(Enum):
    CARTESIAN = 1
    POLAR = 2
    
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __str__(self):
        return f'x: {self.x}, y: {self.y}'
        
    # instead of using this...
#     def __init__(self, a, b, system=CordinateSystem.CARTESIAN):
#         if system = CordinateSystem.CARTESIAN:
#             self.x = a
#             self.y = b
#         elif system == CoordinateSystem.POLAR:
#             self.x = a * cos(b)
#             self.y = a * sin(b)
    
    @staticmethod
    def new_cartesian_point(x, y):
        """Factory method"""
        return Point(x, y)
        
    @staticmethod
    def new_polar_point(rho, theta):
        """Factory method"""
        return Point(rho * cos(theta), rho * sin(theta))

p = Point.new_cartesian_point(2, 3)
p2 = Point.new_polar_point(2, 3)
print(p)
print(p2)

```
### Factory
Factory is simply a separate class that manages all the factory methods.
At the core, it's a class that allows to manufacture objects.
- so in above example, it can be done as
```python
class PointFactory:
	
	@staticmethod
	def new_cartesian_point(x, y):
		pass

	@staticmethod
	def new_poloar_point(rho, theta):
		pass

```
### Abstract Factory
Make the factory class abstract class to build the hierarchy of the sub factory class
```python
class HotDrinkFactory(AB):
	def prepare(self, amt):
	pass

class TeaFactory(HotDrinkFactory):
	def prepare(self, amt):
		...
		return Tea()

class CoffeeFactory(HotDrinkFactory):
	def prepare(self, amt):
		...
		return Coffee()


```

## Prototype
A partially or fully initialized object that you copy and make use of.
Prototype reiterate existing design. Essentially we take advantage of some existing design and build/customize it.
```python
# key here is copying the object. In order to custom the object you copy properly, use deepcopy. Something like
john = Persob('John', Address('tokyo', 'Japan')
jane = copy.deepcopy(john)
jane.name = 'Jane'
jane.address.city = 'osaka'
# rather than creating a jane Person object from scrach you can use Proptotype 
# notice if you use copy.copy (shallow copy) you will have have the name attribute as Jane but the Address will still be reference so you will have it both for john and jane which won't be what you want.
```
### Use Factory for Prototype
A nice way to make prototype easier is to use Factory. Example
```python
# use factory for prototype
import copy

class Employee:
    def __init__(self, name, address):
        self.name = name
        self.address = address
    
    def __str__(self):
        return f'{self.name} works at {self.address}'
    
class Address:
    def __init__(self, street, city):
        self.street = street
        self.city = city
        
    def __str__(self):
        return f'{self.street}, {self.city}'
    
    
class EmployeeFactory:
    main_office_employee = Employee('', Address('main street','Princeton'))
    ny_office_employee = Employee('', Address('manhatan', 'NY'))
    
    @staticmethod
    def new_main_office_employee(name):
        new_main_emp = copy.deepcopy(EmployeeFactory.main_office_employee)
        new_main_emp.name = name
        return new_main_emp
    
    @staticmethod
    def new_ny_office_employee(name):
        new_ny_emp = copy.deepcopy(EmployeeFactory.ny_office_employee)
        new_ny_emp.name = name 
        return new_ny_emp
    
kyle = EmployeeFactory.new_main_office_employee("Kyle")
jess = EmployeeFactory.new_ny_office_employee("Jess")

```
