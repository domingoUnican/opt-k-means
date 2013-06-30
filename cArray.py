import ctypes

class cArray:
    """Fast boolean array implementation with support for logical operations"""

    cModule = None   #To be loaded by ctypes only once!!!
    
    def __init__(self, size, orig=None):
        """Creates the array, size is needed for C to do the allocation"""
        if not cArray.cModule:
            cArray.cModule=ctypes.cdll.LoadLibrary("./arraylib.so")
            #Arg & return types must be said explicitly, otherwise we are gonna get seg. faults when dealing with pointers.
            #pointers of 64 bit machines are longlong, if treated as int, they are truncated => seg. fault
            cArray.cModule.reserve_array.restype = ctypes.c_longlong
            cArray.cModule.reserve_array.argtypes = [ctypes.c_int]
            cArray.cModule.free_array.argtypes =    [ctypes.c_longlong]
            cArray.cModule.and_array.argtypes =     [ctypes.c_longlong,ctypes.c_longlong,ctypes.c_longlong,ctypes.c_int]
            cArray.cModule.or_array.argtypes =     [ctypes.c_longlong,ctypes.c_longlong,ctypes.c_longlong,ctypes.c_int]
            cArray.cModule.not_array.argtypes =     [ctypes.c_longlong,ctypes.c_int]
            cArray.cModule.get_element.argtypes =   [ctypes.c_longlong,ctypes.c_int]
            cArray.cModule.set_element.argtypes =   [ctypes.c_longlong,ctypes.c_int,ctypes.c_int]
            
        self.size=size
        self.arrayRef=cArray.cModule.reserve_array(ctypes.c_int(self.size))
        self.myCModule=cArray.cModule #on the destructor, cArray can not be accesed anymore, hence the object should store a ref to this.
        if orig != None:
            for i in range(size):
                self.__setitem__(i,orig[i])

       

    def __del__(self):
        """Used by the destructor, used to free the C allocated array"""
        #self.myCModule.free_array(self.arrayRef)
        pass
        
    def __len__(self):
        """Provides the overload for []"""
        return self.size
    
    def __getitem__(self,key):
        """Provides the overload for []"""
        return cArray.cModule.get_element(self.arrayRef,ctypes.c_int(key))

    def __setitem__(self,key, value):
        """Provides the overload for []"""
        cArray.cModule.set_element(self.arrayRef,ctypes.c_int(key),ctypes.c_int(value)) 
      
    def __str__(self):
        """Used mostly to print and debug"""
        my_str="["
        for elem in range(self.size):
            x=cArray.cModule.get_element(self.arrayRef,ctypes.c_int(elem))
            my_str+=str(x)+" "
        my_str+="]"
        return my_str
   
    def arrayAnd(self,other):
        cArray.cModule.and_array(self.arrayRef,self.arrayRef,other.arrayRef,ctypes.c_int(self.size))
      
    def arrayOr(self,other):
        cArray.cModule.or_array(self.arrayRef,self.arrayRef,other.arrayRef,ctypes.c_int(self.size))
    
    def arrayNot(self):
        cArray.cModule.not_array(self.arrayRef,ctypes.c_int(self.size))

if __name__ == "__main__":
  
   from time import time
   
   size=10
   my_array=cArray(size)
   my_array[5]=True
   my_array[3]=True
   my_array[2]=True
   my_array[7]=True

   print "array 1 is "+str(my_array)
   my_array2=cArray(size)
   my_array2[3]=True
   my_array2[7]=True
   my_array2[1]=True
   my_array2[6]=True
   print "array 2 is "+str(my_array2)
   my_array.arrayOr(my_array2)
   print "result  is "+str(my_array)
   
   size=20000000
   my_array=cArray(size)
   my_array[5]=True
   my_array[3]=True
   my_array[2]=True
   my_array[7]=True

   #print "array 1 is "+str(my_array)
   my_array2=cArray(size)
   my_array2[3]=True
   my_array2[7]=True
   my_array2[1]=True
   my_array2[6]=True
   #print "array 2 is "+str(my_array2)
   time_s=time()
   my_array.arrayAnd(my_array2)
   time_e=time()
   print "For "+str(size)+" C version took "+str(time_e-time_s)
   
   #Now python time
   
   list1=size*[False]
   list2=size*[False]
   time_s=time()
   for i in range(size):
      list1[i]=list1[i]&list2[i]
   time_e=time()
   print "For "+str(size)+" Py version took "+str(time_e-time_s)
   #print "result  is "+str(my_array)
  
  
