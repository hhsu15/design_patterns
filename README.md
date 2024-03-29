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

### Example 2

```python
from abc import ABC
from collections.abc import Iterable

class Connectable(Iterable, ABC):
    """base class"""
    def connect_to(self, other):
	    if self == other:
		    return

        for s in self:
		   for o in other:
		      s.outputs.append(o)
			  o.inputs.append(s)

class Neuron(Connectable):
    def __init__(self, name):
		self.name = name
		self.inputs = []
		self.outputs = []

	def __str__(self):
		return f'{self.name}' \
		       f'{len(self.inputs)} inputs, ' \
			   f'{len(self.outputs)} outputs'

	def __iter__(self):
	    "Turn a scala value into a collection"
		yield self

	#def connect_to(self, other):
	#   self.outputs.append(other)
	#	self.inputs.append(self)

class NeuronLayer(list, Connectable):
    def __init__(self, name, count):
	    super().__init__()
		self.name = name
		for x in range(0, count):
		    self.append(Neuron(f'{name}--{x}'))

	def __str__(self):
	    return f'{self.name} with {len(self)} neurons'

if __name__ = '__main__':
    # now imagine you have to connect two neurons but you don't want to end up having to write all the combinations
    neuron1 = Neuron('n1')
	neuron2 = Neuron('n2')
	layer1 = NeuronLayer('L1', 3)
	layer2 = NeuronLayer('L2', 3)

    neuron1.connect_to(neuron2)
	neuron1.connect_to(layer1)
	layer1.connect_to(neuron2)
	layer1.connect_to(layer2)

	print(neuron1)
	print(layer1)
	print(neuron2)
	print(layer2)


```

- Summary
  - Objects can use other objects via inheritance/composition
  - Some composed and singular objects need similar/identical behaviors
  - Composite design pattern lets us treat both types of objects uniformly
  - Python supports iteration with **iter** and Iterable ABC
  - A single object can make itself iterable by yielding `self` from **iter**

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
	def __init__(self):
		self.success = False

	def invoke(self):
		pass

	def undo(self):
		pass

class BankAcountCommand(Command):
	class Action(Enum):
		DEPOSIT=0
		WITHDRAW = 1

	def __init__(self, account, action, amount):
		super().__init__()
		self.amount = amount
		self.action = action
		self.account = account

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

class CompositBankAccountCommand(Command, list):
	"""Composite command
	It's a Command with the same interface and it's also a list

	"""
	def __init__(self, items=[]):
		super().__init__()
		for i in items:
			self.append(i)

	def invoke(self):
		for x in self:
			x.invoke()

 	def undo(self):
		for x in reversed(self):
			x.undo()


class MoneyTransferCommand(CompositeBankAccountCommand):
	def __init__(self, from_acct, to_acct, amount):
		super().__init__([
		  BankAccountCommand(from_acct,
		  					BankAccount.Action.WITHDRAW, amount),
		  BankAccountCommand(to_acct,
		  					BankCoountCommand.Action.DEPOSIT, amount)
		])

	def invoke(self):
		ok = True
		for cmd in self:
			if ok:
				cmd.invoke()
				ok = cmd.success
			else:
				cmd.success = False
		self.success = ok


class TestSuite(unittest.TestCase):
  	def test_composite_deposit(self):
	ba = BankAccount()
	deposit1 = BankAccountCommand(
		ba, BankAccountCommand.Action.DEPOSIT, 100
	)

	deposit2 = BankAccountCommand(
		ba, BankAccountCommand.Action.DEPOSIT, 50
	)

	composite = CompositeBankAccountCommand([deposit1, deposit2])
	composite.invoke()
	print(ba)

	composite.undo()
	print(ba)

	test_transfer(self):
		ba1 = BankAccount(100)
		ba2 = BankAccount()

		amount = 100

		transfer = MoneyTransferCommand(ba1, ba2, amount)
		transfer.invoke()
		print(ba1, ba2)

		transfer.undo()
		print(ba1, ba2)


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

	unittest.main()  # this will run the unittests
```

## Decorator

Ficilitates the addition of behaviors to individual objects without inheriting from them. Python decorator is one example.

```python
"""Dynamic class decorator"""

class FileWithLogging:
    def __init__(self, file):
        self.file = file

	def writelines(self, strings):
	    '''This is my custom method '''
		self.file.writelines(strings)
		print(f'wrote {len(strings)} lines')

	def __iter__(self):
		self.file.__iter__()

	def __next__(self):
		self.file.__next__()

	'''From below is what's cool here! We can save some time by using this dynamic programing.
	Essentially whatever methods we want to use from the underlying objects we use the following methods to delagate them to. For example, the "write" method'''
	def __getattr__(self, item):
		return getattr(self.__dict__['file'], item)

	def __setattr__(self, key, value):
		if key == 'file':
			self.__dict__[key] = value
		else:
			setattr(self.__dict__['file'], key, value)  # set

	def __delattr__(self, item):
		delattr(self.__dict__['file'], item)


if __name__ == '__main__':
	file = FileWithLogging(open('hello.txt', 'w'))
	file.writelines('hello', 'world')
	file.write('testing')
	file.close()
```

## Facade (pronouce like fasade)

Provide nice interface that will just work. Users don't need to know the implementation details
Example:

```python
class Buffer:
"Low level implementation api"
	def __init__(self, width=30, height=20):
		self.width = width
		self.height = height
		self.buffer = [' '] * (width * height)  # create buffer as placeholder

	def __getitem__(self, item):
		return self.buffer.__getitem__(item)

	def write(self, text):
		self.buffer += text


class Viewport:
	def __init__(self, buffer=Buffer()):
		self.buffer = buffer
		self.offset = 0

	def get_char_at(self, index):
		return self.buffer[index+self.offset]

	def append(self, text):
		self.buffer.write(text)

"""Now here comes the facade"""
class Console:
	def __init__(self):
		b = Buffer()
		self.current_viewport = Viewport(b)
		self.buffers = [b]
		self.viewports = [self.current_viewport]

	def write(self, text):
		return self.current_viewport.buffer.write(text)

	def get_char_at(self, index):
		return self.current_viewport.get_char_at(index)

if __name__ = '__main__':
	c = Console()
	c.write('hello')
	ch = c.get_char_at(0)
```

## Flyweight design patter

A space optimization technique that lets us use less memory by storing externally the data associated with simliar objects.

The way to do it is essentially:

- store common data externally
- specify an index or a reference into the external data store
- define the idea of "ranges" on homegeneous collections and store data related to those ranges
  Example:

```python
import string
import random

class User:
	def __init__(self, name):
		self.name = name

class User2:
	"""This one uses Flyweight pattern
	We are storing the pointers for the chars
	"""
	strings = [] # a static variable bound to the class storing all the string names. So the idea is all the objects will point the names to here rather than storing the names with them

	def __init__(self, full_name):
		"""simply store the indeces for the setup"""
		def get_or_add(s):
			if s in self.strings:
				return self.strings.index(s)
			else:
				self.strings.append(s)
				return len(self.strings) - 1

		# this will give you two indices for your name. One for first name, one for last name
		self.names = [get_or_add(x)
					  for x in full_name.split(' ')]  # loop thru first name and last name

	def __str__(self):
		return ' '.join([self.strings[x] for x in self.names])

def random_string():
	chars = string.ascii_lowercase
	return ''.join(
	  [random.choice(chars) for i in range(8)]
	)



if __name__ == '__main__':
	users = []

	first_names = [random_string() for x in range(100)
	last_names = [random_string() for x in range(100)]

	for first in first_names:
		for last in last_names:
		 	users.append(User2(f'{first} {last}')

```

```python
class FormattedText:
	def __init__(self, plain_text):
		self.plain_text = plain_text
		self.caps = [False] * len(plain_text)

	def capitalize(self, start, end):
		for i in range(start, end):
			self.caps[i] = True

	def __str__(self):
		result = []
		for i in range(len(self.plain_text)):
			c = self.plain_texy[i]
			result.append(
			  c.upper() if self.caps[i] else c
			)
		return ''.join(result)

class BetterFormattedText:
"""Flyweight version"""
	def __init__(self, plain_text):
		self.plain_text = plain_text
		self.formatting = []

	class TextRange:
	    """The essense of flyweight"""
		def __init__(self, start, end, capitalize=False):
			self.start = start
			self.end = end
			self.capitalize = capitalize

		def covers(self, position):
			return self.start <= position <= self.end

	def get_range(self, start, end):
		range = self.TextRange(start, end)
		self.formatting.append(range)
		return range  # return the TextRrange obj so you can subsquently call the method, say `.capitalize`

	def __str__(self):
		result = []
		for i in range(len(self.plain_text)):
			c = self.plain_text[i]
			for each_range in self.formating:
				if each_range.covers(i) and each_range.capitalize:
				c = c.upper()
			result.append(c)
		return ''.join(result)


if __name__ == '__main__':
	text = 'hello world'
	ft = FormattedText(text) # the problem with this is if the text is large, say 1 million words we would end up assigned 1 million boolean values.
	ft.capitalized(0, 4)
	print(ft)

	bft = BetterFormattedText(text)
	bft.get_range(2, 6).capitalize = True

```

## Proxy design pattern

A class that functions as an interface to a particular resource. That resource may be remote, expensive to construct, or may require logging or some other added functionalities.

A typical proxy class is "protection proxy". For example, for access control

```python
class Car:
	def __init__(self, driver):
		self.driver = driver

	def drive(self):
		print(f'Car is driving by {self.driver.name}')

# now you want to change the sementics without changing the code for Car implementation. Here comes the protection proxy
class CarProxy:
	def __init__(self, driver):
		self.driver = driver
		self._car = Car(driver)

    def drive(self):
		if self.driver.age < 21
			print('Driver is too young')
		else:
			self._car.drive()


class Driver:
	def __init__(self, name, age):
		self.name = name
		self.age = age

if __name__ == '__main__':
	driver = Driver('John', 20)
	car = CarProxy(driver)
	car.drive()
```

- Example of Virtual Proxy
- the goal is without changing the underlying object (i.e., OCP) but somehow have it look the same but work the way we want. Below example shows how we can use virtual proxy to avoid loading image when obj is created

```python
class BipMap:
	def __init__(self, filename):
		self.filename = filename
		print(f'Loading image from {self.filename}') # this is what we try to mask

	def draw(self):
		print('drawing image')

def draw_image(image):
	print('About to draw image')
	image.draw()
	print('Done drawing image')

class LazyBitMap:
    """Virtual proxy"""
	def __init__(self, filename):
		self.filename = filename
		self._bitmap = None

	def draw(self):
		if not self._bitmap:
			self._bitmap = BitMap(self.filename)
		self._bitmap.draw()

if __name__ = '__main__':
	bmp = BitMap('something.jpg') # this will load the image even though you don't draw it which can be expensive
	draw_image(bmp)

	# use the virtual proxy
	bmp = LazyBitMap(something.jpg)
	draw_image(bmp)
	draw_image(bmp) # if you draw the same thing twice you will see it only gets load once.

```

#### Proxy VS. Decorator

Proxy provides an identical interface to the underlying components; decorator provides an enhanced interface

## Chain of Respobsibility design patter

A chain of components who all get a chacne to process a command or a query, optionally having default processing implementation and a ability to terminate the processing chain.

- Example using chain of reference (linked list)

```python
class Creature:
	def __init__(self, name, attack, defence):
		self.name = name
		self.attack = attack
		self.defense = defense

	def __str__(self):
		return f'{self.name} ({self.attack})/{self.defence})'

class CreatureModifier:
    """Base class"""
	def __init__(self, creature):
		self.creature = creature
		self.next_modifier = None  # This is where we build the chain so you can pick up multiple modifier on a creature.

	def add_modifier(self, modifier):
	    """To provide the chain effect"""
		if self.next_modifier: # if we already have a modifier ofcouse we will call the next modifier (recursive here)
			self.next_modifier.add_modifier(modifier)
		else:
			self.next_modifier = modifier

	def handle(self):
		"""becasue this is a base class, we are relying on the sub class to handle"""
		if self.next_modifier:
			self.next_modifier.handle()

class DoubleAttackModifier(CreatureModifier):
	def handle(self):
		print(f'Doubling {self.creature.name}' 's attak')
		self.creature.attack *= 2
		super().handle()  # criticle! call the base class's handle becasue it's the one that propagates the chain responsibilities

class IncreaseDefenseModifier(CreatureModifier):
	def handle(self):
		if self.creature.attack <= 2:
		print(f'Increasing {self.creature.name} defense')
		self.creature.defense += 1
		super().handle()

class NoBonusesModifier(CreateModifier):
    """If you don't want the chain of resposibilities,
	You do not call the super().handle()
	"""
	def handle(self):
		print('no bonuses for you')


if __name__ == '__main__':
	goblin = Creature("Goblin", 1, 1)
	print(goblin)

	# here is the idea, you have a root top level element
	root = CreatureModifier(goblin)  # this is the base abstract class which does not do anything
	# what we can do, is to apply custom modifier object under the root.

    # root.add_modifier(NoBonusesModifier(goblin)) # if you apply this modifier then no other modifier will be applied. This will essentially stop the chain of responsibilities
	root.add_modifier(DoubleAttackModifier(goblin))
	root.add_modifier(DoubleAttackModifier(goblin)) # apply same modifier twice
	root.add_modifier(IncreaseDefenseModifier(goblin)) # apply different modifier
	root.handle()
	print(goblin)

```

### Command Query Separation (CQS)

To allow you to invoke the chain of responsiblities dynamically..
it's quite complex and we are using the following design patterns

- Event Broker (observer design pattern)
- CQS
  So it works like this,
- you have a Event which is a list of functions
- When you apply a modifier it adds the function to the event
- "Game" object keeps track of the events(queries)
- When you print the creature object it essentially triggers all all queries (event) by calling `attack` and `defense` property
- you can also apply the scope using `with` to limit the effect of the modifier
- Example using centralized construct:

```python
class Event(list):
    """Event is a list of functions you can call"""
	def __call__(self, *args, **kwargs):
		for item in self:
			item(*args, **kwargs)

class WhatToQuery(Enum):
	ATTACK = 1
	DEFENSE = 1

class Query:
	def __init__(self, creature_name, what_to_query, default_value):
		self.value = default_value
		self.what_to_query = what_to_query
		self.creature_name = creature_name

class Game:
    """Event Broker that basically stores all the event functions"""
	def __init__(self):
		self.queries = Event()

    def perform_query(self, sender, query):
	    """Call a list of functions"""
		self.queries(sender, query)

class CreatureModifier(ABC):
	def __init__(self, game, creature):
		self.game = game
		self.creature = creature
		self.game.queries.append(self.handle)

	def handle(self, sender, query):
		pass

	def __enter__(self):
		pass

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.game.queries.remove(self.handle) # remove from the event

class DoubleAttackModifier(CreatureModifier):
	def handle(self, sender, query):
		if sender.name == self.creature.name and \
			query.what_to_query == WhatToQuery.ATTACK:
			query.value *= 2  # this is where the attribute value gets modified

class Creature:
	def __init__(self, game, name, attack, defense):
		self.initial_defense = defense
		self.initial_attack = attack
		self.name = name
		self.game = game

	@property
	def attack(self):
		#query
		q = Query(self.name, WhatToQuery.ATTACK, self.initial_attack)
		self.game.perform_query(self, q)
		return q.value

	@property
	def defense(self):
		#query
		q = Query(self.name, WhatToQuery.DEFENSE, self.initial_defense)
		self.game.perform_query(self, q)
		return q.value

	def __str__(self):
		return f'{self.name} ({self.attack}/{self.defense})'

if __name__ == '__main__':
	game = Game()
	goblin = Creature(game, 'Strong Goblin', 2, 2)
	print(goblin)

	with DoubleAttackModifier(game, goblin): # as soon as it's built, the DoubleAttackModifier is going to intercept the goblin and change it's value
	    print(goblin) # should print "Strong Goblin (4/2)

    print(goblin)  # should print (2/2) since it's out of scope
```

## Interpreter

Interpreper design pattern. Make them object oriented structure.
Mainly lex anbd parse

Example:

```python
class Token:
	class Type(Enum):
		INTEGER = auto()
		PLUS = auto()
		MINUS = auto()
		LPAREN = auto()
		RPAREN = auto()

	def __init__(self, type, text):
		self.type = type
		self.text = text

	def __str__(self):
		return f'`{self.text}`'

def lex(input):
   result = []
   i = 0
   while i < len(input):
   	if input[i] == '+':
		result.append(Token(Token.Type.PLUS, '+'))

   	if input[i] == '-':
		result.append(Token(Token.Type.MINUS, '-'))

   	elif input[i] == '(':
		result.append(Token(Token.Type.LPAREN, '('))

	elif input[i] == ')':
		result.append(Token(Token.Type.RPAREN, ')'))

	else:
	    # get the integer
		digits = [input[i]] # start with current digit
		for j in range(i+1, len(input)):
			if input[j].isdigit():
				digits.append(input[j])
				i += 1
			else:
				result.append(Token(Token.Type.INTEGER,
									''.join(digits)))
				break
	i += 1
		return result

class Integer:
	def __init__(self, value):
		self.value = value

class BinaryExpression:
	class Type(Enum):
		ADDITION = auto()
		SUBSTRACTION = auto()

	def __init__(self):
		self.type = None
		self.left = None  # left part for binary exression
		self.right = None  # right part for binary expression

	@property
	def value(self):
		if self.type = self.Type.ADDITION:
			return self.left.value + self.right.value # left plus right
		elif self.type = self.Type.SUBSTRACTION:
			return self.left.value - self.right.value # left minus right


def parse(tokens):
	"""Traverse the tokens and parse the elements"""
	result = BinaryExpresiion() # result is always going to be BinaryExpression

	have_lhs = False # have left hand side
	i = 0
	while i < len(tokens):
		token = tokens[i]

		if token.type == Token.Type.INTEGER:
			integer = Integer(int(token.text))
			if not have have_lhs:
				result.left = integer
				have_lhs = True # now I have left hand side

			else:
				result.right = integer # now I have right hand side
		elif token.type = Token.Type.PLUS:
			result.type = BinaryExpression.Type.ADDITION
		elif token.type = Token.Type.MINUS:
			result.type = BinaryExpression.Type.SUBSTRACTION

		# this is the difficult part when you see parathesis
		# a recursive operation which basically
		elif toke.type = Token.Type.LPAREN:
			j = i
			while j < len(tokens): # start with where you are
				if tokens[j].type = Token.Type.RPAREN: # advance until you find the right parenthesis
					break
				j += 1

			subexpression = tokens[i+1:j] # parse the subexpressio within the parenthesises
			element = parse(subexpression) # pass the subex to parse recursively. Remember "parse()" returns BinaryExpression
			if not have_lfs:
				result.left = element
				have_lhs = True
			else:
				result.right = element
			i = j
		i += 1
	return result


def calc(input):
	tokens = lex(input)
	print(' '.join(map(str, tokens)))
    parsed = parse(tokens)


if __name__ = '__main__':
	calc('(13+4)+(3+25)')
```

## Iterator design pattern

An object that facilitates the traversal of a datastructure

Normally, you woukd implement the `__iter__` with `__next__` protocal however in reality it can result in ugly and messy code, so here is an example of a nice and readable implementation (without the custom iter object

```python
class Node:
	def __init__(self, value, left=None, right=None):
		self.right = right
		self.left = left
		self.value = value

		self.parent = None
		if self.left:
			self.left.parent = self
		if self.right:
			self.right.parent = self

	def __iter__(self):
		return InOrderIterator(self)

class InOrderIterator:
	def __init__(self, root):
		self.root = self.current = root
		self.yielded_start = False
		while self.current.left:
			self.current = self.current.left

    def __next__(self):
		....this is going to be ugly so I give up. Essentially this a stateful way which keeps manipulating `self.current` and eventually return self.current

def traverse_in_order(root):
	"""This is the more elegant way of implementation you would find in the text book.
	Basically, you "yield" from the left to right
	"""
	def traverse(current):
		if current.left:
			for left in traverse(current.left):
				yield left
			# after you are done with the left side, you yield the current element
			yield current
			for right in traverse(current.right):
				yield right

	for node in traverse(root):
		yield node


if __name__ = '__main__':
	# in-order

	root = Node(1, Node(2), Node(3)) # in-order will give you 2, 1, 3

	for y in traverse_in_order(root):
		print(y.value)

```

# Array Backed Properties

This is very interesting design. Essentially rather than normallyhow would you set up the attributes and make properties for calcuated result, you create a list that stores the values of those property which allows you to be more easily manage the computation.

```python
class Creature:
	_strength = 0
	_agility = 1
	_intelligence = 2

	def __init__(self):
        # so intead of creating these attributes...
		#self.strength = 10
		#self.agility = 10
		#sefl.intelligence = 10

		self.stats = [10, 10, 10]  # just one attribute

	@property
	def sum_of_stats(self):
		# return self.strength + self....... # this is annoying
		return sum(self.stats) # now this is much easier

	@property
	def max_of_stats(self):
		return max(self.stats)

	@property
	def avg_of_stats(self):
		return self.sum_of_stats / len(self.stats)

	@property
	def strength(self):
		"""So you can still access these as properties"""
		return self.stats[Creature._strength]

	@strength.setter
	def strength(self, value):
		self.stats[Creature._strength] = value



```

## Mediator

In a system the components can be in and out at anytime and therefore it does not make senset to directly reference each one, Like chat room. A chat midiator will connect everyone in the same room and allow everyone to send messages to one another

- create the mediator and have each object in the system refer to it (e.g., in a property)
- midiator engages in bidirectional communication with its connected components
- mediator has functions the components can call (like broadcast)
- components have functions mediator can call (like receive)
- Evenbt processing libraries make communication easier to implement (i.e., the components will subscribe the functions to the event and you can just fire the events)

```python

class Person:
	def __init__(self, name):
		self.name = name
		self.chat_log = []

		self.room = None  # this will be assigned as chat room

	def receive(self, sender, message):
		s = f'{sender}: {message}'
		print(f'[{self.name}\'s chat session] {s})
		self.chat_log.append(s)

	def private_message(self, who, message):
	    """Use the chatroom mediator"""
		self.room.message(self.name, who, message)

	def say(self, message):
		self.room.broadcast(self.name, message)


class ChatRoom:
	def __init__(self):
		self.people = []

	def join(self):
		join_msg = f'{person.name} joins the chat'
		self.broadcast('room', join_msg)
		person.room = self
		self.people.append(person)

	def broadcast(self, source, msg):
		for p in self.people:
			if p.name != source:
				p.receive(source, message)

	def message(self, source, destination, message):
		for p in self.people:
			if p.name == destination:
				p.receive(source, message)

if __name__ == '__main__':
	room = ChatRoom()

	jane = Person('Jane')
	john = Person('John')

	room.join(john)
	room.join(jane)

	john.say('hi room')
	jane.say('hi John')

	simon = Person('Simon')
	room.join(simon)
	simon.say(('hi everyone')

	jane.private_msg("glad you can join us")

```

### Mediator with Events

```python

class Event(list):
	"""Recall event is a list of functions"""
	def __call__(self, *args, **kwargs):
		for item in self:
			item(*args, **kwargs)


class Game:
	"""Mediator."""
	def __init__(self):
		self.events = Event()

	def fire(self, args):
		self.events(args)


class GoalScoredInfo:
	def __init__(self, who_scored, goals_scored):
		self.who_scored = who_scored
		self.goals_scored = goals_scored

class Player:
	def __init__(self, name, game):
		self.name = name
		self.game = game
		self.goals_scored = 0

	def score(self):
		self.goals_scored += 1
		# when someone scored, we want to broadcast the event to people who subscribe to the game
		args = GoalScoredInfo(self.name, self.goal_scored)
		self.game.fire(args) # use the game mediator to fire the events

class Coach:
	def __init__(self, game):
		# they need to subscribe to the game's events
		game.events.append(self.celebrate_goal)
		game.events.append(self.say_oh_yeah)

	def celebrate_goal(self, args):
		if isinstance(args, GoalScoreIndo) and \
			args.goals_scored < 3:
			print(f'Coach says: well done, {args.who_scored}')

	def say_oh_yeah(self, args):
		print(f'Oh yeah!')

if __name__ = "__main__":
	game = Game()
	player = Player("Sma", game)
	coach = Coach(game)

	player.score()
	player.score()

```

## Memento design pattern

Memento takes a snapshot of a state which will allow you to restore the system to that state. Memento is simply a token/handle class with no functions of its own.
We can use memento to perform undo and redo functions

```python

class BankAccount:
	def __init__(self, balance):
		self.balance = balance
		# to be able to perform "undo" and "redo" we can store all the snapshots (mementos)
		self.changes = [Memento(self.balance)]  # this encapcilates all the states
		self.current = 0  # start with position 0
	def deposit(self, val):
		self.balance += val
		m = Memento(self.balance) # make a memento
		self.changes.append(m) # add to chagnes
		self.current += 1  # you are now in this memento
		return m

	def restore(self, memento):
		if memento:
			self.balance = memento.balance
			self.changes.append(memento) # again, add this state to changes
			self.current = len(self.changes) - 1  # when you resore, you move back one step

	def undo(self):
		if self.current > 0:
			self.current -= 1
			m = self.changes[self.current]
			self.balance = m.balance
			return m
		return None

	def redo(self):
		if self.current + 1 < len(self.changes):
			self.current += 1
			m = self.changes[self.current]
			self.balance = m.balance
			return m
		return None

	def __str__(self):
		return f'Balance = {self.balance}'

class Memento:
	def __init__(self, balance):
		self.balance = balance

if __name__ == '__main__':
	ba = BankAccount(100)
	ba.deposit(50)
	ba.deposit(25)

	ba.undo() # will give you balance of 150
    ba.undo() # will give you balance of 100
	ba.redo() # will give balance back to 150

```

## Observer

This is probablly the most popular design pattern. You want to observe certain events and get alerted when the event occurs.

```python
class Event(list):
	def __call__(self, *args, **kwargs):
		for item in self:
			item(*args, **kwargs)

class Person:
	def __init__(self, name, address):
		self.name = name
		self.address = address
		self.falls_ill = Event()

	def catch_a_cold(self):
		self.falls_ill(self.name, self.address)

def call_a_doctor(name, address):
	print(f'{name} needs a doctor at {address}')

def drink_more_water():
	print("need to drink more water")

if __name__ == '__main__':
	person = Person('Ken', '111 New York Road')
	person.falls_ill.append(call_a_doctor)  # susbcription
	person.falls_ill.append(drink_more_water) # subscription

    person.falls_ill.remove(call_a_doctor) # remove the subscription
	person.catch_a_cold()
```

### Property Observer

Tells you when property is actually changed

```python
class Event(list):
	def __call__(self, *args, **kwargs):
		for item in self:
			item(*args, **kwargs)

class PropertyObservable:
	def __init__(self):
		self.property_changed = Event()

class Person(PropertyObservable):
	def __init__(self, age=0):
		super().__init__()
		self._age = age

	@property
	def age(self):
		return self._age

	@age.setter
	def age(self, value):
		if self._age == value:
			return

		self._age = value
		self.property_changed('age', value)  # this is how you would notify

class TrafficAuthority:
	def __init__(self, person):
		self.person = person
		person.property_changed.append(
			self.person_changed
		)

	def person_changed(self, name_of_property, value):
		"""This is the method we want to subscirbe to the property change"""
		if name_of_property == 'age':
			if value < 16:
			print("sorry you can't drive")
		else:
			print("Okay, you can drive now")
			self.person.property_changed.remove(
				self.person_changed
			)

if __name__ == '__main__':
	p = Person()
	ta = TrafficAuthority(p)
	for age in range(14, 20):
		print(f'setting age to {age}')
		p.age = age

```

## State (State machine)

A pattern in which the object's behavior is determined by its state. An object transitions from one state to another (something needs to trigger a transition)

A formalized construct which managges state and transitions is called a state machine.

```python
from enum import Enum, auto


class State(Enum):
	OFF_HOOK = auto()  # pick up the phone
	CONNECTING = auto()
	CONNECTED = auto()
	ON_HOLD = auto()
	ON_HOOK = auto()  # hang up the phone


class Trigger(Enum):
	CALL_DIALED = auto()
	HUNG_UP = auto()
	CALL_CONNECTED = auto()
	PLACED_ON_HOLD = auto()
	TAKEN_OFF_HOLD = auto()
	LEFT_MESSAGE = auto()

if __name__ == '__main__':
	rules = {
		State.OFF_HOOK: [
			(Trigger.CALL_DIALED, State.CONNECTING)
		],
		State.CONNECTING: [
			(Trigger.HUNG_UP, State.CONNECTED),
			(Trigger.CALL_CONNECTED, State.CONNECTED)
		],
		State.CONNECTED: [
			(Trigger.LEFT_MESSAGE, State.ON_HOOK),
			(Trigger.HUNG_UP, State.ON_HOOK),
			(Trigger.PLACED_ON_HOLD, State.ON_HOD)
		],
		... # you get the idea
	}

	start_state = State.OFF_HOOK
	exit_state = State.ON_HOOK

	while state != exit_state:
		print(f'The phone is currently {state}')

		# loop thru all the options in current state
		for i in range(len(rules[state])):
			trigger = rules[state][i][0]
			print(f'{i}: {trigger}')

		idx = int(input("Select a trigger"))
		st = rules[state][idx][1]
		state = st
	print("We are done using the phone")
```

## Strategy design pattern

Essentially it's blueprint which enables the exact behavior of a system to be selected at run-time. Strategy does this through composition.

```python
from abc import ABC
from enum import Enum, auto

class ListStrategy(ABC):
	"""Blueprint for your algo."""
	def start(self, buffer): pass
	def end(self, buffer): pass
	def add_list_item(self, buffer, item): pass

class OutputFormart(Enum):
	MARKDOWN = auto()
	HTML = auto()

class MarkdownListStrategy(ListStrategy):
	def add_list_item(self, buffer, item):
		buffer.append(f'* {item}\n')

class HtmlStrategy(ListStrategy):
	def start(self, buffer):
		buffer.append('<ul>\n')

	def end(self, buffer):
		buffer.append('</ul>\n')

	def add_list_item(self, buffer, item):
		buffer.append(f'  <li>{item}</li>\n')


class TextProcesser:
	def __init__(self, list_strategy=HtmlStrategy()):
		self.buffer = []
		self.list_strategy = list_strategy

	def append_list(self, items):
		ls = self.list_strategy
		ls.start(self.buffer)
		for item in items:
			ls.add_list_item(self.buffer, item)
		ls.end(self.buffer)

	def set_output_format(self, format):
		if format = OutputFormat.MARKDOWN:
			self.list_strategy = MarkDownListStrategy()
		elif format == OutputFormat.HTML:
			self.list_stratefy = HtmlListStrategy()

	def clear(self):
		self.buffer.clear()

	def __str__(self):
		return ''.join(self.buffer)

if __name__ == '__main__':
	items = ['foo', 'bar', 'baz']

	tp = TextProcesser()
	tp.set_output_format(OutputFormat.MARKDOWN)
	tp.append_list(items)
	print(tp)

	tp.clear()
	tp.set_output_format(OutputFormat.HTML)
	tp.append_list(items)
	print(tp)


```

## Template design patter

Similar to Strategy design pattern, but rather than using composition it does it thru inheritance.

```python
from abc import ABC

class Game(ABC):
	"""Skeleton of any kind of game"""
	def __init__(self, number of players):
		self.number_of_players = number_of_players
		self.current_player = 0

	def run(self):
		"""This is the Template method."""
		self.start()
		while not self.have_winner:
			self.take_turn()
		print(f'Player {self.winnder_player} wins!')

	def start(self): pass

	@property
	def have_winner(self): pass

	def take_turn(self): pass

	@property
	def winner_player(self): pass

class Chess(Game):
	def __init__(self):
		super().__init__(2)
		self.max_turns = 10
		self.turn = 1

	def run(self):
		super().run()

	def start(self):
		print(f'Starting a game of chess with '
			  f'{self.number_of_players} players')

	@property
	def have_winnder(self):
		return self.turn == self.max_turns

	def take_turn(self):
		print(f'Turn {self.turn} taken by player '
		      f'{self.current_player}')

		self.turn += 1
		self.current_palyer = 1 - self.current_player

	@property
	def winning_player(self):
		return self.current_player

if __name__ == '__main__':
	chess = Chess()
	chess.run()

```

## Vistor

A component that knows how to traverse a data structure composed of possibly related types.

Intrusive solution example

```python
from abc import ABC

class Expression(ABC):
	pass

class DoubleExpression(Expression):
	def __init__(self, value):
		self.value = value

#	def print(self, buffer):
#		buffer.append(str(self.value))
#
#	def eval(self):
#		return self.value

class AdditionExpression(Expression):
	def __init__(self, left, right):
		self.left = left
		self.right = right

#	def print(self, buffer):
#		buffer.append('(')
#		self.left.print(buffer)
#		buffer.append('+')
#		buffer.right.print(buffer)
#		buffer.append(')')
#
#	def eval(self):
#		return self.left.eval() + self.right.eval()

# this is called reflective approach in that you check the instance type
class ExpressionPriner:
	@staticmethod
	def print(e, buffer):
		if isinstance(e, DoubleExpression):
			buffer.append(str(e.value))
		elif isinstance(e, AdditionExpression):
			buffer.append('(')
			ExpressionPriter.print(e.left, buffer)
			buffer.append('+')
			ExpressionPrinter.print(e.right, buffer)
			buffer.append(')')

# to propagate so you can use e.print()
Expression.print = lambda self, b: \
	ExpressionPrinter.print(self,b)

if __name__ == '__main__':
	e = AdditionExpression(
		DoubleExpression(1),
		AdditionExpression(
			DoubleExpression(2),
			DoubleExpression(3)
		)
	)

	buffer = []  # this is the element sorta vistor
    ExpressionPrinter.print(e, buffer)
	#e.print(buffer)
	print(''.join(buffer), '='., e.eval())


```

#### Double dispatch

```python
# use the code from above
# we ha ve another ExpressionPrinter

class DoubleExpression:
	def __init__(self, value):
		self.value = value

	def accept(self, visitor):
		vistor.visit(self) # this will be redicted to the proper visit method. so for example, if I pass a self (DoubleExpression), I will end up in the visit that expects de(DoubleExpression)

class AdditionExpression:
	def __init__(self, left, right):
		self.left = left
		self.right = right

	def accept(self, visitor):
		visitor.visit(self)

class ExpressionPrinter:
	def __init__(self):
		self.buffer = []

    @visitor(DoubleExpression)
	def visit(self, de):
		self.buffer.append(str(de.value))

	@visitor(AditionExpression)
	def visit(self, ae):
		self.buffer.append('(')
		self.left.accept(self)
		self.buffer.append('+')
		ae.right.accept(self)
		self.buffer.append(')')

	def __str__(self):
		return ''.join(self.buffer)

# this is the magic decorator that does the redirection

def _qualname(obj):
    """Get the fully-qualified name of an object (including module)."""
    return obj.__module__ + '.' + obj.__qualname__

def _declaring_class(obj):
    """Get the name of the class that declared an object."""
    name = _qualname(obj)
    return name[:name.rfind('.')]

# Stores the actual visitor methods
_methods = {}

# Delegating visitor implementation
def _visitor_impl(self, arg):
    """Actual visitor method implementation."""
    method = _methods[(_qualname(type(self)), type(arg))]
    return method(self, arg)

# The actual @visitor decorator
def visitor(arg_type):
    """Decorator that creates a visitor method."""

    def decorator(fn):
        declaring_class = _declaring_class(fn)
        _methods[(declaring_class, arg_type)] = fn

        # Replace all decorated methods with _visitor_impl
        return _visitor_impl

    return decorator


```

*Update:*

To overload a function or method, you can use the `singledispatch` or `singledispatchmethod` provided by functools.

[Here](https://martinheinz.dev/blog/50)to read about about it.



