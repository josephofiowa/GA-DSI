class Shape:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    description = "This shape has not been described yet"
    author = "Nobody has claimed to make this shape yet"
    def area(self):
        return self.x * self.y
    def perimeter(self):
        return 2 * self.x + 2 * self.y
    def describe(self,text):
        self.description = text
    def authorName(self,text):
        self.author = text
    def scaleSize(self,scale):
        self.x = self.x * scale
        self.y = self.y * scale


'''
Define a class called "dog"
Define the __init__ function with 3 attributes
Define two attributes that can be changed later
Define five functions
'''

class dog:
    def __init__(self, breed, name):
        self.breed = breed
        self.name = name
    gender = 'Male'
    is_sitting = False
    def set_name(self, name):
        self.name = name
    def set_breed(self, breed):
        self.breed = breed
    def set_gender(self, gender):
        self.gender = gender
    
    def fetch(self):
        return 'Stick'
    def bark(self):
        return 'woof'*3
    
    def bite(self):
        if self.gender == 'Male':
            print 'Bite'
        else:
            print 'No, I am polite.'
    def sit(self):
        self.is_sitting = True
