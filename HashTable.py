class HashTable(object):
    """ Linear Probing implmentation of the abstract data type HashTable
    
        Ana-Lea N; CSCI 361; 11/22/2020; For Extra Credit
    """
    def __init__(self):
        self.list_primes = [11, 19, 41, 79, 163, 317, 
                            641, 1279, 2557, 5119, 10243, 
                            20479, 40961, 81919, 163841, 327673]
    
        self.items = 0                                             # Elements in hashTable 

        self.thumb_prime = 0 
        self.capacity = self.list_primes[self.thumb_prime]         # Actual size of HashTable

        self.load_facor_indicator = 0.5

        self.values = [None for i in range(self.capacity)]
        self.keys =   [None for i in range(self.capacity)]
        self.valid =  [False for i in range(self.capacity)]
    
    def put(self, key, value):
        """ inseart key value pair into this hashTable. """
        if self.need_to_reload():
            self.resize()
        
        hash = self.get_hash(key)
        index = -1
        for i in range(hash, (self.capacity + hash)):
            index = ((i) % self.capacity)
            if (self.valid[index] == False):
                break
            elif (self.keys[index] == key):
                self.values[index] = value
                return
            
        self.keys[index] = key
        self.values[index] = value
        self.valid[index] = True
        self.items += 1

    def need_to_reload(self):
        """ Check if we need to increase size of our arrays to keep loadfactor down """
        return (self.items/self.capacity >= self.load_facor_indicator)

    def get_hash(self, key):
        """ returns the hash of a given key """
        return ((hash(key) & 0x7fffffff) % self.capacity)

    def resize(self):
        """ resize all array, adding all old key values to the new bigger home """
        if self.thumb_prime >= len(self.list_primes) - 1:
            return # cannot resize; no more room
        
        #save old values
        tmpKeys =  self.keys
        tmpVals =  self.values
        tmpValid = self.values

        #init new bigger arrays
        self.thumb_prime = self.thumb_prime + 1
        self.capacity = self.list_primes[self.thumb_prime]

        self.values = [None for i in range(self.capacity)]
        self.keys =   [None for i in range(self.capacity)]
        self.valid =  [False for i in range(self.capacity)]

        self.items = 0

        for i in range(len(tmpKeys)):
            if(tmpValid[i]):
                self.put(tmpKeys[i], tmpVals[i])

    def get(self, key):
        """ returns the value associated with the key """
        hash = self.get_hash(key)
        index = -1

        for i in range(hash, (self.capacity + hash)):
            index = ((i) % self.capacity)
            if (self.valid[index] == False):
                break
            elif (self.keys[index] == key):
                return self.values[index]
        return None

    def delete(self,key):
        """ Deletes this entry based on i.d./key"""
        if not self.contains(key):
            return False
        
        index = self.get_hash(key)
        while not key == self.keys[index]:
            index = (index + 1) % self.capacity # find the key, what's its index
        self.valid[index] = False

        index = (index + 1) % self.capacity

        # Go through deleted node's cluster, fix them up
        while not self.valid[index]:
            key_redo = self.keys[index]
            val_redo = self.values[index]
            self.valid[index] = False
            self.items -= 1

            self.put(key_redo, val_redo)
            index = (index + 1) % self.capacity
        
        self.items -= 1 # delete the final one.
        return True
    
    def size(self):
        return self.items
    
    def contains(self, key):
        """ Does this key exist in the hashtable? """
        hash = self.get_hash(key)
        index = -1

        for i in range(hash, (self.capacity + hash)):
            index = ((i) % self.capacity)
            if (self.valid[index] == False):
                return False
            elif (self.keys[index] == key):
                return True
        return False

    def isEmpty(self):
        return self.items == 0

    def __str__(self):
        string = "{"
        for i in range(self.capacity):
            if self.valid[i]:
                string += '{}({}) : {}, '.format(str(self.keys[i]), str(self.get_hash(self.keys[i])), str(self.values[i]))  
        
        string = string[0:-2] + "}"
        return string
