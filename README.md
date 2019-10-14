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

## Singleton
For some components it only makes sense to have on ein the system such as dataybase repositoy or object factory. 
```python

class Database:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Database, cls).__new__(cls,*args, **kwargs)
        return cls._instance
```
### Singleton decorator
```python
# However this does not prevent __init__ gets called multiple times, which is half baked,
# a better approach would be using a decorator

def singleton(class_):
    _instances = {}

    def wrapper(*args, **kwargs):
        if class_ not in _instances:
            _instances[class_] = class_(*args, **kwargs)
        return _instances[class_]
    return wrapper

@singleton
class Database:

    def __init__(self):
        print("Loading database")

```

### Singleton metaclass
```python
class Singleton(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls)\
                .__call__(*args, **kwargs)
        return cls._instances[cls]
    
class Database(metaclass=Singleton):
    def __init__(self):
        print("Loading database")
        
d1 = Database()
d2 = Database 

d1 is d2 # => True

```

### Monostate
A variation of Singleton. You have a static state but you allow them to be overriden. The trick is you always referece the same object
```python
class CEO:
    # create a static variable for the attributes
    _shared_state = {
        'name': 'John',
        'age': 55        
    }
    
    def __init__(self):
        self.__dict__ = CEO._shared_state  # you are always refencing the same set of attributes
        
    def __str__(self):
        return f'{self.name}, {self.age}'
    
c1 = CEO()
print(c1)
c2 = CEO()
c2.name = 'Hsin'
c2.age = 39
print(c2)
print(c1)

```

## Adapter
Getting the interface you want from the interface you have - the inbetween component. 
Example:
```python 
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
def draw_point(p):
    print('.', end='')

# you are given above API

# You want to use below
class Line:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        
class Rectangle(list):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.append(Line(Point(x, y), Point(x + width, y)))
        self.append(Line(Point(x + width, y), Point(x + width, y + height)))
        self.append(Line(Point(x, y), Point(x, y + height)))
        self.append(Line(Point(x, y + height), Point(x + width, y + height)))

        
# here is the adapter which is an "in-btween component"
class LineToPointAdapter:
    cache = {}  # so we do not have to create a new object every time
    
    def __init__(self, line):
        self.h = hash(line)  # use this as unique key
        if self.h in self.cache:
            return
        
        super().__init__()
        
        print(f'Generating points for line'
              f'[{line.start.x}, {line.end.y}] ->'
              f'[{line.end.x}, {line.end.y}]'
             )
        
        left = min(line.start.x, line.end.x)
        right = max(line.start.x, line.end.x)
        top = min(line.start.y, line.end.y)
        bottom = min(line.start.y, line.end.y)
        
        points = []
        
        if right - left == 0:
            for y in range(top, bottom):
                points.append(Point(left, y))
        elif line.end.y - line.start.y == 0:
            for x in range(left, right):
                points.append(Point(x, top))
                
        self.cache[self.h] = points
        
    def __iter__(self):  # so you can interate the obj like a list
        return iter(self.cache[self.h])
        
        
        
def draw(rcs):
    print("\n\n--drawing some stuff---\n")
    for rc in rcs:
        for line in rc:
            adapter = LineToPointAdapter(line)
            for p in adapter:
                draw_point(p)
                
if __name__ == '__main__':
    rcs = [Rectangle(1, 1, 10, 10),
         Rectangle(3, 3, 6, 6)]
    
    draw(rcs)
    
    draw(rcs) # notice send time it won't generate those points 
              #becasue they have been created and stored in cache

```

## Bridge
Bridge pattern prevents a "Cartesian product" complexity explosion. For example, if you would normally create a combinations of hierarchy scenerios where it ends up being 2*2, 4*4 due to the number of senerios

Example:
```python
# circle square
# vector raster

from abc import ABC

class Renderer(ABC):
	def render_circle(self, radius):
		pass
	# render_square

class VectorRender(Renderer):
	def render_circle(self, radius):
		print(f'drawing a circle of radius {radius}')

class RasterRenderer(Renderer):
	def render_circle(self, radius):
		def render_circle(self, radius):
			print(f"Drawing pixels for a circle of radius {radius}')

class Shape:  # this the Bridge pattern, which connects two hierachy with different classes with a parameter (in this case renderer)and you have the connection between each other  
	def __init__(self, renderer):
		self.renderer = renderer

	def draw(self): pass

	def resize(self): pass

class Circle(Shape):
	def __init__(self, renderer, radius):
		super().__init__(renderer)
		self.radius = radius

	def draw(self):
		self.renderer.render_circle(self.radius)

	def resize(self, factor):
		self.radius *= factor

raster = RasterRenderer()
vector = VectorRenderer()
circle = Circle(vector, 5)
circle.draw()
circle.resize(2)
circle.draw()
```

## Composite
Composition lets us make compound objects. E.g., A Person object composes Address object and Job object. Or an object that is a group of other objects. Composite pattern is a mechanisim for treating individual objects and compositions of objects in an uniform manner

Example:
```python
class GraphicObject:
	def __init__(self, color=None):
		self.color = color
		self.children = []
		self.name = 'Group'

	@property
	def name(self):
		return self._name

	def _print(self, items, depth):
	    # this is so called "do use" utility
		items.append('*' * depth)  # * shows the level for children
		if self.color:
			items.append(self.color)
		items.append(f'{self.name}\n')
		for child in self.childrem:
			child._print(items, depth + 1)
	
	def __str__(self):
		# use recursive operation
		items = []
		self._print(items, 0)
		return ''.join(items)

class Circle(GraphicObject):
	@property
	def name(self):
		return 'Circle"

class Square(GraphicObject):
	@property
	def name(self):
		return "Square"

drawing = GraphicObject()
drawing.name = 'my drawing'
drawing.children.append(Square("Red")
drawing.children.append(Circle("Yellow")

group = GraphicObject()
group.children.append(Circle('Blue'))
group.children.append(Square('Blue'))
drawing.children.append(group)
print(drawing)
   # will print this
   """
   my drawing
   *RedSquare
   *YellowSquare
   *Group
   **BlueCircle
   **BlueSquare
   """	
```

## Command pattern
Perform and record certain operations

Example:
```python
class BankAcount:
	OVERDRAFT_LIMIT = -500

	def __init__(self, balance=0):
		self.balance = balance
	
	def deposit(self, amount):
		self.balance += amount
		print(f'Deposited {amount}'
			  f'balance= {self.balance}')

	def withdraw(self, amount):
		if self.balance - amount >= BankAccount.OVERDRAFT_LIMIT:
			self.balance -= amount
			print(f'Withdrew {amount}'
			      f'balance = {self.balance}')
	        return True

		return False

	def __str__(self):
		return f'Balance = {self.balance}'

"""You could, use these methods direcly and they will work, 
However, in order to have records for these operations we can use
the "Command" pattern. One good side effect is you will have the ability
to "undo" the operation
"""

"""Interface for command"""
class Command(ABC):
	def invoke(self):
		pass

	def undo(self):
		pass

class BankAcountCommand(Command):
	class Action(Enum):
		DEPOSIT=0
		WITHDRAW = 1
	
	def __init__(self, account, action, amount):
		self.amount = amount
		self.action = action
		self.account = account
		self.success = None

    def invoke(self):
		if self.action == self.Action.DEPOSIT:
			self.account.deposit(self.amount)
			self.success = True
		elif self.action == self.Action.WITHDRAW:
			self.success = self.account.withdraw(self.amount)

	def undo(self):
		if not self.success:
			return

		if self.action == self.Action.DEPOSIT:
			self.account.withdraw(self.amount)
		elif self.action == self.Action.WITHDRAW:
			self.account.deposit(self.amount)


if __name__ == '__main__':
	ba = BankAccount()
	cmd = BankAccountCommand(ba, BankAccountCommand.Action.DEPOSIT, 100)
	cmd.invoke()
	print(f'After $100 deposit: {ba}')

	cmd.undo()
	print(f'$100 undone: {ba}')

	illegal_withdraw_cmd = BankAccountCommand(ba, BankAccountCommand.Action.WITHDRAW, 1000)
	illegal_withdraw_cmd.invoke()
	print('After impossible withdrawal: {ba}')

	illegal_withdraw.cmd.undo()
	print('After undo: {ba}')
```
