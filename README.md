# Design Pattern

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
