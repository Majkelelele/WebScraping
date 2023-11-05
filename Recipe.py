class Recipe:
    def __init__(self, ingredients, details, amount, title):
        self.ingredients = ingredients
        self.details = details
        self.amount = amount
        self.title = title

    def printIngredients(self):
        for i in self.ingredients:
            print(i)
    def printDetails(self):
        for i in self.details:
            print(i)
    def printInfo(self):
        print("Title: " + self.title)
        print("Amount: " + self.amount)
        print("INGREDIENTS:")
        self.printIngredients()
        print("DETAILS")
        self.printDetails()
    def writeInfo(self, file):
        file.write("Title: " + self.title)
        file.write("\n")
        file.write("Amount: " + self.amount)
        file.write("\n")
        file.write("INGREDIENTS:\n")
        for i in self.ingredients:
            file.write(i)
            file.write("\n")
        file.write("DETAILS:\n")
        for i in self.details:
            file.write(i)
            file.write("\n")
        file.write("\n")
