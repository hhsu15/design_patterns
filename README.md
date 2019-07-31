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
```
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
