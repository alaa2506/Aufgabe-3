"""
Hier eine Klasse `DataSet` implementieren.

Die Klasse muss eine Unterklasse von `dataset.DataSetInterface` sein
und alle dort geforderten Methoden implementieren.
Bei den Methoden von `DataSetInterface` stehen auch weitere Infos
zur benoetigen Funktionalitaet!

Die hier implementierte Klasse wird spaeter mittels `from implementation import DataSet`
geladen und mit Daten befüllt. Anschließend werden die Daten ausgelesen und überprüft!

Alle drei Dateien liegen im gleichen Ordner.

"""	

# TODO

# Importe
# Klasse: DataSet


from dataset import DataSetInterface, DataSetItem

class DataSet(DataSetInterface):
    def __init__(self, items=None):
        print("Initializing DataSet...")
        super().__init__(items)  # Call the constructor of the superclass
        self.items = {}  # Initialize an empty dictionary to store DataSetItem objects
        if items is not None:
            for item in items:
                if isinstance(item, DataSetItem):
                    self.items[item.name] = item

    def __setitem__(self, name, id_content):
        print(f"__setitem__ called with name={name}, id_content={id_content}")
        if not isinstance(id_content, tuple) or len(id_content) != 2:
            raise ValueError("id_content must be a tuple with two elements (id, content)")

        id, content = id_content
        if not isinstance(id, int) or not isinstance(name, str):
            raise TypeError("id must be an int and name must be a str")

        self.items[name] = DataSetItem(name, id, content)
        print(f"Item set: {self.items[name]}")

    def __iadd__(self, item):
        print(f"__iadd__ called with item={item}")
        if not isinstance(item, DataSetItem):
            raise TypeError("Item must be a DataSetItem")
        self.items[item.name] = item
        return self

    def __getitem__(self, name):
        if name not in self.items:
            raise KeyError("Name nicht gefunden.")
        return self.items[name]

    def __delitem__(self, name):
        if name not in self.items:
            raise KeyError("Name nicht gefunden.")  
        del self.items[name] 
    def __contains__(self, name):
        return name in self.items  

    def __and__(self, dataset):
        new_dataset = DataSet()  
        for name in self.items:
            if name in dataset:
                new_dataset += self.items[name]  
        return new_dataset

    def __or__(self, dataset):
        new_dataset = DataSet()  
        for item in self.items.values():
            new_dataset += item  
        for item in dataset.items.values():
            new_dataset.items[item.name] = item  
        return new_dataset

    def __iter__(self):
        items = list(self.items.values())  
        if self.iterate_sorted:
            key_func = lambda item: getattr(item, self.iterate_key)  
            items.sort(key=key_func, reverse=self.iterate_reversed)  
        return iter(items)  

    def filtered_iterate(self, filter):
        for item in self:
            if filter(item.name, item.id):
                yield item  

    def __len__(self):
        return len(self.items) 

    def __str__(self):
        return f"DataSet mit {len(self)} Elementen: " + ', '.join([str(item) for item in self])